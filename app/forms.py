from django import forms
from .models import Quiz, Question


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description"]


class QuestionCreateForm(forms.Form):
    text = forms.CharField(
        label="Question text",
        widget=forms.Textarea(attrs={"rows": 3, "class": "border rounded w-full px-3 py-2"})
    )
    option1 = forms.CharField(
        label="Option 1",
        widget=forms.TextInput(attrs={"class": "border rounded w-full px-3 py-2"})
    )
    option2 = forms.CharField(
        label="Option 2",
        widget=forms.TextInput(attrs={"class": "border rounded w-full px-3 py-2"})
    )
    option3 = forms.CharField(
        label="Option 3",
        widget=forms.TextInput(attrs={"class": "border rounded w-full px-3 py-2"})
    )
    option4 = forms.CharField(
        label="Option 4",
        widget=forms.TextInput(attrs={"class": "border rounded w-full px-3 py-2"})
    )

    CORRECT_CHOICES = [
        ("1", "Option 1"),
        ("2", "Option 2"),
        ("3", "Option 3"),
        ("4", "Option 4"),
    ]

    correct_option = forms.ChoiceField(
        label="Correct option",
        choices=CORRECT_CHOICES,
        widget=forms.RadioSelect
    )
