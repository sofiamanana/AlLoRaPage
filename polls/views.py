from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import functions
from django.template import loader
from pathlib import Path
import json
import functions
import numpy as np
import requests
import classes

def getNodos(request):

    response = requests.get('http://127.0.0.1:8002/api/nodes/')
    data = response

    if response.status_code == 200:
        data = response.json()
        print(data['nodes'])
        rows = functions.rowsToNodo(data)

        nodo = request.GET.get('nodo')

        if nodo:
            active = request.GET.get('active')
            mesh = request.GET.get('mesh')
            erase = request.GET.get('erase')

            if active:
                response = requests.post('http://127.0.0.1:8002/api/setActiveNode/',data={'nodo': nodo}) 
                data = response
                if response.status_code == 200: 
                    data = response.json()
                    rows = functions.rowsToNodo(data)
                    return redirect('getNodos')
            if mesh:
                response = requests.post('http://127.0.0.1:8002/api/setMeshNode/',data={'nodo': nodo}) 
                data = response
                if response.status_code == 200:
                    data = response.json()
                    rows = functions.rowsToNodo(data)
                    return redirect('getNodos')
            if erase:
                response = requests.post('http://127.0.0.1:8002/api/deleteNode/',data={'nodo': nodo}) 
                data = response
                if response.status_code == 200:
                    data = response.json()
                    rows = functions.rowsToNodo(data)
                    return redirect('getNodos')
    else:
        rows = []

    if request.method == 'POST':
        name = request.POST.get('name')
        mac_address = request.POST.get('mac_address')
        sleep_mesh = request.POST.get('sleep_mesh')
        active = request.POST.get('active')

        nodo = {
            'name': name,
            'mac_address': mac_address,
            'sleep_mesh': sleep_mesh,
            'active': active,
        }

        response = requests.post('http://127.0.0.1:8002/api/deleteNode/',data={'name': name}) 
        data = response.json()

        if response.status_code == 200:
            response = requests.get('http://127.0.0.1:8002/api/getNode/',data={'name': name}) 
            data = response.json()
            if response.status_code == 200:
                if data["node"]:
                    response = requests.post('http://127.0.0.1:8002/api/updateNode/',data=nodo) 
                    data = response
                    if response.status_code == 200:
                        data = response.json()
                        rows = functions.rowsToNodo(data)
                        return redirect('getNodos')
                else:
                    response = requests.post('http://127.0.0.1:8002/api/addNode/',data=nodo) 
                    data = response
                    print(nodo)
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
        response = requests.get('http://127.0.0.1:8002/api/gateway/')
        data = response

        if response.status_code == 200:
            response2 = requests.get('http://127.0.0.1:8002/api/getState/')
            state = response2.json()["state"]
            data = response.json()
            gateway = functions.jsonToGateway(data, state)
        else:
            gateway = []

        response = requests.get('http://127.0.0.1:8002/api/nodes/')
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
            response = requests.get('http://127.0.0.1:8002/api/activateg/')
            data = response
            return redirect('getGateway')
        stop = request.GET.get('stop')
        if stop:
            response = requests.get('http://127.0.0.1:8002/api/deactivateg/')
            data = response
            return redirect('getGateway')

        reload = request.GET.get('reload')
        if reload:
            response = requests.get('http://127.0.0.1:8002/api/getState/')
            state = response.json()["state"]
            if state:

                response = requests.get('http://127.0.0.1:8002/api/restartGateway/')
                
            else:
                response = requests.get('http://127.0.0.1:8002/api/activateg/')
                
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
        response = requests.get('http://127.0.0.1:8002/api/getNode/',data={'name': name}) 
        data = response.json()
        if response.status_code == 200:
            nodo = data["node"]
            if nodo:
                name = nodo['name']
                mac_address = nodo['mac_address']
                sleep_mesh = nodo['sleep_mesh']
                active = nodo['active']
            else:
                name = ''
                mac_address = ''
                sleep_mesh = ''
                active = ''

    context = {
        'name': name,
        'mac_address': mac_address,
        'sleep_mesh': sleep_mesh,
        'active': active,
    }

    return render(request, "addnode.html", context)

def getData(request):
    context = {
        'data': 'data',
    }
    return render(request, "data.html", context)