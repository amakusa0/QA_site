from django import forms

class QuestionForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    text = forms.CharField(max_length=1000, widget=forms.Textarea, required=True)

class AnswerForm(forms.Form):
    text = forms.CharField(max_length=1000, widget=forms.Textarea, required=True)


