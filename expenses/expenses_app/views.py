from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import ExpenseIncome
from .serializers import UserRegisterSerializer, ExpenseIncomeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class IsOwnerOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user == request.user

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    throttle_scope = 'anon'  # Anonymous users have lower rate limits

class ExpenseIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseIncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]
    
    # Filtering, Searching, and Ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'tax_type', 'created_at', 'updated_at']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'amount', 'title']
    ordering = ['-created_at']
    
    # Throttling
    throttle_scope = 'user'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ExpenseIncome.objects.all().order_by('-created_at')
        return ExpenseIncome.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        # Always fetch from all objects so we can check permissions
        queryset = ExpenseIncome.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        obj = queryset.get(**{self.lookup_field: lookup_value})
        self.check_object_permissions(self.request, obj)
        return obj
