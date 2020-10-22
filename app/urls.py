from . import views as _

from django.conf import settings
from django.conf.urls import url

from django.urls import path

from django.views.static import serve

app_name = 'app'

urlpatterns = [
    path('', _.HOME, name = 'home'),
    path('store/', _.STORE, name = 'store'),
    path('store/<int:pk>/', _.DETAIL, name = 'detail'), 
    path('comment/', _.comment, name = 'comment'),
    path('categorys/', _.categorys, name = 'categorys'),
    path('categorys/<str:cat>/', _.categorys, name = 'categorys'),
    path('search/', _.search, name = 'search'), 
    
    path('aboutus/', _.aboutus, name = 'aboutus'), 

    path('login/', _.login, name = 'login'), 
    path('signup/', _.signup, name = 'signup'), 
    path('logout/', _.logout, name = 'logout'), 
    
    path('payment/', _.payment, name = 'payment'), 
    path('submit/<int:user_id>/', _.submit, name = 'submit'), 

    path("sabad_kharid/", _.sabad_kharid, name = "sabad_kharid"),

    path("cart/", _.cart, name = "cart"),

    # AJAX 
    path("remove_product/", _.remove_product, name = "remove_product"),
    path("change_count/", _.change_count, name = "change_count"),
    path("Second_Update_Prices/", _.Second_Update_Prices, name = "Second_Update_Prices"),

    # Login
    path('check/', _.check.as_view(), name = 'check'),
    
    # Clients 
    path('get_users/', _.get_users.as_view(), name = 'get_users'),
    path('search_clients/', _.search_clients.as_view(), name = 'search_clients'),
    path('adduser/', _.adduser.as_view(), name = 'adduser'),
    path('delete/', _.delete.as_view(), name = 'delete'),
    path('get_user/', _.get_user.as_view(), name = 'get_user'),
    path('update_user/', _.update_user.as_view(), name = 'update_user'),
        
    # Store
    path('update_store/', _.update_store.as_view(), name = 'update_store'),
    path('add_product/', _.add_product.as_view(), name = 'add_product'),
    path('get_product/', _.get_product.as_view(), name = 'get_product'),
    path('update_product/', _.update_product.as_view(), name = 'update_product'),
    path('delete_product/', _.delete_product.as_view(), name = 'delete_product'),
    path('product_search/', _.product_search.as_view(), name = 'product_search'),
    path('AllSells/', _.AllSells.as_view(), name = 'AllSells'),

    # Card 
    path('get_product_for_buy/', _.get_product_for_buy.as_view(), name = 'get_product_for_buy'),
    path('verify/', _.verify.as_view(), name = 'verify'),

    url(r'^media/(?P<path>.*)/$', serve, {'document_root': settings.MEDIA_ROOT}, name = 'Media'), 
]