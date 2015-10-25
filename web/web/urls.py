"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

# admin.autodiscover()
from spatial import views, models as s_models
from djgeojson.views import GeoJSONLayerView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^map$', views.mapview),
    url(r'^map2$', views.mapview2),

    url(r'^all_datapoints.js$',
        GeoJSONLayerView.as_view(
            model=s_models.Incident,
            properties=('marker_title', 'point',),
            geometry_field='point',
        ),
        name='all_datapoints_geojson'),
]
