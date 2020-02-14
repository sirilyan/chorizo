from django.contrib import admin

# Register your models here.

from chorizo.models import Chore

class ChoreAdmin(admin.ModelAdmin):
    fields = [ 'assigner', 'assignee', 'chore_type', 'due_date', 'reward', 'daily_penalty' ]

admin.site.register(Chore)

