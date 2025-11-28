from django.db import models

# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    SINGLE_CHOICE = "single"
    MULTIPLE_CHOICE = "multiple"

    QUESTION_TYPES = [
        (SINGLE_CHOICE, "Single choice"),
        (MULTIPLE_CHOICE, "Multiple choice"),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(
        max_length=20, choices=QUESTION_TYPES, default=SINGLE_CHOICE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"


class UserSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="submissions")
    user_name = models.CharField(max_length=100)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.quiz.title} ({self.score})"


class UserAnswer(models.Model):
    submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.submission.user_name} - {self.question.text[:30]}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} @ {self.location}"
