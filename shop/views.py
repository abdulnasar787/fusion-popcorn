from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Order

PRODUCTS = {
    "classic": {"name": "Classic Popcorn", "price": 99, "description": "Light, crispy and delicious — the timeless movie-night favourite.", "emoji": "🍿", "tag": "BESTSELLER"},
    "caramel": {"name": "Caramel Popcorn", "price": 149, "description": "A golden caramel coating for a sweet, satisfying crunch.", "emoji": "🍯", "tag": "SWEET"},
    "cheese": {"name": "Cheese Popcorn", "price": 129, "description": "A bold, savoury cheese flavour in every bite.", "emoji": "🧀", "tag": "SAVOURY"},
    "chocolate": {"name": "Chocolate Popcorn", "price": 159, "description": "A cocoa-inspired treat for chocolate lovers.", "emoji": "🍫", "tag": "PREMIUM"},
    "spicy": {"name": "Spicy Masala Popcorn", "price": 119, "description": "A lively masala kick for snack-time explorers.", "emoji": "🌶️", "tag": "SPICY"},
    "party": {"name": "Party Combo Box", "price": 349, "description": "A shareable mix for movie nights and get-togethers.", "emoji": "🎉", "tag": "VALUE PACK"},
}
COMBOS = [
    {"name": "Movie Night Duo", "description": "Two crowd-favourite flavours", "price": 229, "emoji": "🎬"},
    {"name": "Family Crunch Box", "description": "A shareable selection for everyone", "price": 349, "emoji": "🍿"},
    {"name": "Sweet & Savoury Set", "description": "A little bit of everything", "price": 279, "emoji": "✨"},
]

def cart_data(request):
    cart = request.session.get("cart", {})
    rows, total, count = [], 0, 0
    for slug, qty in cart.items():
        product = PRODUCTS.get(slug)
        if not product:
            continue
        qty = max(1, min(int(qty), 20))
        subtotal = product["price"] * qty
        rows.append({"slug": slug, **product, "qty": qty, "subtotal": subtotal})
        total += subtotal
        count += qty
    return rows, total, count

def common(request):
    rows, total, count = cart_data(request)
    return {"cart_count": count}

def home(request):
    featured = [PRODUCTS[k] | {"slug": k} for k in ("classic", "caramel", "cheese")]
    return render(request, "shop/home.html", {"featured": featured, **common(request)})

def shop(request):
    products = [PRODUCTS[k] | {"slug": k} for k in PRODUCTS]
    return render(request, "shop/shop.html", {"products": products, **common(request)})

def product_detail(request, slug):
    product = PRODUCTS.get(slug)
    if not product:
        return redirect("shop")
    return render(request, "shop/product_detail.html", {"product": product | {"slug": slug}, **common(request)})

def offers(request):
    combos = [combo | {"slug": "party" if "Family" in combo["name"] else "classic"} for combo in COMBOS]
    return render(request, "shop/offers.html", {"combos": combos, **common(request)})

def cart(request):
    rows, total, count = cart_data(request)
    return render(request, "shop/cart.html", {"rows": rows, "total": total, **common(request)})

@require_POST
def add_to_cart(request, slug):
    if slug not in PRODUCTS:
        return redirect("shop")
    cart = request.session.get("cart", {})
    cart[slug] = min(int(cart.get(slug, 0)) + 1, 20)
    request.session["cart"] = cart
    messages.success(request, f'{PRODUCTS[slug]["name"]} added to your cart.')
    return redirect(request.POST.get("next") or "cart")

@require_POST
def update_cart(request, slug):
    cart = request.session.get("cart", {})
    try:
        qty = int(request.POST.get("qty", "1"))
    except ValueError:
        qty = 1
    if slug in cart:
        if qty <= 0:
            cart.pop(slug, None)
        else:
            cart[slug] = min(qty, 20)
    request.session["cart"] = cart
    return redirect("cart")

@require_POST
def remove_from_cart(request, slug):
    cart = request.session.get("cart", {})
    cart.pop(slug, None)
    request.session["cart"] = cart
    return redirect("cart")

def checkout(request):
    rows, total, count = cart_data(request)
    if not rows:
        messages.info(request, "Add a product before checkout.")
        return redirect("shop")
    if request.method == "POST":
        name = request.POST.get("customer_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        if not name or not phone or not address:
            messages.error(request, "Please complete all delivery details.")
        else:
            order = Order.objects.create(
                customer_name=name,
                phone=phone,
                address=address,
                items_json=[{"slug": r["slug"], "name": r["name"], "qty": r["qty"], "price": r["price"]} for r in rows],
                total_paise=total * 100,
            )
            request.session["pending_order_id"] = order.id
            return redirect("payment")
    return render(request, "shop/checkout.html", {"rows": rows, "total": total, **common(request)})

def payment(request):
    order_id = request.session.get("pending_order_id")
    if not order_id:
        return redirect("cart")
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/payment.html", {"order": order, **common(request)})

def about(request):
    return render(request, "shop/about.html", common(request))

def gallery(request):
    gallery_items = [
        ("Classic Crunch", "🍿"), ("Caramel Glow", "🍯"), ("Cheese Please", "🧀"),
        ("Chocolate Treat", "🍫"), ("Spicy Kick", "🌶️"), ("Party Time", "🎉")
    ]
    return render(request, "shop/gallery.html", {"gallery_items": gallery_items, **common(request)})

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        if name and email and message:
            messages.success(request, "Thanks! Your demo enquiry has been received.")
            return redirect("contact")
        messages.error(request, "Please complete all fields.")
    return render(request, "shop/contact.html", common(request))

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/order_confirmation.html", {"order": order, **common(request)})
