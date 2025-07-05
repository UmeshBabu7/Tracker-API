from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView, ExpenseIncomeViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'expenses', ExpenseIncomeViewSet, basename='expenseincome')

urlpatterns = [
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
] 
 