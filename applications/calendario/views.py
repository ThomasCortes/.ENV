import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Actividad
from datetime import datetime


def calendario_view(request):
    return render(request, 'calendario.html')


# ===============================
# 1. OBTENER EVENTOS
# ===============================
def obtener_eventos(request):
    eventos = Actividad.objects.all()
    data = []

    for e in eventos:
        if e.hora:
            start = f"{e.fecha.isoformat()}T{e.hora.strftime('%H:%M')}"
        else:
            start = e.fecha.isoformat()

        data.append({
            "id": e.id,
            "title": e.titulo,
            "start": start,
        })

    return JsonResponse(data, safe=False)


# ===============================
# 2. AGREGAR EVENTO
# ===============================
@csrf_exempt
def agregar_evento(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        titulo = data.get('title')
        fecha = data.get('date')
        hora_str = data.get('time')

        hora = None
        if hora_str:
            hora_str = hora_str.strip()

            # Caso 1: Formato con AM/PM -> 10:30 AM
            if "AM" in hora_str or "PM" in hora_str:
                hora = datetime.strptime(hora_str, "%I:%M %p").time()

            # Caso 2: Formato 24h -> 14:30
            else:
                hora = datetime.strptime(hora_str, "%H:%M").time()


        actividad = Actividad.objects.create(
            titulo=titulo,
            fecha=fecha,
            hora=hora
        )

        return JsonResponse({"id": actividad.id})
    return HttpResponseNotAllowed(['POST'])


# ===============================
# 3. EDITAR EVENTO (AHORA USA POST, NO PUT)
# ===============================
@csrf_exempt
def editar_evento(request, evento_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        actividad = get_object_or_404(Actividad, id=evento_id)

        actividad.titulo = data.get('title', actividad.titulo)

        hora_str = data.get('time')
        if hora_str:
            actividad.hora = datetime.strptime(hora_str, "%H:%M").time()

        actividad.save()

        return JsonResponse({"message": "Evento actualizado"})

    return HttpResponseNotAllowed(['POST'])


# ===============================
# 4. ELIMINAR EVENTO
# ===============================
@csrf_exempt
def eliminar_evento(request, evento_id):
    if request.method == 'DELETE':
        actividad = get_object_or_404(Actividad, id=evento_id)
        actividad.delete()
        return JsonResponse({"message": "Evento eliminado"})

    return HttpResponseNotAllowed(['DELETE'])
