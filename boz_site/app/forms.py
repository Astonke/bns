from django import forms

class GameForm(forms.Form):
    Game_id = forms.CharField(max_length=10, required=True)
    match = forms.CharField(max_length=100)
    home_odd = forms.DecimalField(max_digits=5, decimal_places=2)
    draw_odd = forms.DecimalField(max_digits=5, decimal_places=2)
    away_odd = forms.DecimalField(max_digits=5, decimal_places=2)
    gg = forms.DecimalField(max_digits=5, decimal_places=2)
    ngg = forms.DecimalField(max_digits=5, decimal_places=2)
    o1_5 = forms.DecimalField(max_digits=5, decimal_places=2)
    u1_5 = forms.DecimalField(max_digits=5, decimal_places=2)
    o2_5 = forms.DecimalField(max_digits=5, decimal_places=2)
    u2_5 = forms.DecimalField(max_digits=5, decimal_places=2)
    date = forms.TimeField()
