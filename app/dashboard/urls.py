from django.urls import path
from dashboard.views import home, dashboard_student, dashboard_personnel, dashboard_finance

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard_student, name='dashboard'),
    path('dashboard/student/', dashboard_student, name='dashboard_student'),
    path('dashboard/personnel/', dashboard_personnel, name='dashboard_personnel'),
    path('dashboard/finance/', dashboard_finance, name='dashboard_finance'),
]