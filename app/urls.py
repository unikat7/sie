from django.urls import path
from .views import home,about,contact,register,signin,log_out,course,description,profile,profile_update,success,failure,pay

urlpatterns=[
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('register/',register,name='register'),
    path('courses',course,name='course'),
    path('description/<int:id>',description,name='description'),
    path('signin/',signin,name='signin'),
    path('logout/',log_out,name='logout'),
    path('profile/',profile,name='Profile'),
    path('pay/<int:id>/', pay, name='pay'),
    path('success/<int:id>',success,name='success'),
    path('failure/<int:id>',failure,name='failure'),
    path('profileupdate/',profile_update,name='profileup')

   
]