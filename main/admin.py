from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'company', 'inn', 'phone', 'date_joined', 'is_staff', 'is_active')
    list_filter = ('email', 'company', 'inn', 'phone', 'date_joined', 'is_staff', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('email', 'company', 'inn', 'phone')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'company', 'inn', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'company', 'inn', 'phone', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'company', 'inn', 'phone')
    ordering = ('email', 'company')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'time_update', 'is_published', 'author_id')
    list_display_links = ('title',)
    search_fields = ('title', 'time_create', 'time_update', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
