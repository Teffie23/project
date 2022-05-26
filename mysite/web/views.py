from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from .forms import *
from .utils import DataMixin
from robokassa.forms import RobokassaForm
from django.contrib.auth.decorators import login_required


# Класс представления свободных шкафов
class home(DataMixin, ListView):
    model = scaf
    template_name = 'web/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return scaf.objects.filter(is_blocks=True)


class showpost(DataMixin, DetailView):
    model = scaf
    template_name = 'web/post.html'
    slug_url_kwarg = 'scafs_slug'
    context_object_name = 'posts'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['posts'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return scaf.objects.filter(is_blocks=True)


# Класс представления категорий(тренажёров)
class traiiner(DataMixin, ListView):
    model = trainer
    template_name = 'web/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return user.objects.filter(trainer__slug=self.kwargs['train_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].trainer_id))
        context = dict(list(context.items()) + list(c_def.items()))


class Think(LoginRequiredMixin, DataMixin, CreateView):
    form_class = thinkForm
    template_name = 'web/think.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Запись')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# класс регистрации
class registerUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'web/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        users = form.save()
        print(users.username)
        # создание пользователя
        user.objects.create(name=users.username, slug=users.username.upper(), num_scaf=None, trainer=None)
        login(self.request, users)
        return redirect('home')


def think(request):
    form = thinkForm()
    if request.method == 'POST':
        form = thinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = thinkForm()
    return render(request, 'web/think.html', {'form': form})


# функция для выхода из прилжения
def logout_user(request):
    p = user.objects.filter(slug=request.user.username.upper())[0].num_scaf_id
    user.objects.filter(slug=request.user.username.upper()).update(num_scaf=None,trainer=None)
    scaf.objects.filter(id=p).update(is_blocks=True)
    logout(request)
    return redirect('login')


# класс авторизации на сайте
class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'web/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


# функция предоставляющая возможность забронировать шкафчик
def test(request, scafs_slug):
    if request.method == 'POST':
        form = fooform(request.POST)
        if form.is_valid():
            val = form.cleaned_data.get('bth')
            scaf.objects.filter(slug=scafs_slug).update(is_blocks=False)
            p = scaf.objects.get(slug=scafs_slug).pk
            user.objects.filter(slug=request.user.username.upper()).update(num_scaf=p)
            return redirect('other')
    else:
        form = fooform()
    return render(request, 'web/post.html', locals())


# функция представления 'о сайте'
def other(request):
    return render(request, 'web/other.html')


# функция представления 'обратная связь'
def reverse_top(request):
    return render(request, 'web/other.html')


# функция для предоставления оплаты за тариф
@login_required
def bye(request, order_id):
    order = get_object_or_404(tarif, pk=order_id)
    form = RobokassaForm(initial={
        'OutSum': order.total,
        'InvId': order.id,
        'Desc': order.name_tarif,
        'Email': request.user.email
    })
    return render(request, 'web/bye.html', {'form': form})


# функция для представления выбора пользователю тренажёра
def tray(request, train_slug):
    l = trainer.objects.get(slug=train_slug).pk
    user.objects.filter(slug=request.user.username.upper()).update(trainer=l)
    return render(request, 'web/train.html')
