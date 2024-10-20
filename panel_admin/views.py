from django.shortcuts import render
import json

def vista_admin_ventas(request):
    data = [10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 23, 33]
    data_pagos = [140, 235]
    return render(request, 'panel_admin/admin_ventas.html', {
        'data': json.dumps(data),
        'data_pagos': json.dumps(data_pagos),
    })

def vista_admin_empleados(request):
    return render(request, 'panel_admin/admin_empleados.html')

def vista_admin_plantilla(request):
    return render(request, 'panel_admin/admin_base.html')