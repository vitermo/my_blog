from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论
    path('post-comment/<int:blog_id>', views.post_comment, name='post_comment'),
    path('post-comment/<int:blog_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
]
