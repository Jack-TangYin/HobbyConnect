from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CustomUser, Hobby, FriendRequest, Friendship
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .utils import flatten_errors, get_filtered_and_sorted_users
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from datetime import date

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.csrf import csrf_exempt
from typing import Any, Dict
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.db import transaction
from django.db.models import Q


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
    
    
@login_required
@require_http_methods(["GET"])
def fetch_similar_users_api(request: HttpRequest) -> JsonResponse:
    """
    Returns a paginated JSON list of users who have hobbies in common
    with the request.user, filtered by an age range [min_age, max_age],
    sorted descending by number of common hobbies.
    """
    # Retrieve query parameters (with defaults).
    try:
        min_age = int(request.GET.get("min_age", 0))
    except (TypeError, ValueError):
        min_age = 0

    try:
        max_age = int(request.GET.get("max_age", 100))
    except (TypeError, ValueError):
        max_age = 100

    try:
        page = int(request.GET.get("page", 1))
    except (TypeError, ValueError):
        page = 1

    # Filter + sort the users by number of common hobbies
    users_queryset = get_filtered_and_sorted_users(request.user, min_age, max_age)

    # Paginate (10 users per page)
    paginator = Paginator(users_queryset, 10)
    paged_users = paginator.get_page(page)

    # Build the list of user data for JSON response
    users_list = []
    today = date.today()
    for u in paged_users:
        age = None
        if u.date_of_birth:
            age = (today - u.date_of_birth).days // 365
            
         # Check if there's already a Friendship
        is_friend = Friendship.objects.filter(
            Q(user1=request.user, user2=u) | Q(user1=u, user2=request.user)
        ).exists()

        # Check if there's a pending request in *either* direction
        has_pending_request = FriendRequest.objects.filter(
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

    response_data = {
        "results": users_list,
        "count": paginator.count,
        "current_page": paged_users.number,
        "total_pages": paginator.num_pages,
    }

    return JsonResponse(response_data)


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


@login_required
@require_http_methods(["PUT"])
def update_profile_api(request: HttpRequest) -> JsonResponse:
    """
    Update username, email, or date of birth.
    If a field is not provided or is blank, its current value remains unchanged.
    Before updating, checks are performed so that the new username or email 
    do not already exist for another user.
    """
    try:
        data: Dict[str, Any] = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user: CustomUser = request.user
    updated_fields: list[str] = []

    # Update username if provided
    if 'username' in data and data['username']:
        new_username: str = data['username']
        # Check if the new username exists for another user
        if CustomUser.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            return JsonResponse({'message': 'Username already taken'}, status=400)
        else:
            user.username = new_username
            updated_fields.append('username')

    # Update email if provided
    if 'email' in data and data['email']:
        new_email: str = data['email']
        # Check if the new email exists for another user
        if CustomUser.objects.filter(email=new_email).exclude(pk=user.pk).exists():
            return JsonResponse({'message': 'Email already taken'}, status=400)
        else:
            user.email = new_email
            updated_fields.append('email')

    # Update date of birth if provided and valid
    if 'dateOfBirth' in data and data['dateOfBirth']:
        parsed_date = parse_date(data['dateOfBirth'])
        if parsed_date:
            user.date_of_birth = parsed_date
            updated_fields.append('date of birth')
        else:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

    user.save()
    if updated_fields:
        message = f'Updated: {", ".join(updated_fields)}'
    else:
        message = 'No fields updated.'
    return JsonResponse({'message': message})


@login_required
@require_http_methods(["PUT"])
def change_password_api(request: HttpRequest) -> JsonResponse:
    """
    Update user password.
    Prevent changing to the same password.
    """
    try:
        data: Dict[str, Any] = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    
    if not old_password or not new_password:
        return JsonResponse({'message': 'All password fields are required'}, status=400)
    
    # Check if the new password is the same as the old password
    if old_password == new_password:
        return JsonResponse({'message': 'The new password must be different from the old password.'}, status=400)
    
    password_data: Dict[str, str] = {
        'old_password': old_password,
        'new_password1': new_password,
        'new_password2': new_password,
    }
    
    password_form = PasswordChangeForm(user=request.user, data=password_data)
    if password_form.is_valid():
        password_form.save()
        update_session_auth_hash(request, request.user)
        return JsonResponse({'message': 'Password changed successfully'})
    else:
        # Flatten the errors into a single string
        error_message = flatten_errors(password_form.errors)
        print(password_form.errors)
        return JsonResponse({'message': error_message}, status=400)


@login_required
@require_http_methods(["PUT"])
def update_hobbies_api(request: HttpRequest) -> JsonResponse:
    """
    Update user's hobbies.
    
    Expects a JSON payload with:
      - "action": "add" or "remove"
      - "hobby": (string) for adding, or
      - "hobby_id": (number) for removing.
    
    For 'add':  
      If the hobby already exists in the Hobby table, it is retrieved and added to the user's hobbies.
      If it does not exist, it is created, then added to the user's hobbies.
    
    For 'remove':  
      Only the association between the user and the hobby is removed;
      the hobby remains in the Hobby table.
    """
    try:
        data: Dict[str, Any] = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    action: str = data.get('action', '')
    user: CustomUser = request.user  # type: ignore

    if action == "add":
        hobby_names: list[str] = [h.strip() for h in data.get('hobby', '').split(',') if h.strip()]
        print(hobby_names)
        for hobby_name in hobby_names:
            if not hobby_name:
                return JsonResponse({'error': 'Hobby name required'}, status=400)
            # get_or_create returns a tuple of (object, created)
            hobby, _ = Hobby.objects.get_or_create(name=hobby_name)
            print("hobby:", hobby)
            user.hobbies.add(hobby)
            user.save()
        return JsonResponse({
            'message': f'Hobby "{", ".join(hobby_names)}" added',
            'hobbies': [h.as_dict() for h in user.hobbies.all()]
        })
    elif action == "remove":
        hobby_id = data.get('hobby_id')
        try:
            hobby = Hobby.objects.get(id=hobby_id)
        except Hobby.DoesNotExist:
            return JsonResponse({'error': 'Hobby not found'}, status=404)
        user.hobbies.remove(hobby)
        user.save()
        return JsonResponse({
            'message': f'Hobby "{hobby.name}" removed',
            'hobbies': [h.as_dict() for h in user.hobbies.all()]
        })
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)


