from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Tag, Comment
from django.views.generic import ListView, DetailView, CreateView
from django.utils.text import slugify


from django.views.decorators.http import require_POST
from django.contrib.auth import logout as auth_logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login # authenticate : 인가, login : 인증 담당
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django.contrib import messages # 예외나 상황에 대한 메시지 처리
from django.contrib.auth.mixins import LoginRequiredMixin

# Mixin라는 부가 기능들을 확인하기 위해 다중상속으로 주 기능을 확장하는 별도의 클래스
# 주 기능을 가진 클래스 앞에 작성

class PostCreate(LoginRequiredMixin, CreateView) :
    model = Post
    fields = ["title", "content", "head_image", "file_upload"]

    # CreateView가 내장한 함수 - 오버라이딩
    # tag는 참조관계이므로 Tag 테이블에 등록된 태그만 쓸 수 있는 상황
    # 임의로 방문자가 form에 Tag를 달아서 보내도록 form_valid()에 결과를
    # 저장된 포스트로 돌아오도록
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_active):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()   # 책; 독후감, 작가명

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(tag_name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tag.add(tag)

            return response

        else:
                return redirect('/blog/')

class PostList(ListView):   # post_list.html, post-list
    model = Post 
    # template_name = 'blog/index.html' 
    ordering = '-pk' 
    context_object_name = 'post_list'

def index(request): # 함수를 만들고, 그 함수를 도메인 주소 뒤에 달아서 호출하는 구조
    posts = Post.objects.all()
    return render(
        request,
        'blog/index.html', {
            'posts':posts, 'my_list': ["apple", "banana", "cherry"], 'my_text': "첫번째 줄 \n 두번째 줄", 'content' : '<img src="data/jjangu.jpg" / >'
        }
    )# 없는 index.html을 호출하고 있음

def about_me(request): # 함수를 만들고, 그 함수를 도메인 주소 뒤에 달아서 호출하는 구조
    return render(
        request,
        'blog/about_me.html'
    )

class PostDetail(DetailView): # 함수를 만들고, 그 함수를 도메인 주소 뒤에 달아서 호출하는 구조
    model = Post 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = '임의로 작성한 새로운 변수'
        print(context['now'])
        return context


@login_required
def user_delete(request):
    if request.user.is_authenticated:
        request.user.delete()

        auth_logout(request)

        return redirect('blog_app:about_me')