from django.urls import path
from . import views

urlpatterns = [
    # blog 앱 내부의 경로를 지정할 부분
    path('', views.index), # localhost:8000/blog 경로, 경로를 호출하면 실행할 함수의 위치
    path('post-list', views.PostList.as_view()),
    path('about-me', views.about_me),
    path('<int:pk>', views.PostDetail.as_view()), # 동적으로 변경되는것은 <를 써서 자료형, 어느필드를 쓸것인지를 기입
    path('create-post/', views.PostCreate.as_view())
]