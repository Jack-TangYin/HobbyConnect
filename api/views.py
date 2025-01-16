from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .utils import get_filtered_and_sorted_users
from django.contrib.auth.decorators import login_required
import json

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.csrf import csrf_exempt

# def main_spa(request: HttpRequest) -> HttpResponse:
#     return render(request, 'api/spa/index.html', {})

@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({'message': 'CSRF cookie set'})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'api/register.html'
    # success_url = reverse_lazy('home')
    success_url = 'http://localhost:5173'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after successful signup
        CustomUser = self.object
        login(self.request, CustomUser)
        return response
    
    
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'api/profile.html'


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'api/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Handle password change if needed
        if 'old_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                # Important: keep user logged in after password change
                update_session_auth_hash(request, request.user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(user=self.request.user)
        return context
    
class SimilarUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        min_age = int(request.GET.get('min_age', 0))
        max_age = int(request.GET.get('max_age', 100))

        users = get_filtered_and_sorted_users(user, min_age, max_age)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(users, request)
        return paginator.get_paginated_response({
            'users': [
                {
                    'id': u.id,
                    'username': u.username,
                    'common_hobbies': u.common_hobbies,
                    'age': (date.today() - u.date_of_birth).days // 365,
                } for u in result_page
            ]
        })


def logout_view(request):
    """
    API endpoint for logging the user out
    """
    logout(request)
    return JsonResponse({'message': 'Logged out'})


def user_api(request: HttpRequest) -> HttpResponse:
    """
    API endpoint for the collection of users
    
    Supports GET methods
    """
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    
    
    if request.method == 'GET':
        user_data = request.user.as_dict()
        return JsonResponse(user_data)
    
    # Return a 405 Method Not Allowed response for all other request methods
    return HttpResponse(status=405)


def users_api(request, user_id):
    """
    API endpoint for handling operations on a single user
    
    Supports PUT, and DELETE methods
    """
    
    user = CustomUser.objects.get(id=user_id)

    if request.method == 'PUT':
        # Update user attributes and save changes
        PUT = json.loads(request.body)
        user.name = PUT['name']
        user.save()
        return JsonResponse(user.as_dict())

    if request.method == 'DELETE':
        # Delete the user
        user.delete()
        return JsonResponse({})

    # Default response is the user data in JSON format
    return JsonResponse(user.as_dict())
