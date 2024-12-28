from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse 
from .models import Product

import stripe 


def product_list(request):
    products = Product.objects.all()
    return render(request, 'stripe/product_list.html', {'products': products})

def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        
        product = get_object_or_404(Product, id=product_id)
        
        # el precio debe estar en centavos y ser >= a $0.50 Ejemplo 2000 y luego Stripe lo convierte en $20.00 USD
        product_price = int(product.price)
        
        image = product.images.first()
        image_url = request.build_absolute_uri(image.image.url) if image else None
        
        user_email = request.user.email if request.user.is_authenticated else None
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": product_price,  
                        "product_data": {
                            "name": product.name,
                            "description": product.description,
                            # Imagen de Prueba
                            'images': ['https://images.unsplash.com/photo-1579202673506-ca3ce28943ef'],
                            # Descomentar en produccion y usar imagenes hosteadas en algun servidor
                            #'images': [image_url],
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("cancel", kwargs={'product_id': product_id})),
        )
        return redirect(checkout_session.url, code=303)
    # cambiar por la pagina a redireccionar si no es POST
    return render(request, "products/home.html")

def home(request):
    pass

def success(request):
    return render(request, "stripe/success.html")


def cancel(request, product_id=None):
    return render(request, "stripe/cancel.html", {'product_id': product_id})
