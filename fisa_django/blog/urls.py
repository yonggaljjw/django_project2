from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    # blog 앱 내부의 경로를 지정할 부분
    # path('', views.index), # localhost:8000/blog 경로, 경로를 호출하면 실행할 함수의 위치
    path('post-list', views.PostList.as_view(paginate_by=5), name = 'post_list'),
    path('', views.about_me, name='about_me'),
    path('<int:pk>', views.PostDetail.as_view(), name="revise"), # <자료형:필드명> 
    path('create-post/', views.PostCreate.as_view(), name="create"), # blog_app:create
    path('user-delete/', views.user_delete, name='user_delete'),
    # update는 이미 있는 글을 수정하므로 글번호가 필요합니다.
    path('edit-post/<int:pk>', views.PostUpdate.as_view(), name = 'update'),
    path('delete-post/<int:pk>', views.PostDelete.as_view(), name = 'delete'),
    
    # 겉운 tag를 가진 글끼리 게시판에 보여주기
    path('tag/<str:slug>', views.tag_posts, name="tag"),


    # 댓글 조회 -> post-detail.html 안에서 동작하도록
    # 댓글 작성
    path('<int:pk>/create-comment', views.create_comment, name = 'create_comment'),
    # 댓글 수정
    path('update-comment/<int:pk>', views.CommentUpdate.as_view(), name='update_comment'),
    # 댓글 삭제
    path('delete-comment/<int:pk>', views.delete_comment, name='delete_comment'),

    # 검색을 위한 주소
    path("search/<str:q>/", views.PostSearch.as_view(), name="search")
]