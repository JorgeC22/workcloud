from distutils.archive_util import make_archive
from ntpath import join
import os
from this import d
from urllib import response
import uuid
from xmlrpc.client import boolean
import requests
import json
from datetime import datetime
import base64
from flask import *
#ec2-54-188-33-247.us-west-2.compute.amazonaws.com:8080/

host = "localhost:8080"

def inicioProceso():
    baseUrl = "http://"+host+"/engine-rest/process-definition/key/Process_0w2618a/start"
    data = {
        "variables": {
            "datosProceso": {
                "value": "{\"documentos\": [], \"contrato\": {}}",
                "type": "String"
            }
        } 
    }

    respuesta = requests.post(baseUrl, json=data)
    instanciaProceso = respuesta.json()
    print(instanciaProceso)



def getProcesos():
    baseUrl = "http://"+host+"/engine-rest/process-instance"
    data ={
        "processDefinitionKey":"Process_0w2618a"
    }
    respuesta = requests.post(baseUrl, json=data)
    procesos_json = respuesta.json()
    return procesos_json



def getactividadProcesos(procesos):
    listProcesos = procesos
    for p in procesos:
        #print(p['idproceso'])
        baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(p['id'])+"/activity-instances"
        respuesta = requests.get(baseUrl)
        actividades_json = respuesta.json()
        childActivityInstances = actividades_json['childActivityInstances']
        for a in childActivityInstances:
            #print(childActivityInstances)
            p["tarea"] = a['activityName']
      
    return listProcesos

def getProcesoActividad(data):
    Proceso = data
    #print(p['idproceso'])
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(Proceso['id'])+"/activity-instances"
    respuesta = requests.get(baseUrl)
    actividades_json = respuesta.json()
    childActivityInstances = actividades_json['childActivityInstances']
    for a in childActivityInstances:
        #print(childActivityInstances)
        Proceso["tarea"] = a['activityName']
      
    return Proceso
#a['activityName']

def gettask(idproceso):
    baseUrl = "http://"+host+"/engine-rest/task?processInstanceId="+str(idproceso)+""
    respuesta = requests.get(baseUrl)
    como_json = respuesta.json()
    #print(como_json)
    for x in como_json:
        idtask = x['id']
 
    return idtask

def CompleteTask(idtask,dataJson):
    
    if "id" in dataJson:
        dataJson.pop('id')

    print(dataJson)
    baseUrl = "http://"+host+"/engine-rest/task/"+str(idtask)+"/complete"
    jsonD = json.dumps(dataJson)
    #jsonD = jsonD.replace("\"", "\\\"")
    #print(jsonD)
    data = {
        "variables": {
            "datosProceso": {
                "value": ""+jsonD,
                "type": "String"
            }
        }
    }

    respuesta = requests.post(baseUrl, json=data)

    print("La respuesta del servidor es: ")
    print(f"Tarea  Completado: {idtask}")

def filesCompleteTask(idtask,dataJson,jsonFiles):
    
    if "id" in dataJson:
        dataJson.pop('id')

    print(dataJson)
    baseUrl = "http://"+host+"/engine-rest/task/"+str(idtask)+"/complete"
    jsonD = json.dumps(dataJson)
    #jsonD = jsonD.replace("\"", "\\\"")
    print(jsonD)
    data = {
        "variables": {
            "datosProceso": {
                "value": ""+jsonD,
                "type": "String"
            }
        }
    }


    data['variables'].update(jsonFiles)
    respuesta = requests.post(baseUrl, json=data)
    print("La respuesta del servidor es: ")
    print(f"Tarea  Completado: {idtask}")



############################################################################################
############################################################################################
############################################################################################


def getJsonProceso(idproceso):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idproceso)+"/variables"
    respuesta = requests.get(baseUrl)
    response = respuesta.json()
    datos_json = response['datosProceso']['value']
    datos_json = json.loads(datos_json)
    datos_json['id'] = idproceso

    return datos_json

