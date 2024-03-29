from django.urls import path

from customer.views import ListCustomerView, CustomerView, ListFidelityCardView, FidelityCardView

urlpatterns = [
    path('', ListCustomerView.as_view(), name='customers'),
    path('customer/<str:customer_id>', CustomerView.as_view(), name='customer'),
    path('fidelityCards', ListFidelityCardView.as_view(), name='fidelity_cards'),
    path('fidelityCards/<str:barcode>', FidelityCardView.as_view(), name='fidelity_card')
]