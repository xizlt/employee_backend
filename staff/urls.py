from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views
from users.views import black_list_refresh_view

router = routers.DefaultRouter()
router.register(r'position', views.PositionViewSet)
router.register(r'filial', views.FilialViewSet)
router.register(r'account_type', views.AccountTypeViewSet)
router.register(r'account', views.AccountViewSet)
router.register(r'special', views.SpecialUsersViewSet)
router.register(r'employee', views.EmployeeViewSet)
router.register(r'status', views.StatusViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/blacklist/', black_list_refresh_view),
    path('api/v1/create_password', views.create_password),
    path('api/v1/create_template', views.create_template),
    path('api/v1/get_csv/temp/<str:temp>', views.get_csv_for_accounts),
    path('api/v1/', include(router.urls)),
]
