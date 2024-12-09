# scores/forms.py

from django import forms

class AddScoreForm(forms.Form):
    id = forms.IntegerField(label='ID', min_value=1)
    teams_status = forms.CharField(label='Teams and Status', max_length=255)
    score1 = forms.IntegerField(label='Score 1', min_value=0)
    score2 = forms.IntegerField(label='Score 2', min_value=0)

class EditScoreForm(forms.Form):
    teams_status = forms.CharField(label='Teams and Status', max_length=255)
    score1 = forms.IntegerField(label='Score 1', min_value=0)
    score2 = forms.IntegerField(label='Score 2', min_value=0)


class EditScoreForm(forms.Form):
    teams_status = forms.CharField(label='Teams and Status', max_length=255)
    score1 = forms.IntegerField(label='Score 1', min_value=0)
    score2 = forms.IntegerField(label='Score 2', min_value=0)

class DeleteScoreForm(forms.Form):
    delete_id = forms.IntegerField(widget=forms.HiddenInput())

class DeleteAllScoresForm(forms.Form):
    confirm = forms.BooleanField(
        label='I confirm that I want to delete all scores.',
        required=True
    )