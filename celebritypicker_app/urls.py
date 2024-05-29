from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('celebrity/<int:celeb_id>/', views.celebrity_details, name='celebrity_details'),
    path('celebrity/birthdays/', views.celebrity_birthdays, name='celebrity_birthdays'),
    path('celebrity/random/', views.random_movie_or_show, name='random_movie_or_show'),
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.update_profile, name='update_profile'),
    path('delete_pick/<int:pick_id>/', views.delete_pick, name='delete_pick'),
    path('clear_filter/', views.clear_filter, name='clear_filter'),
    path('save_random_pick/', views.save_random_pick, name='save_random_pick'),
    path('mark_favorite/', views.mark_favorite, name='mark_favorite'),
    path('unmark_favorite/', views.unmark_favorite, name='unmark_favorite'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
