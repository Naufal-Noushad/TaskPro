from django import forms

from notes.models import Task

class TaskForm(forms.ModelForm):

    class Meta:

        model=Task

        # feilds="__all__"

        exclude=("created_date","status","updated_date")

        widgets={

            "title":forms.TextInput(attrs={"class":"form-control mb-3"}),

            "description":forms.Textarea(attrs={"class":"form-control mb-3"}),

            "due_date":forms.DateInput(attrs={"class":"form-control mb-3","type":"date"}),

            "category":forms.Select(attrs={"class":"form-control form-select mb-3"}),

            "user":forms.TextInput(attrs={"class":"form-control mb-3"})
        }

