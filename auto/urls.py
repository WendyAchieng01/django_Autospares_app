from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("shop/", views.shop, name="shop"),
    path('shop/category/<int:category_id>/', views.categorypage, name='categorypage'),
    path('shop/brand/<int:brand_id>/', views.brandpage, name='brandpage'),
    path('shop/accessories/<int:accessories_id>/', views.accessoriespage, name='accessoriespage'),
    path("specials/", views.specials, name="specials"),
    path("about-us/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("single-product-variable/<int:product_id>/", views.singleproduct, name="singleproduct"),
    path("faq/", views.faq, name="faq"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("search_shop/", views.search_shop, name="search_shop"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("delivery/", views.delivery, name="delivery"),
    path("terms_and_conditions/", views.terms_and_conditions, name="terms_and_conditions"),
    path("returns/", views.returns, name="returns"),
]
