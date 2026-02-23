from django.contrib.auth import login
from django.views.generic import CreateView

CreateView
from django.urls import path, include
from .views import sport, category_sps, SPCreateView, index, compet, home, about
from .views import SPLoginView, profile, SPLogoutView, PasswordEditView, RegisterView, RegisterDoneView
from .views import ProfileEditView, user_activate
from .views import ProfileDeleteView
from .views import rubric_newss
from .views import news_detail

urlpatterns = [
    path('', home, name='home'),
    path('accounts/activate/<str:sign>/', user_activate,name='activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', SPLogoutView.as_view(), name='logout'),
    path('accounts/login/', SPLoginView.as_view(), name='login'),
    path('accounts/password/edit', PasswordEditView.as_view(), name='password_edit'),
    path('account/profile/delete', ProfileDeleteView.as_view(), name='profile_delete'),
    path('accounts/profile/edit', ProfileEditView.as_view(), name='profile_edit'),
    path('accounts/profile/', profile, name='profile'),
    path('about/', about, name='about'),

    path('<int:rubric_pk>/<int:pk>/', news_detail, name='news_detail'),
    path('<int:pk>/', rubric_newss, name='rubric_newss'),

    path('main/', index, name='index'),

    path('add/', SPCreateView.as_view(), name='add'),

#    path('main/', include('main.urls')),
    path('compet/', compet, name='compet'),
    path('sport/', sport, name='sport'),
    path('sport/<int:category_id>/', category_sps, name='category_sps'),




]
