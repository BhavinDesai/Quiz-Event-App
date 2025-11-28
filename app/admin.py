from django.contrib import admin
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event

# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ("text", "quiz", "question_type")


class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)


class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location")
    list_filter = ("date", "location")


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(UserSubmission)
admin.site.register(UserAnswer)
admin.site.register(Event, EventAdmin)
