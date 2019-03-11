from django import forms
from .models import Question, Choice


class CreateQuestionView(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


class AddChoiceView(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
