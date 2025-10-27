from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
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
        cache_key = f"expenses_user_{user.id}"
        
        # Try to get from cache first
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset
            
        # If not in cache, fetch from database
        if user.is_superuser:
            queryset = ExpenseIncome.objects.all().order_by('-created_at')
        else:
            queryset = ExpenseIncome.objects.filter(user=user).order_by('-created_at')
        
        # Cache the queryset for 15 minutes
        cache.set(cache_key, queryset, 60 * 15)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Clear cache after creating new expense
        cache_key = f"expenses_user_{self.request.user.id}"
        cache.delete(cache_key)

    def perform_update(self, serializer):
        serializer.save()
        # Clear cache after updating expense
        cache_key = f"expenses_user_{self.request.user.id}"
        cache.delete(cache_key)

    def perform_destroy(self, instance):
        instance.delete()
        # Clear cache after deleting expense
        cache_key = f"expenses_user_{self.request.user.id}"
        cache.delete(cache_key)

    def get_object(self):
        # Always fetch from all objects so we can check permissions
        queryset = ExpenseIncome.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        obj = queryset.get(**{self.lookup_field: lookup_value})
        self.check_object_permissions(self.request, obj)
        return obj
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    @method_decorator(vary_on_headers('Authorization'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
