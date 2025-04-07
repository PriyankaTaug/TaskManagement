from django.contrib import admin
from .models import CustomUser, Task
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'created_by', 'status', 'worked_hours', 'created_at']
    list_filter = ['status', 'created_by']
    search_fields = ['title', 'assigned_to__username']
