from django.urls import path, include
from dashboard.views import dashboard, notification, stock, orders, feedback, reports, profile
import django_eventstream

app_name = 'dash'

urlpatterns = [
    path('home/', dashboard.dash_home, name='dash_home'),
    path('reports/', reports.reports_view, name='reports'),
    # feedback 
    path('feedback/', feedback.FeedBackListView.as_view() , name="feedback_list"),
    path('feedback/create/', feedback.create_feedback, name="create_feedback"),
    path('feedback/approve/<int:pk>/', feedback.approve_feedback, name="approve_feedback"),
    path('feedback/delete/<int:pk>/', feedback.delete_feedback, name="delete_feedback"),
    # Stock 
    path('stock/', stock.stock_list, name='stock_list'),
    path('stock/create/', stock.create_stock, name='stock_create'),
    path('stock/edit/<int:pk>/', stock.edit_stock, name='edit_stock'),
    path('stock/delete/<int:pk>/', stock.delete_stock.as_view(), name='delete_stock'),
    path('get_product_gallery/<int:pk>/', stock.get_product_gallery, name='get_product_gallery'),
    # Sales
    path('orders/', orders.sales_list, name='sales_list'),
    path('orders/delete/<int:pk>', orders.delete_order.as_view(), name='delete_sale'),
    path('get_order_details/<int:pk>/', orders.get_order_details, name='get_order_details'),
    path('update_order_status/<int:pk>/', orders.update_order_status, name='update_order_status'),
    # SSE events (django_eventstream built-in handler — no custom view)
    path("sse/", include(django_eventstream.urls)),
    # Notifications API
    path('api/notifications/unread/<int:user_id>/', notification.unread_notifications_api, name='unread_notifications_api'),
    path('api/notifications/mark-all-read/<int:user_id>/', notification.mark_all_notifications_as_read_api, name='mark_all_notifications_as_read_api'),
    # Profile
    path('profile/', profile.profile_view, name='profile'),
]
