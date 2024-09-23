from django.urls import path
from . import views

urlpatterns = [    
    path('',views.home),
    path('showCakes/<cid>',views.showCakes),
    path('ViewDetails/<cake_id>',views.ViewDetails),
    path('Register',views.Register),
    path('Login',views.Login),
    path("Logout",views.Logout),
    path("Cart",views.showcart),
    path('MakePayment',views.MakePayment),
    path('MyOrders',views.MyOrders),
]
