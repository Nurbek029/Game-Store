from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib import messages
from django.db.models import Avg, Sum
from django.core.paginator import Paginator

from .forms import GameProductCreateForm, GameProductUpdateForm
from .filters import GameProductListFilter
from .models import Game_Product, Rating, RatingAnswer, PaymentMethod, PaymentRequest, Category, Payment


def index_view(request):
    game_products = Game_Product.objects.filter(is_active=True)

    return render(request, 'main/index.html', {"game_products": game_products})

def contacts_view(request):
    return render(request, 'main/contact.html')

def game_product_detail_view(request, game_product_id):
    game_product = get_object_or_404(Game_Product, id=game_product_id)
    game_product_update_form = GameProductUpdateForm(instance=game_product)
    game_product_comments = Rating.objects.filter(game_product=game_product)

    game_products_with_ratings = []

    rating_avg = game_product_comments.aggregate(Avg('count'))['count__avg']
    similar_game_products = Game_Product.objects.filter(category=game_product.category).exclude(id=game_product.id)

    game_products_with_ratings.append({
        'product': game_product,
        'rating_avg': rating_avg
    })

    return render(
        request=request,
        template_name='main/game_product_detail.html',
        context={
            "game_product": game_product,
            "similar_game_products": similar_game_products,
            "game_product_update_form": game_product_update_form,
            "game_product_comments": game_product_comments,
            "rating_avg": rating_avg
        })


def game_product_create_view(request):
    if not request.user.is_authenticated:
        raise Http404()

    if request.method == 'POST':
        form = GameProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            game_product_object = form.save(commit=False)
            game_product_object.user = request.user
            game_product_object.save()

            messages.success(request, 'Успешно создано!')
            return redirect('index')

    form = GameProductCreateForm()
    return render(request, 'main/game_product_create.html', {"form": form})


def game_product_update_view(request, game_product_id):
    game_product = get_object_or_404(Game_Product, id=game_product_id)

    if request.method == 'POST':
        form = GameProductUpdateForm(request.POST, request.FILES, instance=game_product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно изменено!')
            return redirect('game_product_detail', game_product_id)

def game_product_delete_view(request, game_product_id):
    game_product = get_object_or_404(Game_Product, id=game_product_id)

    if request.method == "POST":
        game_product.delete()
        messages.success(request, "Товар успешно удален!")
        return redirect("index") 

    return redirect("game_product_detail", game_product_id)


def rating_create_view(request, game_product_id):
    game_product = get_object_or_404(Game_Product, id=game_product_id)

    if not request.user.is_authenticated:
        messages.error(request, 'Только авторизованные!')
        return redirect('game_product_detail', game_product_id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        count = int(request.POST.get('count', ''))

        rating = Rating(
            user=request.user,
            game_product=game_product,
            count=count,
            comment=comment
        )
        rating.save()
        messages.success(request, 'Спасибо за отзыв!')
        return redirect('game_product_detail', game_product_id)


def rating_answer_create_view(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)

    if rating.game_product.user != request.user:
        messages.error(request, 'Нету доступа')
        return redirect('game_product_detail', rating.game_product.id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '')

        rating_answer = RatingAnswer(
            user=request.user,
            rating=rating,
            comment=comment
        )

        rating_answer.save()

        messages.success(request, 'Успешно отправлено')
        return redirect('game_product_detail', rating.game_product.id)


def user_profile_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Только авторизованные!')
        return redirect('index' )
    
    payment_requests = PaymentRequest.objects.filter(game_product__user=request.user, status='in_processing').order_by('-id')[:3]
  
    return render(
        request=request,
        template_name='main/user_profile.html',
        context={
            'payment_requests': payment_requests
        }
    )


def game_product_payment_create_view(request, game_product_id):
    game_product = get_object_or_404(Game_Product, id=game_product_id)
    seller_payment_methods = PaymentMethod.objects.filter(user=game_product.user)

    if request.method == 'POST':
        check = request.FILES.get('check', '')
        quantity = request.POST.get('quantity')

        total_price = Decimal(quantity) * game_product.price

        order = PaymentRequest(
            user=request.user,
            game_product=game_product,
            quantity=quantity,
            check_image=check,
            total_price=total_price
        )
        order.save()
        messages.success(request, 'Заявку на оплату отправлена продавцу')
        return redirect('index')

    return render(
        request=request,
        template_name='main/game_product_payment.html',
        context={
            "seller_payment_methods": seller_payment_methods
        }
    )
def game_product_list_view(request):
    queryset = Game_Product.objects.filter(is_active=True)
    queryset = queryset.annotate(avg_rating=Avg('rating__count'))

    if 'game_product_search' in request.GET:
        game_product_name = request.GET.get("game_product_search")
        queryset = queryset.filter(title__icontains=game_product_name)

    game_products = GameProductListFilter(request.GET, queryset=queryset)

    # Paginator
    paginator = Paginator(game_products.qs, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, 
        'main/game_product_list.html', 
        {'page_obj': page_obj, 
         'game_products': game_products,
         'avg_ratings': {product.id: product.avg_rating for product in queryset}
         })


def payment_request_list_view(request):
    payment_requests = PaymentRequest.objects.filter(game_product__user=request.user).order_by('-id')

    return render(
        request=request,
        template_name='main/payment_request.html',
        context={
            'payment_requests': payment_requests
        }
    )


def payment_request_update_status(request, payment_request_id):
    payment_request = get_object_or_404(PaymentRequest, id=payment_request_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        payment_request.status = status
        payment_request.save()

        if payment_request.status == 'accepted':

            payment = Payment(
                seller=payment_request.game_product.user,
                user=payment_request.user.first_name,
                game_product=payment_request.game_product.title,
                quantity=payment_request.quantity,
                check_image=payment_request.check_image,
                total_price=payment_request.total_price
            )
            payment.save()

        messages.success(request, 'Успешно изменено')

    return redirect('payment_requests')


def payment_list_view(request):
    payments = Payment.objects.filter(seller=request.user)

    total_payments = payments.aggregate(Sum('total_price'))['total_price__sum']

    return render(
        request=request,
        template_name='main/payments.html',
        context={
            "payments": payments,
            "total_payments": total_payments
        }
    )
