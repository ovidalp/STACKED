from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name = 'codeapp/index.html'), name='index'),
    url(r'^download$', TemplateView.as_view(template_name = 'codeapp/download.html'), name='download'),
    url(r'^presentation$', TemplateView.as_view(template_name = 'codeapp/presentation.html'), name='presentation'),
    url(r'^comparation$', views.comparation_view, name='comparation'),
    url(r'^comparedata$', views.compare_data, name='comparedata'),

    url(r'^factor$', views.factor_view, name='factor'),
    url(r'^factordata$', views.factor_data, name='factordata'),

    url(r'^dataset$', views.download_dataset, name='dataset'),
]

