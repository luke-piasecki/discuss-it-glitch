from django.urls import path, include

from . import views
import chat.urls

urlpatterns = [

    # login-section
    path("logout/", views.logout_view, name="logout"),
    path('signup/', views.SignUp.as_view(), name='sign_up'),
    path('login/', views.login_view, name='login'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', views.home_view, name = 'home'),
    path('politics/', views.people_view, name = 'form1'),
    path('topics/', views.topic_view, name = 'form2'),
    path('account/', views.account_view, name = 'account'),

]
