from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.base import TemplateView
from tempfile import template

# Create your views here.
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import  loader
from unicodedata import category
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.signing import BadSignature
from django.core.paginator import Paginator
from django.db.models import Q
from .models import SP, SubRubric
from .models import Category
from .models import News
from .forms import SearchForm
from .forms import SPForm
from .models import AdvUser
from .forms import ProfileEditForm
from .forms import RegisterForm
from .utilities import signer


class SPLoginView(LoginView):
     template_name = 'sportsman/login.html'

class SPCreateView(CreateView):
     template_name = 'sportsman/sp_create.html'
     form_class = SPForm
     success_url = reverse_lazy('sport')

class SPLogoutView(LogoutView):
     pass

@login_required()
def profile(request):
     newss = News.objects.filter(author=request.user.pk)
     context = {'newss': newss}
     return render(request, 'sportsman/profile.html')

class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
     model = AdvUser
     template_name = 'sportsman/profile_edit.html'
     form_class = ProfileEditForm
     success_url = reverse_lazy('profile')
     success_message = 'Данные пользователя изменены'

     def setup(self, request, *args, **kwargs):
         self.user_id = request.user.pk
         return super().setup(request, *args, **kwargs)

     def get_object(self, queryset = None):
          if not queryset:
               queryset = self.get_queryset()
          return get_object_or_404(queryset, pk=self.user_id)

class PasswordEditView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
     template_name = 'sportsman/password_edit.html'
     success_url = reverse_lazy('profile')
     success_message = 'Пароль пользователя изменен'

class RegisterView(CreateView):
     model = AdvUser
     template_name = 'sportsman/register.html'
     form_class = RegisterForm
     success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
     template_name = 'sportsman/register_done.html'

class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
     model = AdvUser
     template_name = 'sportsman/profile_delete.html'
     success_url = reverse_lazy('home')
     success_message = 'Пользователь удален'

     def setup(self, request, *args, **kwargs):
          self.user_id = request.user.pk
          return super().setup(request, *args, **kwargs)

     def post(self, request, *args, **kwargs):
          logout(request)
          return super().post(request, *args, **kwargs)

     def get_object(self, queryset=None):
          if not queryset:
               queryset = self.get_queryset()
          return get_object_or_404(queryset, pk=self.user_id)


def user_activate (request, sign):
     try:
          username = signer.unsign(sign)
     except BadSignature:
          return render(request, 'sportsman/activation_failed.html')
     user = get_object_or_404(AdvUser, username=username)
     if user.is_activated:
          template = 'sportsman/activation_done_earlier.html'
     else:
          template = 'sportsman/activation_done.html'
          user.is_active = True
          user.is_activated = True
          user.save()
     return render(request, template)


def get_sport_data(self, **kwargs):
     context = super().get_sport_data(**kwargs)
     context['categorys'] = Category.objects.all()
     return context



def category_sps(request, category_id):
     sps = SP.objects.filter (category=category_id)
     categorys = Category.objects.all()
     current_category = Category.objects.get(pk=category_id)
     context = {'sps': sps, 'categorys': categorys, 'current_category':  current_category}
     return render(request, 'sportsman/category_sps.html', context)


def sport(request) :
     template = loader.get_template('sportsman/sport.html')
     sps = SP.objects.all()
     paginator = Paginator(sps, 2)
     if 'page' in request.GET:
          page_num = request.GET['page']
     else:
          page_num = 1
     page = paginator.get_page(page_num)
     categorys = Category.objects.all()
     context = {'categorys': categorys, 'page': page, 'sps': sps}
     return render(request, 'sportsman/sport.html', context)
#     return HttpResponse (template.render (context, request))

def index(request):
     template = loader.get_template('couches/couches.html')
     return render(request, 'couches/couches.html')
#     return  HttpResponse ("Тренера")

def compet(request):
     template = loader.get_template('competition/compet.html')
     return render(request, 'competition/compet.html')
#     return  HttpResponse ("Соревнования")

#def rubric_newss(request, pk):
#     pass

def home(request):
     newss = News.objects.filter(is_active=True) .select_related('rubric')
#     newss = News.objects.filter(is_active=True, rubric=pk)
     if 'keyword' in request.GET:
          keyword = request.GET['keyword']
          q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
          newss =newss.filter(q)
     else:
          keyword = ''
     form = SearchForm(initial={'keyword':keyword})
     paginator = Paginator(newss, 2)
     if 'page' in request.GET:
          page_num = request.GET['page']
     else:
          page_num = 1
     page = paginator.get_page(page_num)
     context = {'page': page, 'newss': page.object_list, 'form':form}
     template = loader.get_template('site/site.html')
     return render(request, 'site/site.html', context)

def rubric_newss(request, pk):
     rubric = get_object_or_404(SubRubric, pk=pk)
     newss = News.objects.filter(is_active=True, rubric=pk)
     if 'keyword' in request.GET:
          keyword = request.GET['keyword']
          q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
          newss =newss.filter(q)
     else:
          keyword = ''
     form = SearchForm(initial={'keyword':keyword})
     paginator = Paginator(newss, 2)
     if 'page' in request.GET:
          page_num = request.GET['page']
     else:
          page_num = 1
     page = paginator.get_page(page_num)
     context = {'rubric': rubric ,'page': page, 'newss': page.object_list, 'form':form}
     return render(request, 'site/rubric_news.html', context)

def news_detail(request, rubric_pk, pk):
     news = get_object_or_404(News, pk=pk)
     ais = news.newsimage_set.all()
     context = {'news': news, 'ais': ais}
     return render(request, 'site/news_detail.html', context)

def other_page(request, page):
     try:
          template = get_template('sportsman/'+ page + '.html')
     except TemplateDoesNotExist:
          raise Http404
     return HttpResponse(template.render(request=request))

def about(request):
    template = loader.get_template('sportsman/about.html')
    return render(request, 'sportsman/about.html')