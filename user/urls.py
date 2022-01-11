from django.urls import path
from user import views
from django.contrib.auth.views import LogoutView
from rest_framework.authtoken import views as rest_framework_views
urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("films/", views.FilmList.as_view(), name='film-list'),
    path('employees/', views.list_employees, name='employee-list'),
    path('list/', views.employee_view, name='list'),
    # path('api-token-auth/', views.CustomAuthToken.as_view()),
    path('api-token-auth/', rest_framework_views.obtain_auth_token),
]

htmx_urlpatterns = [
    path('check_username/', views.check_username, name='check-username'),
    path('add-film/', views.add_film, name='add-film'),
    path('delete-film/<int:pk>/', views.delete_film, name='delete-film'),
    path('search-film/', views.search_film, name='search-film'),
    path('clear/', views.clear, name='clear'),
    path('id/<int:pk>/', views.set_employee_status_active, name='activate'),
    path('activate/', views.activate, name='active'),
    path('deactivate/', views.deactivate, name='deactive'),
    path('edit/<int:pk>/', views.EmployeeUpdate.as_view(), name='edit'),
    path('random/', views.random_employees, name='random'),
]

urlpatterns += htmx_urlpatterns
