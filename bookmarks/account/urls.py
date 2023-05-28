# django built auth-views for changing, resetting password, and login-logout, register
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from .views import EditProfileView, RegisterView, UserDetailView, UserListView, DashboardView

app_name = 'account'
urlpatterns = [

    # path("", views.dashboard, name="dashboard"),
    # # login/logout urls
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #
    # # changing password urls
    # path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # # reset password urls
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # """
    # Yuqoridagi urls comment sabababi (login-logout-reset-change) shunga o'xshagan urls hammasi (django.contrib.auth.urls) dan keladi.
    # Shuning uchun o'shanga bo'lgan asosiy path ko'rsatilyapti. URL dispatcher o'sha yerdagi barcha urllar(biz yuqoridagi comment qilgan)larni topadi.
    #  Va, ularga ulangan viewlarni topib templatega(biz yaratgan templatelarga) yuboradi.
    # Template esa browser tomonidan foydalanuvchilarga ko'rsatilinadi.
    # """

    # django authentication urls for register

    path('', include('django.contrib.auth.urls')),
    path('', DashboardView.as_view(), name="dashboard"),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('edit/', EditProfileView.as_view(), name='edit'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', UserDetailView.as_view(), name='user_detail'),
]
