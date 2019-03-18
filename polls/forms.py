from django import forms
from .models import Question, Choice
from django.forms import modelformset_factory


class CreateQuestionView(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {'question_text': forms.TextInput(attrs={
            'placeholder': 'Enter question text here'
            })
        }


AddChoiceFormset = modelformset_factory(
    Choice,
    fields=('choice_text',),
    extra=3,
    widgets={'choice_text': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter choice text here'
        })
    }
)
