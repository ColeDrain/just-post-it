from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
	path('', views.PostListView.as_view(), name='post-list'),
	path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
	path('new_post/', views.PostCreateView.as_view(), name='post-create'),
	path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
	path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
	path('signup/', views.signup, name='signup'),
	path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
	path('activate/<uidb64>/<token>/', views.activate, name='activate'),
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),

	path('reset/',
    auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ),
    name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
        name='password_change_done'),
]