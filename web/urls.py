from django.urls import path
from django.shortcuts import render
from . import views
from OnlineLib import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name="home"),
    path('signin',views.signin,name="signin"),
    path('signup',views.signup,name="signup"),
    path('shop',views.shop,name="shop"),
    path('pen',views.pens_view,name="pen"),
    path('books',views.books_view,name='books'),
    path('arts',views.arts_view, name="arts"),
    path('stationery',views.stationeries_view,name='stationeries'),
    path('sport',views.sports_view,name='sport'),


    path('user/<str:username>',views.user,name="user"),
    path('cart',views.cart,name="cart"),
    path('addToCart',views.addToCart,name="addToCart"),
    path('addStationery',views.add_stationery_to_cart,name="addStationery"),
    path('removeItem/<str:ISBN>',views.removeItem,name="removeItem"),
    path('pay',views.pay,name="pay"),
    path('checkpay',views.checkpay,name="checkpay"),
    path('guest',views.guest,name="guest"),
    path('order',views.order,name="order"),
    path('guestorder',views.guestorder,name="guestorder"),
    path('guestpay',views.guestpay,name="guestpay"),
    path('upload_file', views.upload_file, name='upload_file'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('order_user', views.order_user, name='order_user'),
    path('order_pay', views.order_pay, name='order_pay'),
    path('search', views.search, name='search'),
    path('apply', views.apply, name='apply'),
    path('approveseller', views.approveseller, name='approveseller'),
    path('uploaditem', views.uploaditem, name='uploaditem'),
    path('group-of-categories/<str:name>', views.get_book_by_group_of_categories, name='get_book_by_group_of_categories'),
    path('category/<str:name>', views.get_books_by_category, name='get_books_by_category'),
    path('emailNotification',views.emailNotification,name="emailNotification"),
    path('approveapplication/<int:id>',views.approveapplication,name="approveapplication"),
    path('declineapplication/<int:id>',views.declineapplication,name="declineapplication"),
    path('approvedshops',views.approvedshops,name="approvedshops"),
    path('mybooks',views.mybooks,name="mybooks"),
    path('uploadedfiles',views.uploadedfiles,name="uploadedfiles"),
    path('uploadedfile/<int:id>', views.uploadedfile, name="uploadedfile"),
    path('addbookitem',views.addbookitem,name="addbookitem"),
    path('paybookitem',views.paybookitem,name="paybookitem"),
    path('stkconfirm/',views.stkconfirm,name="stkconfirm"),
    # path('stationery', views.stationery, name="stationery"),
    # path('sports', views.sports, name="sports"),
    # path('categorylist',views.categorylist,name="categorylist"),

    # path('cart', views.add_to_cart, name='cart'),
    # path('remove', remove_from_cart, name='remove-cart'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

