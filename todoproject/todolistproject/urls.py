from django.contrib import admin
from django.urls import path,include
from todolistproject import views as view
from django.conf import settings
urlpatterns = [
   path('',view.index,name='index'),
   path('signup/',view.signup,name='signup'),
   path('signin',view.signin,name='signin'), 
   path('signout/',view.signout,name='signout'),
   path('addtask/',view.addtask,name='addtask'),
   path('dashboard',view.dashboard,name='dashboard'),
   path('delete/<int:id>',view.delete,name='delete'),
   path('update/<int:id>',view.update,name='update'),
   path('notfication/',view.notfication,name='notfication'),
]
