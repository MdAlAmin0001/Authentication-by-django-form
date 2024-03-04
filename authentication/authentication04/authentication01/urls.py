from django.contrib import admin
from django.urls import path
from myapp.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',signup, name='signup' ),
    path('',loginpage, name='loginpage' ),
    path('logoutpage/',logoutpage, name='logoutpage' ),
    path('home/',home, name='home' ),
    path('profile/', profile, name='profile'),
    
    path('activate/<uid64>/<token>', activate,name='activate'),
    
    path('forgetpassword/', forgetpassword, name="forgetpassword"),
    path('changepassword/', changepassword, name="changepassword"),
    
    
    # path('search_query/', search_query, name="search_query"),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
