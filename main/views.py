import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from .forms import RegisterUserForm
from .models import *


def index(request):
    posts = Article.objects.order_by('publication_date').reverse().all()

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj
    }
    return render(request, 'main/index.html', context=context)


def article(request, id):
    article_id = id
    if request.method == 'POST':
        user = request.user
        date_posted = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        Comment.objects.create(article_id=article_id, parent_id=request.POST['reply_id'], comments_author=user.username, comment_text=request.POST['comment'], user_id=user.pk, date_posted=date_posted)
        return redirect('article', id)

    post = Article.objects.get(id=article_id)
    all_comments = Comment.objects.filter(article_id=article_id).order_by('parent_id', 'date_posted').all()
    other_article = Article.objects.exclude(id=article_id).order_by('?').all()[:2]
    comments_sort = []
    count = 0
    for comment in all_comments:
        if comment.parent_id == 0:
            comments_sort.append([])
            comments_sort[count].append(comment)
            comments_child = Comment.objects.filter(parent_id=comment.id).order_by('date_posted').all()
            for comment_child in comments_child:
                comments_sort[count].append(comment_child)
        count += 1
    post.text = post.text.replace('\n', '</p><p>')
    context = {
        'post': post,
        'comments': comments_sort,
        'other_article': other_article,
        'comments_length': len(all_comments)
    }
    return render(request, 'main/article_page.html', context=context)


def profile_edit(request):
    user = request.user
    form = RegisterUserForm(request.POST or None, initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    })

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']

        user.save()
        return redirect('profile')

    context = {
        "form": form
    }

    return render(request, "main/settings.html", context=context)


def profile(request):
    user = request.user
    if not user.username:
        return redirect('auth')
    context = {
        'user': user
    }

    return render(request, 'main/profile.html', context=context)


def auth(request):
    return render(request, 'main/auth.html')


def register(request):
    return render(request, 'main/register.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('auth')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/auth.html'

    def get_success_url(self):
        return reverse_lazy('home')
