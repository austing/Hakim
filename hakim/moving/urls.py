from django.conf.urls import patterns, include, url
from moving.views import particulier_devis, calculate_volume


urlpatterns = patterns('',
    url(r'^devis/$', particulier_devis, name='particuliar_devis'),
    url(r'^calculate_volume/$', calculate_volume, name='calculate_volume'),
)


