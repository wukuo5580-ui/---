from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="user"
    )
    bio = models.TextField("profile", blank=True)
    birth_date = models.DateField("Date Birthday", null=True, blank=True)
    is_author = models.BooleanField("Is the author?", default=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profile" #复数名称

    def __str__(self):
        return f"{self.user.username} 's profile"


class Category(models.Model):
    name = models.CharField("Class", max_length=100)
    slug = models.SlugField("URL", max_length=100, unique=True) #网址名称
    icon = models.CharField("icon", max_length=10, default="📝")
    # description = models.TextField("分类描述", blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField("Title", max_length=150)
    content = models.TextField("Tect")

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,#分类删除，帖子也删除
        related_name="posts",
        verbose_name="category"
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="author"
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        blank=True,
        verbose_name="liked Users"
    )

    image_url = models.URLField("Image URL", blank=True) #图片链接
    is_published = models.BooleanField("Published", default=True) #发布
    created_at = models.DateTimeField("Created At", auto_now_add=True) #创建时间

    class Meta:
        verbose_name = "Posts"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


#获取用户模型
User = get_user_model()
#自动创建用户资料
@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)