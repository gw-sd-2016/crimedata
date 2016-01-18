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

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^map$', views.mapview),
    url(r'^map2$', views.mapview2),

    # CBV to encode "crimes-by-type" list into GeoJSON for consumption by mapping UI
    url(r'^crime_type_layer.geojson$',
        views.IncidentTypeMapLayer.as_view(
            model=s_models.Incident,
            properties=('marker_title', 'point',),
            geometry_field='point',
        ),
        name='crime_type_layer_gjson'),

    url(r'^subdiv_layer.geojson$',
        views.SubdivisionMapLayer.as_view(
            model=s_models.Subdivision,
            properties=('display_name', 'src_file_index'),
            geometry_field='polygon',
        ),
        name='subdivision_layer_gjson'),
]