@require_http_methods(["GET"])
def fetch_hobbies_api(request: HttpRequest) -> JsonResponse:
    """
    Returns a list of all hobbies available in the database.
    """
    hobbies = Hobby.objects.all()
    return JsonResponse({'hobbies': [h.as_dict() for h in hobbies]})


@login_required
@require_http_methods(["POST"])
def send_friend_request_api(request: HttpRequest) -> JsonResponse:
    """
    Send a friend request to another user.

    Expects a JSON payload with:
      - "receiver_id": ID of the user to send the friend request to.
    """
    try:
        data: Dict[str, Any] = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    receiver_id = data.get('receiver_id')
    if not receiver_id:
        return JsonResponse({'error': 'Receiver ID is required.'}, status=400)

    try:
        receiver = CustomUser.objects.get(id=receiver_id)
        if FriendRequest.objects.filter(sender=request.user, receiver=receiver, status='pending').exists():
            return JsonResponse({'error': 'Friend request already sent.'}, status=400)

        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        return JsonResponse({'message': 'Friend request sent successfully!'}, status=201)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)


@login_required
@require_http_methods(["GET"])
def fetch_friend_requests_api(request: HttpRequest) -> JsonResponse:
    """
    Fetch all pending friend requests for the logged-in user.

    Response:
      - List of pending friend requests.
    """
    friend_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
    requests_data = [
        {
            'id': req.id,
            'sender': req.sender.username,
            'timestamp': req.timestamp,
        } for req in friend_requests
    ]
    return JsonResponse({'friend_requests': requests_data})


@login_required
def handle_friend_request_api(request, pk):
    """
    Accept or reject a friend request.
    """
    try:
        data = json.loads(request.body)
        action = data.get("action")
        if action not in ["accept", "reject"]:
            return JsonResponse({"error": "Invalid action."}, status=400)

        friend_request = get_object_or_404(FriendRequest, id=pk, receiver=request.user)

        if action == "accept":
            with transaction.atomic():
                friend_request.status = "accepted"
                friend_request.save()
                # Create bidirectional friendship
                Friendship.objects.get_or_create(user1=request.user, user2=friend_request.sender)
                Friendship.objects.get_or_create(user1=friend_request.sender, user2=request.user)
            return JsonResponse({"message": "Friend request accepted successfully."}, status=200)

        elif action == "reject":
            friend_request.status = "rejected"
            friend_request.save()
            return JsonResponse({"message": "Friend request rejected."}, status=200)

    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Friend request not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
