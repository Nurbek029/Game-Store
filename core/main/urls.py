from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('contacts', views.contacts_view, name='contacts'),

    path('game_product/<int:game_product_id>/', views.game_product_detail_view, name='game_product_detail'),
    path('game_product/create/', views.game_product_create_view, name='game_product_create'),
    path('game_product/update/<int:game_product_id>/', views.game_product_update_view, name='game_product_update'),
    path('game_product/<int:game_product_id>/delete/', views.game_product_delete_view, name='game_product_delete'),

    path('rating/create/<int:game_product_id>/', views.rating_create_view, name='rating_create'),
    path('rating-answer/create/<int:rating_id>/', views.rating_answer_create_view, name='rating_answer_create'),

    path('profile/', views.user_profile_view, name='user_profile'),
    
    path('payment_requests/', views.payment_request_list_view, name='payment_requests'),
    path('payment_request/<int:payment_request_id>/update/', views.payment_request_update_status,
         name='payment_request_update_status'),
    path('payments/', views.payment_list_view, name='payments'),

    path('game_product/<int:game_product_id>/payment/create/', views.game_product_payment_create_view,
         name='game_product_payment_create'),

    path('catalog/', views.game_product_list_view, name='catalog')
]
