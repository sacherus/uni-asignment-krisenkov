import debug_toolbar
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from metars.views import MetarViewSet

swagger_schema_view = get_swagger_view(title="API")

metars_list = MetarViewSet.as_view({"get": "list", "post": "create",})

urlpatterns = [
    # Views
    path("metars/<int:timestamp>/", metars_list, name="metars-view"),
    path("__debug__/", include(debug_toolbar.urls)),
    url(r"^$", swagger_schema_view),
    url("admin/", admin.site.urls),
    url("", include("django_prometheus.urls")),
]
admin.site.site_header = "uni_assignment_metars"
admin.site.site_title = "uni_assignment_metars"
