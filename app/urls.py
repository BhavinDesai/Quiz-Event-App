from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.home, name="home"),
    path("quizzes/", views.quiz_list, name="quiz_list"),
    path("quiz/<int:quiz_id>/", views.quiz_attempt, name="quiz_attempt"),
    path(
        "quiz/<int:quiz_id>/submit/",
        views.quiz_submit,
        name="quiz_submit",
    ),
    path(
        "result/<int:submission_id>/",
        views.quiz_result,
        name="quiz_result",
    ),
    path("events/", views.event_list, name="event_list"),



    path("dashboard/", views.quiz_dashboard, name="quiz_dashboard"),
    path("dashboard/quiz/add/", views.quiz_create, name="quiz_create"),
    path(
        "dashboard/quiz/<int:quiz_id>/questions/",
        views.manage_questions,
        name="manage_questions",
    ),
    path(
        "dashboard/quiz/<int:quiz_id>/questions/add/",
        views.add_question,
        name="add_question",
    ),
]
