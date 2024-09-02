from .models import Comment
from django import forms

class CommentForm(forms.ModelForm) :
    class Meta : # 추가적인 정보들을 달아서 보낼 때 사용하는 클래스    
        model = Comment
        fields = ['content']