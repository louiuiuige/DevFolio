from django.contrib import admin

from .models import Category, Project, ProjectImage, Review, StudentProfile, Technology, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'role', 'email', 'course')
    list_filter = ('role', 'course')
    search_fields = ('username', 'full_name', 'email', 'student_id')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'skills')
    search_fields = ('user__username', 'department')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'status', 'average_rating', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'summary', 'owner__username')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('project__title', 'reviewer__username', 'comment')
