
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('categories/',views.categories,name='categories'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('product/<int:pk>/',views.product,name='product'),
    path('category/<str:foo>/',views.categorypr,name='categorypr'),
    path('searchproduct/',views.searchproduct,name='searchproduct'),
    path('findgift/',views.findgift,name='findgift'),
    path('findgifts/gift',views.findcategory,name='findcategory'),
    path('myorders/',views.my_orders,name="my_orders"),
]