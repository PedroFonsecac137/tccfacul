from django.contrib import admin
from django.urls import include, path
from acompanhamento import views as acompanhamento_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("conta/criar/", acompanhamento_views.criar_conta, name="criar_conta"),
    path("conta/", include("django.contrib.auth.urls")),
    path("", include("acompanhamento.urls")),
]
