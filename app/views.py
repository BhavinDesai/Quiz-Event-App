from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import QuizForm, QuestionCreateForm

# Create your views here.

def home(request):
    return render(request, "home.html")


def quiz_list(request):
    quizzes = Quiz.objects.all().order_by("-created_at")
    return render(request, "quiz_list.html", {"quizzes": quizzes})


def quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.prefetch_related("answers").all()
    return render(
        request,
        "quiz_attempt.html",
        {"quiz": quiz, "questions": questions},
    )


def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method != "POST":
        return redirect("app:quiz_attempt", quiz_id=quiz.id)

    user_name = request.POST.get("user_name", "").strip() or "Anonymous"

    questions = quiz.questions.prefetch_related("answers").all()

    score = 0
    submission = UserSubmission.objects.create(
        quiz=quiz,
        user_name=user_name,
        score=0,  # temporary, update after calculation
    )

    for question in questions:
        field_name = f"question_{question.id}"
        answer_id = request.POST.get(field_name)

        selected_answer = None
        is_correct = False

        if answer_id:
            try:
                selected_answer = Answer.objects.get(pk=answer_id, question=question)
                is_correct = selected_answer.is_correct
            except Answer.DoesNotExist:
                selected_answer = None

        if is_correct:
            score += 1

        UserAnswer.objects.create(
            submission=submission,
            question=question,
            answer=selected_answer,
            is_correct=is_correct,
        )

    submission.score = score
    submission.save()

    return redirect("app:quiz_result", submission_id=submission.id)


def quiz_result(request, submission_id):
    submission = get_object_or_404(
        UserSubmission.objects.select_related("quiz").prefetch_related("answers__question"),
        pk=submission_id,
    )
    total_questions = submission.quiz.questions.count()
    return render(
        request,
        "quiz_result.html",
        {
            "submission": submission,
            "total_questions": total_questions,
        },
    )


def event_list(request):
    today = timezone.localdate()
    events = Event.objects.filter(date__gte=today).order_by("date")
    return render(request, "events.html", {"events": events})


def quiz_dashboard(request):
    """Simple dashboard listing all quizzes with manage links."""
    quizzes = Quiz.objects.all().order_by("-created_at")
    return render(request, "quiz_dashboard.html", {"quizzes": quizzes})


def quiz_create(request):
    """Create a new quiz."""
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            # After creating quiz, go to manage questions for this quiz
            return redirect("app:manage_questions", quiz_id=quiz.id)
    else:
        form = QuizForm()

    return render(request, "quiz_form.html", {"form": form})


def manage_questions(request, quiz_id):
    """View all questions for a quiz and see a link to add more."""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all().prefetch_related("answers")
    return render(
        request,
        "manage_questions.html",
        {"quiz": quiz, "questions": questions},
    )


def add_question(request, quiz_id):
    """Add a new single-choice question with 4 options."""
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == "POST":
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            # Create Question
            question = Question.objects.create(
                quiz=quiz,
                text=form.cleaned_data["text"],
                question_type=Question.SINGLE_CHOICE,
            )

            # Create Answers
            option_texts = [
                form.cleaned_data["option1"],
                form.cleaned_data["option2"],
                form.cleaned_data["option3"],
                form.cleaned_data["option4"],
            ]
            correct = form.cleaned_data["correct_option"]  # "1" / "2" / "3" / "4"
            for index, text in enumerate(option_texts, start=1):
                Answer.objects.create(
                    question=question,
                    text=text,
                    is_correct=(str(index) == correct),
                )

            return redirect("app:manage_questions", quiz_id=quiz.id)
    else:
        form = QuestionCreateForm()

    return render(
        request,
        "question_form.html",
        {"quiz": quiz, "form": form},
    )

