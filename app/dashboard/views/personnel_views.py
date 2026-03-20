from django.shortcuts import render


def dashboard_personnel(request):
    return render(request, 'dashboard/dashboard.html', {
        'active_tab': 'personnel',
    })