from django.urls import path

from . import views

urlpatterns = [
    path('faq/', views.faq, name='faq'),
    path('productv/', views.productV, name='productv'),
    path('login/', views.login_page, name='login'),
    
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.store, name='store'),
    path('sorted_store_a', views.sortedStore_a, name='sorted_store_a'),
    path('sorted_store_d', views.sortedStore_d, name='sorted_store_d'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path("search/", views.SearchView, name="search"),

]

