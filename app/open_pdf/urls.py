from django.urls import path
from . import views


from django.conf.urls.static import static
from django.conf import settings


app_name = 'simple_pdf'

urlpatterns = [
    # # path('', views.start, name = 'start'),
    path('api/v1/manual', views.manual_pdf, name = "pdf_maual"),
    # path('generate_pdf/', views.generate_pdf, name = 'generate_pdf'),
    # path('login', views.login, name = 'login'),
    # # path('cutaway', views.cutaway, name = 'cutaway'), #визитка
    # path('', views.cutaway, name = 'cutaway'), #визитка
    # path('generate_pdf/manual', views.manual_pdf), #визитка
    # path('manual', views.manual, name = 'manual'),
    # path('exel', views.exel, name = 'manual'),
    # path('upload_exel', views.upload_exel, name = "upload_exel"),
    # path('preview/<uuid:prev_uuid>', views.preview, name = "preview")
    # path('preview/<uuid:prev_uuid>', views.preview, name = "preview")
]
