from django.urls import path
import apps.dashboard.views as views


urlpatterns = [
    path("index", views.DashboardView.as_view(), name="dashboard"),
    path("api-key/", views.APIKeyView.as_view(), name="api-key"),
    path("links/", views.LinksListView.as_view(), name="links"),
    path("links/create", views.LinksCreateView.as_view(), name="links_create"),
    path("links/<str:slug>/", views.LinksDetailView.as_view(), name="links_detail"),
    path("links/<str:slug>/edit", views.LinksEditView.as_view(), name="links_edit"),
    path(
        "links/<str:slug>/delete", views.LinksDeleteView.as_view(), name="links_delete"
    ),
    path("groups/", views.GroupsListView.as_view(), name="groups"),
    path("groups/create", views.GroupsCreateView.as_view(), name="groups_create"),
    path("groups/<str:slug>/", views.GroupsDetailView.as_view(), name="groups_detail"),
    path(
        "groups/<str:slug>/links-entries",
        views.GroupsLinkEntriesView.as_view(),
        name="groups_links_entries",
    ),
    path("groups/<str:slug>/edit", views.GroupsEditView.as_view(), name="groups_edit"),
    path(
        "groups/<str:slug>/delete",
        views.GroupsDeleteView.as_view(),
        name="groups_delete",
    ),
    path("qrcode/", views.QRCodeListView.as_view(), name="qrcode"),
    path("qrcode/create", views.QRCodeCreateView.as_view(), name="qrcode_create"),
    path("qrcode/<str:slug>/edit", views.QRCodeEditView.as_view(), name="qrcode_edit"),
    path(
        "qrcode/<str:slug>/delete",
        views.QRCodeDeleteView.as_view(),
        name="qrcode_delete",
    ),
]
