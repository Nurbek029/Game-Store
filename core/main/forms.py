from django import forms
from .models import Game_Product

class GameProductCreateForm(forms.ModelForm):
    class Meta:
        model = Game_Product
        fields = (
            'title',
            'category',
            'main_image',
            'images',
            'description',
            'price',
        )

class GameProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Game_Product
        fields = (
            'title',
            'category',
            'main_image',
            'images',
            'description',
            'price',
        )
