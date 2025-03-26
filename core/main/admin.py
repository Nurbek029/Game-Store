from django.contrib import admin
from .models import Category, Image, Game_Product, Rating, RatingAnswer, PaymentMethod, PaymentRequest

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Game_Product)
admin.site.register(Rating)
admin.site.register(RatingAnswer)
admin.site.register(PaymentMethod)
admin.site.register(PaymentRequest)

