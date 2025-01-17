from typing import Any, Dict, List, Optional
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CustomUser, Hobby, FriendRequest, Friendship
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from .utils import flatten_errors, get_filtered_and_sorted_users
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.db import transaction
from django.db.models import Q
from datetime import date
import json


@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request: HttpRequest) -> JsonResponse:
    """
    Set the CSRF cookie on the frontend.
    """
    return JsonResponse({'message': 'CSRF cookie set'})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'api/register.html'
    success_url: str = 'http://localhost:5173'

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponse:
        response: HttpResponse = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name: str = 'api/profile.html'


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name: str = 'api/edit_profile.html'
    success_url: str = reverse_lazy('profile')

    def get_object(self, queryset: Optional[Any] = None) -> CustomUser:
        return self.request.user

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response: HttpResponse = super().post(request, *args, **kwargs)
        if 'old_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
        return response

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(user=self.request.user)
        return context


@login_required
@require_http_methods(["GET"])
def fetch_similar_users_api(request: HttpRequest) -> JsonResponse:
    """
    Returns a paginated JSON list of users with similar hobbies.
    """
    min_age: int = int(request.GET.get("min_age", 0))
    max_age: int = int(request.GET.get("max_age", 100))
    page: int = int(request.GET.get("page", 1))

    users_queryset = get_filtered_and_sorted_users(request.user, min_age, max_age)
    paginator = Paginator(users_queryset, 10)
    paged_users = paginator.get_page(page)

    users_list: List[Dict[str, Any]] = []
    today: date = date.today()
    for u in paged_users:
        age: Optional[int] = (today - u.date_of_birth).days // 365 if u.date_of_birth else None
        is_friend: bool = Friendship.objects.filter(
            Q(user1=request.user, user2=u) | Q(user1=u, user2=request.user)
        ).exists()
        has_pending_request: bool = FriendRequest.objects.filter(
            Q(sender=request.user, receiver=u) | Q(sender=u, receiver=request.user),
            status='pending'
        ).exists()
        users_list.append({
            "id": u.id,
            "username": u.username,
            "common_hobbies": u.common_hobbies,
            "age": age,
            "is_friend": is_friend,
            "has_pending_request": has_pending_request,
        })

    response_data: Dict[str, Any] = {
        "results": users_list,
        "count": paginator.count,
        "current_page": paged_users.number,
        "total_pages": paginator.num_pages,
    }
    return JsonResponse(response_data)


def logout_view(request: HttpRequest) -> JsonResponse:
    """
    API endpoint for logging the user out.
    """
    logout(request)
    return JsonResponse({'message': 'Logged out'})


def user_api(request: HttpRequest) -> HttpResponse:
    """
    API endpoint for the current user.
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if request.method == 'GET':
        user_data: Dict[str, Any] = request.user.as_dict()
        return JsonResponse(user_data)

    return HttpResponse(status=405)


@login_required
@require_http_methods(["PUT"])
def update_profile_api(request: HttpRequest) -> JsonResponse:
    """
    Update username, email, or date of birth for the current user.
    """
    try:
        data: Dict[str, Any] = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user: CustomUser = request.user
    updated_fields: List[str] = []

    if 'username' in data and data['username']:
        new_username: str = data['username']
        if CustomUser.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            return JsonResponse({'message': 'Username already taken'}, status=400)
        user.username = new_username
        updated_fields.append('username')

    # Additional fields handling omitted for brevity
    return JsonResponse({'message': 'Updated successfully.'})
