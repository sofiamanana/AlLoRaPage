import os
from django.shortcuts import redirect, render
from django.http import FileResponse, HttpResponse, HttpResponseNotFound, JsonResponse
from django.conf import settings
import functions
from django.template import loader
from pathlib import Path
import json
import functions
import numpy as np
import requests
import classes
from django.templatetags.static import static
import io
import zipfile
import shutil

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def getNodos(request):

    response = requests.get('http://servicio1:8000/api/nodes/')
    data = response

    if response.status_code == 200:
        data = response.json()
        rows = functions.rowsToNodo(data)

        nodo = request.GET.get('nodo')

        if nodo:
            active = request.GET.get('active')
            mesh = request.GET.get('mesh')
            erase = request.GET.get('erase')
            download = request.GET.get('download')
            

            if active:
                response = requests.post('http://servicio1:8000/api/setActiveNode/',data={'nodo': nodo}) 
                data = response
                if response.status_code == 200: 
                    data = response.json()
                    rows = functions.rowsToNodo(data)
                    return redirect('getNodos')
            if mesh:
                response = requests.post('http://servicio1:8000/api/setMeshNode/',data={'nodo': nodo}) 
                data = response
                if response.status_code == 200:
                    data = response.json()
                    rows = functions.rowsToNodo(data)
                    return redirect('getNodos')
            if erase:
                response = requests.post('http://servicio1:8000/api/deleteNode/',data={'nodo': nodo}) 
                data = response
                if response.status_code == 200:
                    data = response.json()
                    rows = functions.rowsToNodo(data)
                    return redirect('getNodos')
            if download:
                #limpiar static:
                cur_path = settings.BASE_DIR
                ruta_json = str(Path(cur_path, 'polls/', 'static/data_all/'))
                directorios = next(os.walk(ruta_json))[1]
                for directorio in directorios:
                    ruta_carpeta = Path(ruta_json, directorio)
                    shutil.rmtree(ruta_carpeta)
                cur_path = settings.BASE_DIR
                ruta_json = str(Path(cur_path, 'polls/', 'static/data/'))
                archivos = os.listdir(ruta_json)
                for archivo in archivos:
                    ruta_archivo = Path(ruta_json, archivo)
                    os.remove(ruta_archivo)
                response = requests.get('http://servicio1:8000/api/downloadDataNode/',data={'node': nodo})
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Renderizar la plantilla y pasar la URL del archivo ZIP
                    # Nombre del archivo JSON
                    nombre_archivo = "data.json"
                    cur_path = settings.BASE_DIR
                    ruta_json = str(Path(cur_path, 'polls/', 'static/data/'))
                    ruta_json = str(Path(ruta_json, nombre_archivo))

                    with open(ruta_json, 'w') as archivo:
                        json.dump(data, archivo)
                        
                    with open(ruta_json, "rb") as fprb:
                        response = HttpResponse(fprb.read(), content_type="json")
                        response["Content-Disposition"] = "attachment; filename=data.json"
                        return response
                #AGREGAR CATCH
            
                
        download_all = request.GET.get('download_all')
        if download_all:
            print('download all')
            
            response = requests.get('http://servicio1:8000/api/downloadAll/')
            data = response.json()
            nombre_archivo = "data.json"
            cur_path = settings.BASE_DIR
            ruta_json = Path(cur_path, 'polls/', 'static/data_all/')
            i = 0
            nombres_archivos = []
            for mac in data["mac_address"]:
                nombres_archivos.append(mac)
                ruta = Path(ruta_json, mac)
                ruta.mkdir(parents=True, exist_ok=True)
                ruta_j = str(Path(ruta, nombre_archivo))
                with open(ruta_j, 'w') as archivo:
                    json.dump(data["data"][i], archivo)
                i+=1
            cur_path = settings.BASE_DIR
            ruta_carpeta = Path(cur_path, 'polls/', 'static/data_all/')
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_buffer:
                for root, _, files in os.walk(ruta_carpeta):
                    for archivo in files:
                        ruta_archivo = os.path.join(root, archivo)
                        rel_path = os.path.relpath(ruta_archivo, ruta_carpeta)
                        zip_buffer.write(ruta_archivo, arcname=rel_path)
            response = HttpResponse(buffer.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="files.zip"'
            return response
            

    else:
        rows = []

    if request.method == 'POST':
        print('entreeeee')
        name = request.POST.get('name')
        mac_address = request.POST.get('mac_address')
        sleep_mesh = request.POST.get('sleep_mesh')
        active = request.POST.get('active')
        listening_time = request.POST.get('listening_time')

        nodo = {
            'name': name,
            'mac_address': mac_address,
            'sleep_mesh': sleep_mesh,
            'active': active,
            'listening_time': listening_time
        }
        

        response = requests.get('http://servicio1:8000/api/getNode/',data={'mac_address': mac_address}) 
        data = response.json()
        print('entre2')
        print(data)
        print(nodo)
        if response.status_code == 200:
            if data["node"]:
                response = requests.post('http://servicio1:8000/api/updateNode/',data=nodo) 
                data = response
                print('entre3')
                if response.status_code == 200:
                    data = response.json()
                    rows = functions.rowsToNodo(data)
                    return redirect('getNodos')
            else:
                response = requests.post('http://servicio1:8000/api/addNode/',data=nodo) 
                data = response
                if response.status_code == 200:
                    data = response.json()
                    rows = functions.rowsToNodo(data)
                    return redirect('getNodos')

    context = {
        'nodos': rows,
    }

    return render(request, "nodos.html", context)

def getGateway(request):
    if request.method == 'GET':
        
        response = requests.get('http://servicio1:8000/api/gateway/')
        data = response

        if response.status_code == 200:
            response2 = requests.get('http://servicio1:8000/api/getState/')
            state = response2.json()["state"]
            data = response.json()
            gateway = functions.jsonToGateway(data, state)
        else:
            gateway = []

        response = requests.get('http://servicio1:8000/api/nodes/')
        data = response

        if response.status_code == 200:
            data = response.json()
            print(data['nodes'][0]['name'])
            rows = []
            
            rows = functions.rowsToNodo(data)
            
            names = functions.nodesNames(data)
            values = []
            i = 0
            while i<len(names):
                values.append(round(100/len(names)))
                i+=1
            colores = []
            for nodo in rows:
                if nodo.active:
                    colores.append('#88C139')
                else:
                    colores.append('#878787')

            coordenadas_x = [1, 1, 1, 4, 5]
            coordenadas_y = [10, 20, 10, 25, 20]
        else:
            names = []
            values = []
            colores = []
            coordenadas_x = []
            coordenadas_y = []

        activateg = request.GET.get('activateg')
        if activateg:
            response = requests.get('http://servicio1:8000/api/activateg/')
            data = response
            return redirect('getGateway')
        stop = request.GET.get('stop')
        if stop:
            response = requests.get('http://servicio1:8000/api/deactivateg/')
            data = response
            return redirect('getGateway')

        reload = request.GET.get('reload')
        if reload:
            response = requests.get('http://servicio1:8000/api/getState/')
            state = response.json()["state"]
            if state:

                response = requests.get('http://servicio1:8000/api/restartGateway/')
                
            else:
                response = requests.get('http://servicio1:8000/api/activateg/')
                
            return redirect('getGateway')
            
    context = {
            'gateway': gateway,
            'names': names,
            'values': values,
            'colores': colores,
            'coordenadas_x': coordenadas_x,
            'coordenadas_y': coordenadas_y,
        }
    
    return render(request, "gateway.html", context)
    
def addNode(request):
    if request.method == 'GET':

        name = request.GET.get('name')
        mac_address = request.GET.get('mac_address')
        response = requests.get('http://servicio1:8000/api/getNode/',data={'mac_address': mac_address}) 
        data = response.json()
        if response.status_code == 200:
            nodo = data["node"]
            if nodo:
                name = nodo['name']
                mac_address = nodo['mac_address']
                sleep_mesh = nodo['sleep_mesh']
                active = nodo['active']
                listening_time = nodo['listening_time']
            else:
                name = ''
                mac_address = ''
                sleep_mesh = ''
                active = ''
                listening_time = ''

    context = {
        'name': name,
        'mac_address': mac_address,
        'sleep_mesh': sleep_mesh,
        'active': active,
        'listening_time': listening_time
    }

    return render(request, "addnode.html", context)