def getlistJsonProceso(procesos):
    #print(procesos)
    listJsonProcesos = []
    for p in procesos:
        #print(p['id'])
        baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(p['id'])+"/variables"
        respuesta = requests.get(baseUrl)
        response = respuesta.json()
        datos_json = response['datosProceso']['value']
        datos_json = json.loads(datos_json)
        datos_json['id'] = p['id']
        listJsonProcesos.append(datos_json)
        #print(variables_json)
    return listJsonProcesos


def actualizarJSONdocumentos(jsonData,listas):
    for d in jsonData['documentos']:
        for l in listas:
            if d['nombreDoc'] == l[0]:
                d['validacion'] = boolean(l[1])
    return jsonData

def actualizarJSONcontrato(jsonData,listas):
    for l in listas:
        if len(l) > 1:
            jsonData['contrato']['validacion'] = boolean(l[1])
    return jsonData


def crearJsonDocumentos(listas,jsonData):
    #print(jsonData)
    data = []
    for l in listas:
        json = {
            "nombreDoc": l[0],
            "validacion": ""
        }
        data.append(json)
    
    jsonData['documentos'] = data

    #print(jsonData)
    return jsonData

def crearJsonFile(listValues, Files):
    jsons = {}
    for l in listValues:
        archivo = Files.getlist(l[0])
        if archivo[0].filename:
            archivo[0].save("./archivos/"+archivo[0].filename)
            with open("./archivos/"+archivo[0].filename, "rb") as arc:
                code = base64.b64encode(arc.read())

            data = {
                l[0]: {
                    "type": "File",
                    "value": code.decode(),
                    "valueInfo": {
                        "filename": archivo[0].filename,
                        "mimeType": archivo[0].content_type
                    }
                }
            }

            if jsons:
                jsons.update(data)
            else:
                jsons = data

            os.remove("./archivos/"+archivo[0].filename)

    return jsons


def crearJsonContrato(listas,jsonData):
    now = datetime.now()
    for l in listas:
        json = {
            "nombreDoc": l[0],
            "fechaHoraElaboracion": ""+now.strftime('%Y-%m-%d %H:%M:%S'),
            "validacion": ""
        }
    
    jsonData['contrato'] = json
    return jsonData

def fechahoraActividad(procesos):
    
    for p in procesos:
        baseUrl = "http://"+host+"/engine-rest/task?processInstanceId="+str(p['id'])+""
        respuesta = requests.get(baseUrl)
        como_json = respuesta.json()
        #print(como_json)
        for x in como_json:
            p['fechaHora'] = x['created']
    
    return procesos

def cargarArchivo(code):
    baseUrl = "http://"+host+"/engine-rest/process-definition/key/Process_0w2618a/start"
    data = {
        "variables": {
            "archivo": {
                "type": "File",
                "value": code,
                "valueInfo": {
                    "filename": "hola3.pdf",
                    "mimeType": "application/pdf",
                    "encoding": "UTF-8"
                }
            }
        } 
    }

    respuesta = requests.post(baseUrl, json=data)
    instanciaProceso = respuesta.json()
    print(instanciaProceso)

def file():
    baseUrl = "http://"+host+"/engine-rest/process-instance/031a9207-cbb3-11ec-ab2c-b05adacf4ec1/variables/file/data"
    respuesta = requests.get(baseUrl)
    #instanciaProceso = respuesta.json()
    print(respuesta.reason)
    print("#######################################")
    #print(respuesta.content)
    #encabezado = respuesta.headers
    #body = respuesta.content

    return respuesta

def getObjectResponseFile(idproceso,variable):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idproceso)+"/variables/"+str(variable)+"/data"
    respuesta = requests.get(baseUrl)
    return respuesta

def infoFile(idproceso,variable):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idproceso)+"/variables/"+str(variable)+""
    respuesta = requests.get(baseUrl)
    dataFile = respuesta.json()
    return dataFile