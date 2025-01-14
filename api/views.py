from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth import login
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
import json

# def main_spa(request: HttpRequest) -> HttpResponse:
#     return render(request, 'api/spa/index.html', {})

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