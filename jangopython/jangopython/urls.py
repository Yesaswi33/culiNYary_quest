from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from home.views import home,get_dish_data,index,menu_card
from vege.views import receipes, delete_receipe, update_receipe,login_page ,register,logout_page # ✅ Add this
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),             # Homepage
    path('explore/',index, name='index'),   # Map page
    path('get_dish_data/',get_dish_data, name='get_dish_data'),
    path('menu/',menu_card, name='menu-card'),
    path('receipes/', receipes, name="receipes"),
    path('home/', home, name="home"),
    path('login/', login_page, name="login"),  # ✅ matches what logout_page expects
    path('register/', register, name="register"),
    path('logout/', logout_page, name="logout_page"),
    
    path('admin/', admin.site.urls),
    path('delete-receipe/<int:id>/', delete_receipe, name="delete_receipe"), 
    path('update-receipe/<int:id>/', update_receipe, name="update_receipe"), 
    
]


# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
