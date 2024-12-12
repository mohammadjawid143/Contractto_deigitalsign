from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.request_contact_sign, name='request_Contact_sign'),
    path('contract/<int:contract_id>/', views.contract_detail, name='contract_detail'),
    path('<int:contract_id>/', views.contract_detail, name='contract_detail'),
    path('all_contract/', views.all_contract, name='contracts_all'),
    path('delete/<int:contract_id>/', views.contract_delete, name='contract_delete'),

#     path("create-contract/", views.request_contract, name="create_contract"),
#     path("contract_details/<int:pk>/", views.contract_details, name="contract_details"),
#     path("contract_save/", views.contract_save, name="contract_save"),
#     path("contract_update/<int:pk>/", views.contract_update, name="contract_update"),
#     path("contract_delete/<int:pk>/", views.contract_delete, name="contract_delete"),
]

