from django.urls import path 
from . import views 
  
urlpatterns = [ 
    path('secret', views.secret), 
    path('me', views.me), 
    path('manager-view', views.manager_view), 
    path('users/login', views.login),
    path('users/logout', views.logout),
    path('users/assign', views.AssignUser.as_view()),
    path('menu-items', views.MenuItem.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItem.as_view()),
    path('category', views.CategoryItem.as_view()),
    path('category/<int:pk>', views.SingleCategoryItem.as_view()),
    path('customer/menu-items', views.menu_items),
    path('cart', views.CartView.as_view()),
    path('cart/flush', views.FlushCartView.as_view()),
    path('order', views.OrderItemView.as_view()),
    path('admin/order/<int:pk>', views.SingleOrderView.as_view()),
    path('admin/order', views.OrderView.as_view()),
]