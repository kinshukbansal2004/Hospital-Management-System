from django.contrib import admin
from django.urls import path
from dreamapp import views
urlpatterns = [
    path('',views.index,name='index'),
    path('submit/',views.feedback,name='submit'),
    path('emergency/',views.emergency,name='emergency'),
    path('appointment/',views.appointment,name='appointment'),
    path('patient/',views.patient,name='appointment'),
    path('doctor/',views.doctor,name='appointment'),
    path('contacts/',views.contacts,name='appointment'),
    path('rooms/',views.rooms,name='rooms'),
    path('admit/',views.admit,name='admit'),
    path('discharge/',views.discharge,name='discharge'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('discharge/paymenthandler/', views.success, name='paymenthandler'),
    path('appointment/paymenthandler/', views.success1, name='paymenthandler'),
]
