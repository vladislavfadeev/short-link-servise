from django.urls import path
import apps.dashboard.views as views

# app_name = 'dashboard'


urlpatterns = [
    path('index', views.DashboardView.as_view(), name='dashboard'),
    path('user/', views.ProfileView.as_view(), name='profile'),
    # path('bot/', views.ProfileView.as_view(), name='bot_set'),
    # path('developer/', views.ProfileView.as_view(), name='api_doc'),
    # path('donate/', views.ProfileView.as_view(), name='donate'),
    path('links/', views.LinksListView.as_view(), name='links'),
    path('links/create', views.LinksCreateView.as_view(), name='links_create'),
    # path('links/<str:slug>/', views.ProfileView.as_view(), name='links_detail'),
    path('links/<str:slug>/edit', views.LinksEditView.as_view(), name='links_edit'),
    path('links/<str:slug>/delete', views.LinksDeleteView.as_view(), name='links_delete'),
    path('groups/', views.GroupsListView.as_view(), name='groups'),
    path('groups/create', views.GroupsCreateView.as_view(), name='groups_create'),
    # path('groups/<str:slug>/', views.ProfileView.as_view(), name='groups_detail'),
    path('groups/<str:slug>/edit', views.GroupsEditView.as_view(), name='groups_edit'),
    path('groups/<str:slug>/delete', views.GroupsDeleteView.as_view(), name='groups_delete'),
]