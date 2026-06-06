from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
            "image_url",
            "is_published",
        ]
        #创建帖子初始样式
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Please enter the post title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Please enter the post content"
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "image_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Optional"
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "checkbox"
            }),
        }

    def clean_title(self):

        title = self.cleaned_data["title"]

        #标题至少两个字
        if len(title.strip()) < 2:
            raise forms.ValidationError("The title must be at least 2 characters long。")

        return title

    def clean_content(self):

        content = self.cleaned_data["content"]

        #内容10个字
        if len(content.strip()) < 10:
            raise forms.ValidationError("The post content must be at least 10 characters long")

        return content