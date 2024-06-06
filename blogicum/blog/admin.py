from django.contrib import admin

from blog.models import Category
from blog.models import Location
from blog.models import Post


class LocationInline(admin.TabularInline):
    model = Post


class CategoryInline(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (CategoryInline,)
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)


class LocationAdmin(admin.ModelAdmin):
    inlines = (LocationInline,)
    list_display = ('name', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published', 'author', 'location', 'category')


admin.site.empty_value_display = 'Не задано'
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
