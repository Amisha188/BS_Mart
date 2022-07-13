from django.urls import path
from . import views
from django.urls.resolvers import URLPattern


urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name='register'),
    path('addProduct/',views.addProduct,name="addProduct"),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('index/',views.index,name='index'),
    path('displayAllCustomer/',views.displayAllCustomer,name='displayAllCustomer'),

    path('product_details/',views.product_details,name='product_details'),
    path('updateProduct/<id>',views.updateProduct,name="updateProduct"),
    path('displayProduct/',views.displayProduct,name="displayProduct"),
    path('deleteProduct/<id>',views.deleteProduct,name="deleteProduct"),

    path('updateProfile/',views.updateProfile,name="updateProfile"),
    path('displayProfile/',views.displayProfile,name="displayProfile"),
    path('deleteProfile/',views.deleteProfile,name="deleteProfile"),

    path('indexCategory/<category1>',views.indexCategory,name='indexCategory'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('updateAddress/',views.updateAddress,name='updateAddress'),
    path('addToCart/<id>', views.addToCart, name="addToCart"),
    path('deleteCartItem/<id>', views.deleteCartItem, name="deleteCartItem"),
    path('increaseQuantity/<id>',views.increaseQuantity,name='increaseQuantity'),
    path('decreaseQuantity/<id>',views.decreaseQuantity,name='decreaseQuantity'),

    path('addOrder/', views.addOrder, name='addOrder'),
    path('orderHistory/',views.orderHistory,name="orderHistory"),
    path('displayOrder/<id>',views.displayOrder,name="displayOrder")
    # path('add/',views.add,name="add"),
]