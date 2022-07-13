from django.urls import path;
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('addProduct',views.addProduct,name="addProduct"),
    path('add',views.add,name="add"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)