from django.shortcuts import render


def dashboard_finance(request):
    return render(request, 'dashboard/dashboard.html', {
        'active_tab': 'finance',
    })