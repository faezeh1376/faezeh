from django.contrib import admin

from .models import POSTS
from .models import Category
from .models import Comments
from .models import Grouping
from .models import SabadKharid
# Register your models here.

admin.site.register(Grouping)
admin.site.register(SabadKharid)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("name",)

@admin.register(POSTS)
class POSTSAdmin(admin.ModelAdmin):
    list_filter = ("title", "price", )
    list_display = ("title", "price", )

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "post", "create_date", "status",)