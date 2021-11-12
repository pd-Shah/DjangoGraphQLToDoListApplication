from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoModelAdmin(admin.ModelAdmin):
    pass
