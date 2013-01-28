from django.conf.urls import patterns, include, url


urlpatterns = patterns('moving.views',
    url(r'^devis/$', 'particulier_devis', name='particuliar_devis'),
    url(r'^calculate_volume/$', 'calculate_volume', name='calculate_volume'),
    url(r'^$', 'index', name='index'),
)


