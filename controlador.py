import os
from re import L
from urllib import response
import uuid
from xmlrpc.client import boolean
import requests
import json
from datetime import datetime, timedelta
from pytz import timezone
import base64
from flask import *
from conexion import *

host = ""

##Funciones que permiten obtener una lista de las instancias de procesos existentes y la actividad en la que se ubican.
def getProcesos():
    baseUrl = "http://"+host+"/engine-rest/process-instance?processDefinitionKey=Mesa_de_control"
    response = requests.get(baseUrl)
    jsonProcesos = response.json()
    return jsonProcesos



def getactividadProcesos(listaJsonProcesos):
    nuevaListaJsonProcesos = []
    for p in listaJsonProcesos:
        baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(p['id'])+"/activity-instances"
        response = requests.get(baseUrl)
        jsonActividadesProceso = json.loads(response.content)
        childActivityInstances = jsonActividadesProceso['childActivityInstances']
        
        for a in childActivityInstances:
            data = dict(p).copy()
            data["tarea"] = {
                "idActividad": a['id'], 
                "nombreActividad": a['activityName']
            }
            nuevaListaJsonProcesos.append(data)
    
    return nuevaListaJsonProcesos

def getProcesoActividad(jsonProceso):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(jsonProceso['id'])+"/activity-instances"
    response = requests.get(baseUrl)
    jsonActividadesProceso = response.json()
    childActivityInstances = jsonActividadesProceso['childActivityInstances']
    for a in childActivityInstances:
        jsonProceso["tarea"] = {
            "idActividad": a['id'], 
            "nombreActividad": a['activityName']
        }
      
    return jsonProceso

##Funciones que permiten obtener informacion y concluir las tareas de una Instancia de proceso.
def getTaskProcesos(listaJsonProcesos):
    nuevaListaJsonProcesos = []
    for ljp in listaJsonProcesos:
        if ljp['tarea']['nombreActividad'] != None:
            baseUrl = "http://"+host+"/engine-rest/task?processInstanceId="+str(ljp['id'])+"&activityInstanceIdIn="+str(ljp['tarea']['idActividad'])+""
            response = requests.get(baseUrl)
            jsonTaskProceso = response.json()
            for jtp in jsonTaskProceso:
                ljp['idtask'] = jtp['id']

            nuevaListaJsonProcesos.append(ljp)


    return nuevaListaJsonProcesos


def getTaskProceso(idProceso):
    baseUrl = "http://"+host+"/engine-rest/task"
    data = {
            "processInstanceId": idProceso
        }
    response = requests.post(baseUrl, json=data)
    jsonTaskProceso = response.json()

    for jtp in jsonTaskProceso:
        idTask = jtp['id']

    return idTask


def CompleteTask(idTask,jsonProceso):
    
    if "id" in jsonProceso:
        jsonProceso.pop('id')
    if "tarea" in jsonProceso:
        jsonProceso.pop('tarea')
    if "candidatoGrupoPerteneciente" in jsonProceso:
        jsonProceso.pop('candidatoGrupoPerteneciente')

    baseUrl = "http://"+host+"/engine-rest/task/"+str(idTask)+"/complete"
    jsonProcesoString = json.dumps(jsonProceso)
    data = {
        "variables": {
            "datosProceso": {
                "value": ""+jsonProcesoString,
                "type": "String"
            }
        }
    }

    response = requests.post(baseUrl, json=data)

    print("La respuesta del servidor es: ")
    print(f"Tarea  Completado: {idTask}")

def filesCompleteTask(idTask,jsonProceso,jsonFiles):
    
    if "id" in jsonProceso:
        jsonProceso.pop('id')
    if "tarea" in jsonProceso:
        jsonProceso.pop('tarea')
    if "candidatoGrupoPerteneciente" in jsonProceso:
        jsonProceso.pop('candidatoGrupoPerteneciente')

    baseUrl = "http://"+host+"/engine-rest/task/"+str(idTask)+"/complete"
    jsonProcesoString = json.dumps(jsonProceso)
    data = {
        "variables": {
            "datosProceso": {
                "value": ""+jsonProcesoString,
                "type": "String"
            }
        }
    }
    data['variables'].update(jsonFiles)
    response = requests.post(baseUrl, json=data)
    print("La respuesta del servidor es: ")
    print(f"Tarea  Completado: {idTask}")

##Funciones para obtener el JSON de una Instancia de Proceso.
def getJsonProceso(idProceso):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idProceso)+"/variables"
    response = requests.get(baseUrl)
    jsonVariablesProceso = response.json()
    jsonDatosProceso = jsonVariablesProceso['datosProceso']['value']
    jsonDatosProceso = json.loads(jsonDatosProceso)
    jsonDatosProceso['id'] = idProceso

    return jsonDatosProceso

def getlistJsonProceso(listaJsonProcesos):
    nuevaListaJsonProcesos = []
    for ljp in listaJsonProcesos:
        baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(ljp['id'])+"/variables"
        response = requests.get(baseUrl)
        jsonVariablesProceso = response.json()
        jsonDatosProceso = jsonVariablesProceso['datosProceso']['value']
        jsonDatosProceso = json.loads(jsonDatosProceso)
        jsonDatosProceso['id'] = ljp['id']
        nuevaListaJsonProcesos.append(jsonDatosProceso)
    return nuevaListaJsonProcesos


#Funciones para actualizar el json segun la seccion.
def actualizarJSONdocumentos(jsonProceso,listasValueForm):
    for d in jsonProceso['documentos']:
        for l in listasValueForm:
            if d['nombreDoc'] == l[0]:
                d['validacion'] = boolean(l[1])
                if len(l) > 2:
                    d['motivoRechazo'] = l[2]
    return jsonProceso

def ingresarLinkAccionistas(jsonProceso,listasValueForm):
    for l in listasValueForm:
        if l[0] == "linkDocumentosAccionistas":
            if l[1] != '':
                data = {
                    "linkDrive": l[1]
                }

                jsonProceso['documentosAccionistas'] = data 
            else:
                data = {
                    "linkDrive": None
                }

                jsonProceso['documentosAccionistas'] = data
                
    return jsonProceso

def actualizarJSONcontrato(jsonProceso,listasValueForm):
    for l in listasValueForm:
        if len(l) > 1:
            jsonProceso['contrato']['validacion'] = boolean(l[1])
            if len(l) > 2:
                jsonProceso['contrato']['motivoRechazoContrato'] = l[2]
                
    return jsonProceso

def actualizarJSONcuenta(jsonProceso,jsonForm):
    for f in jsonForm.keys():
        key = f
    jsonProceso['cuentaCliente'][f] = jsonForm[f]
    return jsonProceso

def agregarFechaEnvioContratoFisico(jsonProceso,jsonForm):
    for jf in jsonForm.keys():
        key = jf
    jsonProceso['contrato'][jf] = jsonForm[jf]
    return jsonProceso

def actualizarJSONenvioContratoOriginalCliente(jsonProceso,jsonForm):
    for f in jsonForm.keys():
        key = f
    jsonProceso['envioContratoOriginalCliente'][f] = jsonForm[f]
    return jsonProceso


#Creacion de json segun la seccion.
def crearJsonCliente(jsonForm):
    json = {
        "razonSocial": jsonForm['razonSocial'],
        "rfc": jsonForm['rfcProspecto'],
        "email": jsonForm['correoProspecto'],
        "distribuidor": jsonForm['distribuidor'],
        "grupoTrabajo": ""
    }
    return json

def crearJsonDocumentos(listasValuesForm,jsonProceso,Files):
    data = []
    
    if len(jsonProceso['documentos']) > 0:
        for lvf in listasValuesForm:
            archivo = Files.getlist(lvf[0])
            if archivo:
                for jp in jsonProceso['documentos']:
                    if lvf[0] == jp['nombreDoc']:
                        listaCaracteresNombreArchivo = list(archivo[0].filename)
                        for r in range(0,archivo[0].filename.find(".")):
                            del listaCaracteresNombreArchivo[0]
                        extensionArchivo = "".join(listaCaracteresNombreArchivo)

                        jp['validacion'] = ""
                        jp['nombreArchivo'] = jsonProceso['cliente']['rfc']+" "+lvf[0]+extensionArchivo
    else:
        for lvf in listasValuesForm:
            archivo = Files.getlist(lvf[0])
            if archivo:
                listaCaracteresNombreArchivo = list(archivo[0].filename)
                for r in range(0,archivo[0].filename.find(".")):
                    del listaCaracteresNombreArchivo[0]
                extensionArchivo = "".join(listaCaracteresNombreArchivo)
                json = {
                    "nombreDoc": lvf[0],
                    "nombreArchivo": jsonProceso['cliente']['rfc']+" "+lvf[0]+extensionArchivo,
                    "validacion": "",
                    "motivoRechazo": ""
                }
                data.append(json)
        jsonProceso['documentos'] = data
    
    return jsonProceso


def crearJsonFile(listaValuesForm, Files, jsonProceso):
    nuevoJson = {}
    for lvf in listaValuesForm:
        archivo = Files.getlist(lvf[0])
        if archivo:
            if archivo[0].filename:
                archivo[0].save("./archivos/"+archivo[0].filename)
                with open("./archivos/"+archivo[0].filename, "rb") as arc:
                    code = base64.b64encode(arc.read())

                listaCaracteresNombreArchivo = list(archivo[0].filename)
                for r in range(0,archivo[0].filename.find(".")):
                    del listaCaracteresNombreArchivo[0]
                extensionArchivo = "".join(listaCaracteresNombreArchivo)
                
                data = {
                    lvf[0]: {
                        "type": "File",
                        "value": code.decode(),
                        "valueInfo": {
                            "filename": jsonProceso['cliente']['rfc']+" "+lvf[0]+extensionArchivo,
                            "mimeType": archivo[0].content_type
                        }
                    }
                }

                if nuevoJson:
                    nuevoJson.update(data)
                else:
                    nuevoJson = data

                os.remove("./archivos/"+archivo[0].filename)
    return nuevoJson


def crearJsonDatosContacto(listaValuesForm,jsonProceso,Files):
    listaDatosContacto = []
    for lvf in listaValuesForm:
        archivo = Files.getlist(lvf[0])
        if archivo:
            print("No existe archivo con ese nombre nodo.")
        else:
            listaDatosContacto.append(lvf)

    jsonDatosContacto = {
        "nombreContacto": listaDatosContacto[0][0],
        "telefonoContacto": listaDatosContacto[1][0],
        "correoContacto": listaDatosContacto[2][0],
        "puestoContacto": listaDatosContacto[3][0]
    }

    jsonProceso['datosContactoProspecto'] = jsonDatosContacto

    return jsonProceso


def crearJsonContrato(listasValuesForm,jsonProceso,Files):
    zonaHoraria = timezone('America/Mexico_City') 
    for lvf in listasValuesForm:
        archivo = Files.getlist(lvf[0])
        if archivo:
            listaCaracteresNombreArchivo = list(archivo[0].filename)
            for r in range(0,archivo[0].filename.find(".")):
                del listaCaracteresNombreArchivo[0]
            extensionArchivo = "".join(listaCaracteresNombreArchivo)

            fechaHoraContratoCargado = datetime.now(zonaHoraria)
            fechaHoraContratoCargadoString = fechaHoraContratoCargado.strftime('%Y-%m-%d %H:%M:%S')

            json = {
                "nombreDoc": lvf[0],
                "nombreArchivo": jsonProceso['cliente']['rfc']+" "+lvf[0]+extensionArchivo,
                "fechaHoraContratoCargado": ""+fechaHoraContratoCargadoString,
                "validacion": "",
                "motivoRechazoContrato": ""
            }
    
    jsonProceso['contrato'] = json
    return jsonProceso

def crearJsonComision(jsonForm, jsonProceso):
    data = {
        "OperacionCuentaEje": {
            "cashIn": {
                "tipo": jsonForm['inTipo'],
                "valor": jsonForm['inCantidad']
            },
            "cashOut": {
                "tipo": ""+jsonForm['outTipo'],
                "valor": jsonForm['outCantidad']
            }
        },
        "operacionMediosPagosAdicionales": {
            "ATM": {
                "comision": jsonForm['atm']
            },
            "tarjtaVisa": {
                "comision": jsonForm['tarjetaVisa']
            },
            "envioRecepcionDivisas": {
                "diferencial": jsonForm['ERD']
            }
        }
    }

    jsonProceso['comision'] = data
    return jsonProceso

def crearJsonCuenta(jsonForm,jsonProceso):
    data = {
        "idCuenta": jsonForm['idCuenta'],
        "CLABE": jsonForm['CLABE'],
        "numeroCuentaAlquimiapay": jsonForm['numeroCuentaAlquimiapay']
    }
    jsonProceso['cuentaCliente'] = data
    return jsonProceso


#Obtener Fecha y Hora de cuando se creo la tarea de un proceso.
def fechahoraActividad(procesos):
    zonaHoraria = timezone('America/Mexico_City')
    
    for p in procesos:
        baseUrl = "http://"+host+"/engine-rest/task?processInstanceId="+str(p['id'])+""
        response = requests.get(baseUrl)
        jsonTaskProceso = response.json()
        for jtp in jsonTaskProceso:
            fechaCreacionTareaString = jtp['created']
            fechaCreacionTareaString = fechaCreacionTareaString.replace("T", " ")
            fechaCreacionTarea = datetime.strptime(fechaCreacionTareaString, '%Y-%m-%d %H:%M:%S.%f%z')
            fechaCreacionTarea = fechaCreacionTarea.astimezone(zonaHoraria)
            nuevaFechaCreacionTareaString = datetime.strftime(fechaCreacionTarea, '%Y-%m-%d %H:%M:%S.%f%z')
            #fechaHora = datetime.strptime(new, '%Y-%m-%d %H:%M:%S')
            #print(fechaHora)
            p['fechaHora'] = nuevaFechaCreacionTareaString[:-12]
    return procesos


##Funciones manipulacion de Archivos Camunda
def cargarArchivo(codeBase64File):
    baseUrl = "http://"+host+"/engine-rest/process-definition/key/Mesa_de_control/start"
    data = {
        "variables": {
            "archivo": {
                "type": "File",
                "value": codeBase64File,
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


## Funciones para obtencion de informacion de archivos en Camunda.
def getObjectResponseFile(idproceso,variableFile):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idproceso)+"/variables/"+str(variableFile)+"/data"
    respuesta = requests.get(baseUrl)
    return respuesta

def infoFile(idproceso,variableFile):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idproceso)+"/variables/"+str(variableFile)+""
    respuesta = requests.get(baseUrl)
    dataFile = respuesta.json()
    return dataFile




##Obtener Informacion de Usuario Camunda.
def auntenticacion(usuario,password):
    baseUrl = "http://"+host+"/engine-rest/identity/verify"
    data = {
        "username": usuario,
        "password": password
    }
    response = requests.post(baseUrl, json=data)
    dataFile = response.json()
    verificacion = dataFile['authenticated']
    return verificacion


def extraerNombreUsuarioMedianteRfc(rfcProspecto):
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select id from razon_social where rfc = '{rfcProspecto}';")
        resultadoSql = cursor.fetchall()

        for r in resultadoSql:
            cursor.execute(f"select id_usuario from usuario_razonsocial where razon_social = '{r[0]}';")
            resultadoSqlUsuarioRazonSocial = cursor.fetchall()


        for rur in resultadoSqlUsuarioRazonSocial:
            idUsuarioProspecto = rur[0]

        cursor.execute(f"select nombre from usuarios where id = '{idUsuarioProspecto}';")
        resultadoSqlUsuarios = cursor.fetchall()

        for ru in resultadoSqlUsuarios:
            usuarioProspecto = ru[0]


    return usuarioProspecto

def extraerNombreUsuarioMedianteCorreo(correoUsuario):
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select nombre from usuarios where correo = '{correoUsuario}';")
        resultadoSql = cursor.fetchall()

        for r in resultadoSql:
            nombreUsuario = r[0]

    return nombreUsuario

def extraerGruposUser(idUsuarioProspecto):
    listaGruposUsuario = []
    baseUrl = "http://"+host+"/engine-rest/identity/groups?userId="+idUsuarioProspecto+""
    response = requests.get(baseUrl)
    jsonGruposUsuario = response.json()

    for jgu in jsonGruposUsuario['groups']:
        listaGruposUsuario.append(jgu['name'])
    
    return listaGruposUsuario

def obtenerCorreoMedianteRfc(rfcProspecto):
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"""select usuarios.correo 
                            from usuarios 
                                inner join usuario_razonsocial 
                                inner join razon_social
                            on (usuarios.id = usuario_razonsocial.id_usuario)
                            and (usuario_razonsocial.razon_social = razon_social.id)
                            where razon_social.rfc = '{rfcProspecto}';""")
        resultadoConsultaCorreo = cursor.fetchall()

        for rcc in resultadoConsultaCorreo:
            correoProspecto = rcc[0]
    
    return correoProspecto

def getActividadesGrupos(listaGruposUsuario):
    baseUrl = "http://"+host+"/engine-rest/task"
    listaActividadesUsuario = []
    for g in listaGruposUsuario:
        data = {
            "candidateGroup": g,
            "includeAssignedTasks": True
        }
        response = requests.post(baseUrl, json=data)
        jsonTaskGrupo = response.json()
        
        for jtg in jsonTaskGrupo:
            if (len(listaActividadesUsuario) == 0):
                listaActividadesUsuario.append(jtg['name'])
            else:
                for lau in listaActividadesUsuario:
                    if (jtg['name'] != lau):
                        existencia = False
                    else:
                        existencia = True
                        break
            
                if existencia == False:
                    listaActividadesUsuario.append(jtg['name'])

    return listaActividadesUsuario

def filtrarListaProcesosMedianteUsuario(listaJsonProcesos,usuario):
    nuevaListaJsonProcesos = []
    baseUrl = "http://"+host+"/engine-rest/task"
    data = {
        "assignee": usuario
    }
    response = requests.post(baseUrl, json=data)
    listaJsonTareasUsuario = response.json()

    for ljtu in listaJsonTareasUsuario:
        for ljp in listaJsonProcesos:
            if ljtu['id'] == ljp['idtask']:
                jsonProceso = dict(ljp).copy()
                nuevaListaJsonProcesos.append(jsonProceso)


    return nuevaListaJsonProcesos

def obtenerCandidatoGrupoListaProcesos(listaJsonProcesos,gruposUsuario):
    baseUrl = "http://"+host+"/engine-rest/task"
    data = {
        "candidateGroup": gruposUsuario[0],
        "includeAssignedTasks": True
    }
    response = requests.post(baseUrl, json=data)
    listaJsonTareas = response.json()
    
    if listaJsonTareas:
        for ljt in listaJsonTareas:
            for lp in listaJsonProcesos:
                if ljt['id'] == lp['idtask']:
                    jsonProceso = lp
                    jsonProceso['candidatoGrupoPerteneciente'] = gruposUsuario[0]
    else:
        for ljp in listaJsonProcesos:
            jsonProceso = ljp
            jsonProceso['candidatoGrupoPerteneciente'] = "Otro"


    for l in listaJsonProcesos:
        if "candidatoGrupoPerteneciente" in l:
            existenciaCandidatoGrupo = True
        else:
            jsonProceso = l
            jsonProceso['candidatoGrupoPerteneciente'] = "Otro"

    return listaJsonProcesos

def filtroProcesos(listaJsonProcesos,listaActividadesUsuario):
    listaProcesosFiltrada = []
    for ljp in listaJsonProcesos:
        for lau in listaActividadesUsuario:
            if ljp['tarea']['nombreActividad'] == lau:
                listaProcesosFiltrada.append(ljp)

    return listaProcesosFiltrada


##Funciones para la creacion de usuarios en Camunda.
def crearUsuario(session):
    baseUrl = "http://"+host+"/engine-rest/user/create"
    correo = session['correoProspecto']
    nombreUsuarioProspecto = ''.join(char for char in correo if char.isalnum())
    data = {
        "profile": {
            "id": nombreUsuarioProspecto,
            "firstName": "",
            "lastName": "",
            "email": session['correoProspecto']
        },
        "credentials": {
            "password": nombreUsuarioProspecto
        }
    }
    response = requests.post(baseUrl, json=data)

    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select id from usuarios where nombre = '{nombreUsuarioProspecto}';")
        resultadoSqlUsuarios = cursor.fetchall()

        if resultadoSqlUsuarios:
            print(f"Usuario con este el correo \"{session['correoProspecto']}\" ya esta creado y registrado.")
        else:
            cursor.execute(f"select id from usuarios order by id;")
            resultadoConsultaUsuarios = cursor.fetchall()
            listaIdUsuarios =[]

            if resultadoConsultaUsuarios:
                for rcu in resultadoConsultaUsuarios:
                    listaIdUsuarios.append(rcu[0])

                longitudListaConsultaEventos = len(listaIdUsuarios)
                indice = longitudListaConsultaEventos - 1
                ultimoIdUsuario = listaIdUsuarios[indice]
                nuevoIdUsuario = ultimoIdUsuario + 1

                cursor.execute(f"""insert into usuarios (id,nombre,correo,activo)
                            values({nuevoIdUsuario},'{nombreUsuarioProspecto}','{session['correoProspecto']}',0);""")
            else:
                cursor.execute(f"""insert into usuarios (id,nombre,correo,activo)
                            values(1,'{nombreUsuarioProspecto}','{session['correoProspecto']}',0);""")
            
            conexion.commit()

    return nombreUsuarioProspecto


def asignarGrupoProspectos(usuarioProspecto):
    

    baseUrl = "http://"+host+"/engine-rest/group/Prospectos/members/"+str(usuarioProspecto)+""
    response = requests.put(baseUrl)

    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"update usuarios set rol = 'Prospectos' where nombre = '{usuarioProspecto}';")
        conexion.commit()
    
    return True



#Funcion para el inicio de un proceso.
def iniciarProceso(jsonCliente,nombreUsuario):
    jsonClienteString = str(jsonCliente)
    jsonClienteString = jsonClienteString.replace("\'","\"")
    baseUrl = "http://"+host+"/engine-rest/process-definition/key/Mesa_de_control/start"
    data = {
        "variables": {
            "datosProceso": {
                "value": "{\"cliente\": "+str(jsonClienteString)+", \"documentos\": [], \"datosContactoProspecto\": {}, \"contrato\": {}, \"comision\": {}, \"cuentaCliente\": {}, \"envioContratoOriginalCliente\": {}}",
                "type": "String"
            },
            "idUsuarioProspecto": {
                "value": nombreUsuario,
                "type": "String"
            }
        } 
    }

    response = requests.post(baseUrl, json=data)
    instanciaProceso = response.json()
    idInstanciaProceso = instanciaProceso['id']

    for l in instanciaProceso['links']:
        baseUrl = l['href']
        response = requests.get(baseUrl)
        jsonDatosProceso = response.json()

    baseUrl = "http://"+host+"/engine-rest/task?processInstanceId="+str(jsonDatosProceso['id'])+""
    response = requests.get(baseUrl)
    listaJsonTaskProceso = response.json()
    
    return idInstanciaProceso


##Funciones para asignar y verificar las tareas a las que fue asigna un usuario.
def asignarUsuarioTarea(jsonProceso,nombreUsuario):
    for t in jsonProceso:
        baseUrl = "http://"+host+"/engine-rest/task/"+t['id']+"/assignee"
        data = {
            "userId": nombreUsuario
        }

        response = requests.post(baseUrl, json=data)
    return "exito"

def asignarUsuarioListaTareas(jsonTask,nombreUsuario):
    for jt in jsonTask:
        baseUrl = "http://"+host+"/engine-rest/task/"+jt['id']+"/assignee"
        data = {
            "userId": nombreUsuario
        }

        response = requests.post(baseUrl, json=data)
    return "exito"

def verificarAsignacion(listaJsonProcesos,nombreUsuario):
    nuevaListaJsonProceso = []
    for l in listaJsonProcesos:
        baseUrl = "http://"+host+"/engine-rest/task/"+str(l['idtask'])+""
        response = requests.get(baseUrl)
        jsonTask = response.json()
        if jsonTask['assignee'] == nombreUsuario:
            nuevaListaJsonProceso.append(l)
        else:
            print("Asignado a otro")

    return nuevaListaJsonProceso


##Funcion para obtener los mensaje de la notificacion con relacion al Envio de Correos.
def notificacion(idProceso):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idProceso)+"/variables"
    response = requests.get(baseUrl)
    jsonVariablesProceso = response.json()
    json = {
        "notificacion": jsonVariablesProceso['mensajeEnvioCorreo']['value']
    }
    return json


##Funciones para validar la existencia de un Usuario.
def validarCorreo(correoUsuario):
    baseUrl = "http://"+host+"/engine-rest/user"
    respuesta = requests.get(baseUrl)
    listaJsonUsuarios = respuesta.json()

    for usuario in listaJsonUsuarios:
        if correoUsuario == usuario['email']:
            nombreUsuario = usuario['id']
            break
        else:
            nombreUsuario = False

    print(nombreUsuario)

    if nombreUsuario != False:
        conexion = DB()
        with conexion.cursor() as cursor:
            cursor.execute(f"select activo from usuarios where nombre = '{nombreUsuario}';")
            resultadoConsultaUsuarios = cursor.fetchall()

            if resultadoConsultaUsuarios:
                for rcu in resultadoConsultaUsuarios:
                    numeroBytes = rcu[0]
                    numeroEntero = int.from_bytes(numeroBytes, "big")
                    if numeroEntero == 1:
                        nombreUsuario = usuario['id']
                        break
                    else:
                        nombreUsuario = False
            else:
                print("No hubo resultado de consulta.")
                nombreUsuario = False

    print(nombreUsuario)
    return nombreUsuario

def validarRfcProspecto(rfcProspecto):
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select rfc from razon_social where rfc = '{rfcProspecto}';")
        record = cursor.fetchall()

        if record:
            existeRfcProspecto = True
        else:
            existeRfcProspecto = False

    return existeRfcProspecto

    
##Funcion para obtener datos de un UsuariosProspecto.
def getDatosUsuario(nombreUsuarioProspecto):
    baseUrl = "http://"+host+"/engine-rest/user/"+nombreUsuarioProspecto+"/profile"
    response = requests.get(baseUrl)
    jsonDatosUsuario = response.json()

    jsonDatosUsuarioProspecto = {
        "emailProspecto": jsonDatosUsuario['email'],
    }

    return jsonDatosUsuarioProspecto


##Funciones para registrar y verificar los Codigos de seguridad para el acceso a la aplicacion.
def registrarTokenUsuarioProspecto(usuarioProspecto,tokenAcceso):
    zonaHoraria = timezone('America/Mexico_City')
    fechaHoraActualCreacionTokenAcceso = datetime.now(zonaHoraria)
    fechaHoraExpiracionTokenAcceso = (fechaHoraActualCreacionTokenAcceso + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
    fechaHoraActualCreacionTokenAcceso = fechaHoraActualCreacionTokenAcceso.strftime('%Y-%m-%d %H:%M:%S')
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select Id from usuarios where nombre = '{usuarioProspecto}';")
        record = cursor.fetchall()

        for r in record:
            cursor.execute(f"select * from token where id_usuario = '{r[0]}';")
            existeFilaTokenProspecto = cursor.fetchall()

            if existeFilaTokenProspecto:
                for r in record:
                    cursor.execute(f"""update token 
                                        set Token = '{tokenAcceso}', inicio = '{fechaHoraActualCreacionTokenAcceso}', fin = '{fechaHoraExpiracionTokenAcceso}' , 
                                        utilizado = 0 
                                        where id_usuario = '{r[0]}';""")
                    conexion.commit()
            else:
                cursor.execute(f"select id from token order by id;")
                resultadoConsultaToken = cursor.fetchall()
                listaIdToken = []

                if resultadoConsultaToken:
                    for rct in resultadoConsultaToken:
                        listaIdToken.append(rct[0])

                    longitud = len(listaIdToken)
                    indice = longitud - 1
                    ultimoIdToken = listaIdToken[indice]
                    nuevoIdToken = ultimoIdToken + 1

                    for r in record:
                        cursor.execute(f"""insert into token (id,id_usuario,Token,inicio,fin,utilizado) 
                                            values({nuevoIdToken},'{r[0]}','{tokenAcceso}','{fechaHoraActualCreacionTokenAcceso}','{fechaHoraExpiracionTokenAcceso}',0);""")
                else:
                    for r in record:
                        cursor.execute(f"""insert into token (id,id_usuario,Token,inicio,fin,utilizado) 
                                            values(1,'{r[0]}','{tokenAcceso}','{fechaHoraActualCreacionTokenAcceso}','{fechaHoraExpiracionTokenAcceso}',0);""")
                
                conexion.commit()

    return True

def validaTokenAcceso(session,tokenAcceso):
    zonaHoraria = timezone('America/Mexico_City')
    fechaHoraActual = datetime.now(zonaHoraria)
    fechaHoraActual = fechaHoraActual.strftime('%Y-%m-%d %H:%M:%S')
    fechaHoraActual = datetime.strptime(fechaHoraActual, '%Y-%m-%d %H:%M:%S')
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select id from usuarios where nombre = '{session['usuario']}';")
        idUsuarioProspecto = cursor.fetchall()

        for x in idUsuarioProspecto:
            cursor.execute(f"select Token,fin,utilizado from token where id_usuario = '{x[0]}';")
            tokenAccesoProspecto = cursor.fetchall()

        for t in tokenAccesoProspecto:
            fechaFin = t[1].strftime('%Y-%m-%d %H:%M:%S')
            fechaHoraExpiracionTokenAcceso = datetime.strptime(fechaFin, '%Y-%m-%d %H:%M:%S')
            if tokenAcceso == str(t[0]):
                if fechaHoraActual > fechaHoraExpiracionTokenAcceso:
                    existeTokenAcceso = False
                else:
                    numeroBytes = t[2]
                    numeroEntero = int.from_bytes(numeroBytes, "big")
                    if numeroEntero == 0:
                        existeTokenAcceso = True
                    else:
                        existeTokenAcceso = False
            else:
                    existeTokenAcceso = False

        for x in idUsuarioProspecto:
            cursor.execute(f"update token set utilizado = 1 where id_usuario = '{x[0]}';")
            conexion.commit()
    
    return existeTokenAcceso

##Para Pruebas
def validarToken(session,tokenAcceso):
    if tokenAcceso == session['tokenAcceso']:
        existeTokenAcceso = True
    else:
        existeTokenAcceso = False
    
    return existeTokenAcceso


def actualizarStatusCuenta(usuariosProspecto):
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"update usuarios set activo = 1 where nombre = '{usuariosProspecto}';")
        conexion.commit()

    return True


def registrarProceso(jsonProceso,usuarioProspecto,idInstanciaProceso,rutaDistribuidor):
    conexion = DB()
    with conexion.cursor() as cursor:

        cursor.execute(f"select id from distribuidor where distribuidor = '{jsonProceso['distribuidor']}';")
        resultadoSqlDistribuidor = cursor.fetchall()

        if resultadoSqlDistribuidor:
            for rd in resultadoSqlDistribuidor:
                idDistribuidor = rd[0]
        else:
            ##Consulta a tabla distribuidor
            cursor.execute(f"select id from distribuidor order by id;")
            resultadoSqldistribuidor = cursor.fetchall()
            listaIdDistribuidores = []


            if resultadoSqldistribuidor:
                for rds in resultadoSqldistribuidor:
                    listaIdDistribuidores.append(rds[0])

                longitudListaConsultaDistribuidor = len(listaIdDistribuidores)
                indice = longitudListaConsultaDistribuidor - 1
                ultimoIdDistribuidor = listaIdDistribuidores[indice]
                nuevoIdDistribuidor = ultimoIdDistribuidor + 1

                cursor.execute(f"insert into distribuidor values({nuevoIdDistribuidor},'{jsonProceso['distribuidor']}',Null,'{rutaDistribuidor}');")
            else:
                cursor.execute(f"insert into distribuidor values(100001,'{jsonProceso['distribuidor']}',Null,'{rutaDistribuidor}');")

            conexion.commit()

            cursor.execute(f"select id from distribuidor where distribuidor = '{jsonProceso['distribuidor']}';")
            resultadoSqldistribuidor = cursor.fetchall()

            for rd in resultadoSqldistribuidor:
                idDistribuidor = rd[0]


        cursor.execute(f"select id from grupo_trabajo where grupo_trabajo = '{jsonProceso['grupoTrabajo']}';")
        resultadoSqlGrupoTrabajo = cursor.fetchall()

        for rgt in resultadoSqlGrupoTrabajo:
            idGrupoTrabajo = rgt[0]

        cursor.execute(f"select Id,nombre from usuarios where nombre = '{usuarioProspecto}' group by nombre;")
        resultadoSqlUsuarios = cursor.fetchall()

        for ru in resultadoSqlUsuarios:
            idUsuario = ru[0]
                
        ##Consulta a tabla razon social
        cursor.execute(f"select id from razon_social order by id;")
        resultadoSqlRazonSocial = cursor.fetchall()
        listaIdRazonSocial = []


        if resultadoSqlRazonSocial:
            for rzs in resultadoSqlRazonSocial:
                listaIdRazonSocial.append(rzs[0])

            longitudListaConsultaRazonSocial = len(listaIdRazonSocial)
            indice = longitudListaConsultaRazonSocial - 1
            ultimoIdRazonSocial = listaIdRazonSocial[indice]
            nuevoIdRazonSocial = ultimoIdRazonSocial + 1
            cursor.execute(f"insert into razon_social values({nuevoIdRazonSocial},'{idInstanciaProceso}','{jsonProceso['rfc']}','{jsonProceso['razonSocial']}',{idDistribuidor},Null,0);")
            cursor.execute(f"insert into usuario_razonsocial values({idUsuario},{nuevoIdRazonSocial});")
        else:
            cursor.execute(f"insert into razon_social values(100001,'{idInstanciaProceso}','{jsonProceso['rfc']}','{jsonProceso['razonSocial']}',{idDistribuidor},Null,0);")
            cursor.execute(f"insert into usuario_razonsocial values({idUsuario},100001);")


        conexion.commit()

    return True

def registrarDatosProcesoFinal(jsonProceso,idproceso):
    conexion = DB()
    with conexion.cursor() as cursor:
        ##Consulta a tabla distribuidor
        cursor.execute(f"select id from razon_social where rfc = '{jsonProceso['cliente']['rfc']}';")
        resultadoConsulta = cursor.fetchall()

        cursor.execute(f"select id from datos_contrato order by id")
        resultadoConsultaDatosContrato = cursor.fetchall()
        listaIdDatosContrato = []

        if resultadoConsultaDatosContrato:
            for rdc in resultadoConsultaDatosContrato:
                listaIdDatosContrato.append(rdc[0])

            longitud = len(listaIdDatosContrato)
            indice = longitud - 1
            ultimoId = listaIdDatosContrato[indice]
            nuevoId = ultimoId + 1

            for r in resultadoConsulta:
                jsonStringProceso = json.dumps(jsonProceso)
                cursor.execute(f"insert into datos_contrato values({nuevoId},'{idproceso}','{r[0]}','{jsonStringProceso}');")
        else:
            for r in resultadoConsulta:
                jsonStringProceso = json.dumps(jsonProceso)
                cursor.execute(f"insert into datos_contrato values(1,'{idproceso}','{r[0]}','{jsonStringProceso}');")

        conexion.commit()
    return True

def actualizarStatusProceso(idProceso):
    conexion = DB()
    with conexion.cursor() as cursor:

        cursor.execute(f"update razon_social set status = 1 where id_instancia_proceso = '{idProceso}';")
        conexion.commit()
    return True


def registrarEventoFinal(jsonEventoTarea):
    zona = timezone('America/Mexico_City')
    conexion = DB()
    with conexion.cursor() as cursor:

        cursor.execute(f"select id from usuarios where nombre = '{jsonEventoTarea['usuarioProspecto']}'")
        resultadoConsultaUsuarios = cursor.fetchall()

        cursor.execute(f"select id from eventos order by id")
        resultadoConsultaEventos = cursor.fetchall()
        listaIdEventos = []

        fechaCreacionTareaString = jsonEventoTarea['fechaHoraInicio']
        fechaCreacionTareaString = fechaCreacionTareaString.replace("T", " ")
        fechaCreacionTarea = datetime.strptime(fechaCreacionTareaString, '%Y-%m-%d %H:%M:%S.%f%z')
        fechaCreacionTarea = fechaCreacionTarea.astimezone(zona)
        nuevaFechaCreacionTareaString = datetime.strftime(fechaCreacionTarea, '%Y-%m-%d %H:%M:%S.%f%z')
        nuevaFechaCreacionTareaString = nuevaFechaCreacionTareaString[:-12]

        fechaFinalizacionTareaString = jsonEventoTarea['fechaHoraFin']
        fechaFinalizacionTareaString = fechaFinalizacionTareaString.replace("T", " ")
        fechaFinalizacionTarea = datetime.strptime(fechaFinalizacionTareaString, '%Y-%m-%d %H:%M:%S.%f%z')
        fechaFinalizacionTarea = fechaFinalizacionTarea.astimezone(zona)
        nuevaFechaFinalizacionTareaString = datetime.strftime(fechaFinalizacionTarea, '%Y-%m-%d %H:%M:%S.%f%z')
        nuevaFechaFinalizacionTareaString = nuevaFechaFinalizacionTareaString[:-12]

        if resultadoConsultaEventos:
            for rce in resultadoConsultaEventos:
                listaIdEventos.append(rce[0])

            longitudListaConsultaEventos = len(listaIdEventos)
            indice = longitudListaConsultaEventos - 1
            ultimoIdEventos = listaIdEventos[indice]
            nuevoIdEvento = ultimoIdEventos + 1

            for rcu in resultadoConsultaUsuarios:
                cursor.execute(f"insert into eventos values({nuevoIdEvento},'{jsonEventoTarea['proceso']}','{rcu[0]}','{jsonEventoTarea['tarea']}','{nuevaFechaCreacionTareaString}','{nuevaFechaFinalizacionTareaString}');")

        else:
            for rcu in resultadoConsultaUsuarios:
                cursor.execute(f"insert into eventos values(1,'{jsonEventoTarea['proceso']}','{rcu[0]}','{jsonEventoTarea['tarea']}','{nuevaFechaCreacionTareaString}','{nuevaFechaFinalizacionTareaString}');")

        conexion.commit()

    return True

def registrarEvento(idProceso):
    zona = timezone('America/Mexico_City')
    conexion = DB()
    with conexion.cursor() as cursor:

        baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idProceso)+"/variables"
        respuesta = requests.get(baseUrl)
        responseVariables = respuesta.json()

        if "datosRegistroTareaAnterior" in responseVariables:
            jsonRegistroTarea = responseVariables['datosRegistroTareaAnterior']['value']
            jsonRegistroTarea = json.loads(jsonRegistroTarea)

            cursor.execute(f"select id from usuarios where nombre = '{jsonRegistroTarea['usuarioProspecto']}'")
            resultadoConsultaUsuarios = cursor.fetchall()

            cursor.execute(f"select id from eventos order by id")
            resultadoConsultaEventos = cursor.fetchall()
            listaIdEventos = []

            fechaCreacionTareaString = jsonRegistroTarea['fechaHoraInicio']
            fechaCreacionTareaString = fechaCreacionTareaString.replace("T", " ")
            fechaCreacionTarea = datetime.strptime(fechaCreacionTareaString, '%Y-%m-%d %H:%M:%S.%f%z')
            fechaCreacionTarea = fechaCreacionTarea.astimezone(zona)
            nuevaFechaCreacionTareaString = datetime.strftime(fechaCreacionTarea, '%Y-%m-%d %H:%M:%S.%f%z')
            nuevaFechaCreacionTareaString = nuevaFechaCreacionTareaString[:-12]

            fechaFinalizacionTareaString = jsonRegistroTarea['fechaHoraFin']
            fechaFinalizacionTareaString = fechaFinalizacionTareaString.replace("T", " ")
            fechaFinalizacionTarea = datetime.strptime(fechaFinalizacionTareaString, '%Y-%m-%d %H:%M:%S.%f%z')
            fechaFinalizacionTarea = fechaFinalizacionTarea.astimezone(zona)
            nuevaFechaFinalizacionTareaString = datetime.strftime(fechaFinalizacionTarea, '%Y-%m-%d %H:%M:%S.%f%z')
            nuevaFechaFinalizacionTareaString = nuevaFechaFinalizacionTareaString[:-12]

            if resultadoConsultaEventos:
                for rce in resultadoConsultaEventos:
                    listaIdEventos.append(rce[0])

                longitudListaConsultaEventos = len(listaIdEventos)
                indice = longitudListaConsultaEventos - 1
                ultimoIdEventos = listaIdEventos[indice]
                nuevoIdEvento = ultimoIdEventos + 1

                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values({nuevoIdEvento},'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{nuevaFechaCreacionTareaString}','{nuevaFechaFinalizacionTareaString}');")

            else:
                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values(1,'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{nuevaFechaCreacionTareaString}','{nuevaFechaFinalizacionTareaString}');")

            conexion.commit()


        if "datosRegistroTareaAnteriorRutaProspecto" in responseVariables:
            jsonRegistroTarea = responseVariables['datosRegistroTareaAnteriorRutaProspecto']['value']
            jsonRegistroTarea = json.loads(jsonRegistroTarea)

            cursor.execute(f"select id from usuarios where nombre = '{jsonRegistroTarea['usuarioProspecto']}'")
            resultadoConsultaUsuarios = cursor.fetchall()

            cursor.execute(f"select id from eventos order by id")
            resultadoConsultaEventos = cursor.fetchall()
            listaIdEventos = []

            fechaCreacionTareaString = jsonRegistroTarea['fechaHoraInicio']
            fechaCreacionTareaString = fechaCreacionTareaString.replace("T", " ")
            fechaCreacionTarea = datetime.strptime(fechaCreacionTareaString, '%Y-%m-%d %H:%M:%S.%f%z')
            fechaCreacionTarea = fechaCreacionTarea.astimezone(zona)
            nuevaFechaCreacionTareaString = datetime.strftime(fechaCreacionTarea, '%Y-%m-%d %H:%M:%S.%f%z')
            nuevaFechaCreacionTareaString = nuevaFechaCreacionTareaString[:-12]

            fechaFinalizacionTareaString = jsonRegistroTarea['fechaHoraFin']
            fechaFinalizacionTareaString = fechaFinalizacionTareaString.replace("T", " ")
            fechaFinalizacionTarea = datetime.strptime(fechaFinalizacionTareaString, '%Y-%m-%d %H:%M:%S.%f%z')
            fechaFinalizacionTarea = fechaFinalizacionTarea.astimezone(zona)
            nuevaFechaFinalizacionTareaString = datetime.strftime(fechaFinalizacionTarea, '%Y-%m-%d %H:%M:%S.%f%z')
            nuevaFechaFinalizacionTareaString = nuevaFechaFinalizacionTareaString[:-12]

            if resultadoConsultaEventos:
                for rce in resultadoConsultaEventos:
                    listaIdEventos.append(rce[0])

                longitudListaConsultaEventos = len(listaIdEventos)
                indice = longitudListaConsultaEventos - 1
                ultimoIdEventos = listaIdEventos[indice]
                nuevoIdEvento = ultimoIdEventos + 1

                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values({nuevoIdEvento},'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{nuevaFechaCreacionTareaString}','{nuevaFechaFinalizacionTareaString}');")

            else:
                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values(1,'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{nuevaFechaCreacionTareaString}','{nuevaFechaFinalizacionTareaString}');")

            conexion.commit()

        if "datosRegistroTareaAnteriorRutaMesaControl" in responseVariables:
            jsonRegistroTarea = responseVariables['datosRegistroTareaAnteriorRutaMesaControl']['value']
            jsonRegistroTarea = json.loads(jsonRegistroTarea)

            cursor.execute(f"select id from usuarios where nombre = '{jsonRegistroTarea['usuarioProspecto']}'")
            resultadoConsultaUsuarios = cursor.fetchall()

            cursor.execute(f"select id from eventos order by id")
            resultadoConsultaEventos = cursor.fetchall()
            listaIdEventos = []

            fechaCreacionTareaString = jsonRegistroTarea['fechaHoraInicio']
            fechaCreacionTareaString = fechaCreacionTareaString.replace("T", " ")
            fechaCreacionTarea = datetime.strptime(fechaCreacionTareaString, '%Y-%m-%d %H:%M:%S.%f%z')
            fechaCreacionTarea = fechaCreacionTarea.astimezone(zona)
            nuevaFechaCreacionTareaString = datetime.strftime(fechaCreacionTarea, '%Y-%m-%d %H:%M:%S.%f%z')
            nuevaFechaCreacionTareaString = nuevaFechaCreacionTareaString[:-12]

            fechaFinalizacionTareaString = jsonRegistroTarea['fechaHoraFin']
            fechaFinalizacionTareaString = fechaFinalizacionTareaString.replace("T", " ")
            fechaFinalizacionTarea = datetime.strptime(fechaFinalizacionTareaString, '%Y-%m-%d %H:%M:%S.%f%z')
            fechaFinalizacionTarea = fechaFinalizacionTarea.astimezone(zona)
            nuevaFechaFinalizacionTareaString = datetime.strftime(fechaFinalizacionTarea, '%Y-%m-%d %H:%M:%S.%f%z')
            nuevaFechaFinalizacionTareaString = nuevaFechaFinalizacionTareaString[:-12]

            if resultadoConsultaEventos:
                for rce in resultadoConsultaEventos:
                    listaIdEventos.append(rce[0])

                longitudListaConsultaEventos = len(listaIdEventos)
                indice = longitudListaConsultaEventos - 1
                ultimoIdEventos = listaIdEventos[indice]
                nuevoIdEvento = ultimoIdEventos + 1

                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values({nuevoIdEvento},'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{nuevaFechaCreacionTareaString}','{nuevaFechaFinalizacionTareaString}');")

            else:
                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values(1,'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{nuevaFechaCreacionTareaString}','{nuevaFechaFinalizacionTareaString}');")

            conexion.commit()

    return True




## Envio de correo (notificacion de codigo de acceso)
def sendEmail(correoProspecto,tokenAcceso,seccionTokenAcceso,rutaDistribuidor = None):
    
    conexion = DB()
    with conexion.cursor() as cursor:

        cursor.execute(f"select inicio,fin from token where Token = {tokenAcceso};")
        resultadoSqlToken = cursor.fetchall()

    for rst in resultadoSqlToken:
        tokenFechaCreado = rst[0]
        tokenFechaVigencia = rst[1]

    contenidoCorreo = f"""
        <html>
        <body>
            <p>Buen dia.</p>
            <p>Se te hace envio del codigo de seguridad para validar la pertenencia del correo.</p>
            <p>Fecha de creacion: {tokenFechaCreado}</p>
            <p>Vigente hasta: {tokenFechaVigencia}.</p>

            <h2>{tokenAcceso}</h2>
        </body>
        </html>
    """

    if seccionTokenAcceso == "noExisteRFC":
        btnEnlace = f"<a rel=\"nofollow\" style=\"font-weight:normal; text-decoration:none; display:inline-block; color: white; font-size:16px;\" href=\"https://altas.alquimiapay.com/{rutaDistribuidor}/tokenAccesoNoExisteRFC\">Validar Correo</a>"
    if seccionTokenAcceso == "ExisteRFC":
        btnEnlace = f"<a rel=\"nofollow\" style=\"font-weight:normal; text-decoration:none; display:inline-block; color: white; font-size:16px;\" href=\"https://altas.alquimiapay.com/{rutaDistribuidor}/tokenAccesoExisteRFC\">Validar Correo</a>"
    if seccionTokenAcceso == "login":
        btnEnlace = f"<a rel=\"nofollow\" style=\"font-weight:normal; text-decoration:none; display:inline-block; color: white; font-size:16px;\" href=\"https://altas.alquimiapay.com/tokenAccesoCorreoUsuario\">Validar Correo</a>"

    url = "https://api.elasticemail.com/v2/email/send"
    data = {
        'from' : 'jcrivera@vitaebeneficios.com',
		'fromName' : 'Alquimia',
		'apikey' : '0CCF441FD6276D0BB56AEE771C46AB9CC888A0DBF8E18D1A525D49B4E2A9DE9C1FC7D81006F3A545F73FF244EF465BF4',
		'subject' : 'Codigo de Seguridad',
		'to' : correoProspecto,
		'template' : 'notificacionesWorkflow',
        'merge_encabezado' : "Codigo de Seguridad",
        'merge_contenidoHtml' :  contenidoCorreo,
        'merge_tituloBoton' :  btnEnlace,
    }

    res = requests.post(url, params = data)
    resp = '' + res.text
    jsonA = json.loads(resp)

    print(jsonA)
    evento = jsonA["success"]
    return


## Funcion para el envio de correo (notificacion de tareas durante el proceso)
def sendEmailTareasProceso(idProceso,jsonProceso):

    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idProceso)+"/variables/datosCorreoNotificacion"
    respuesta = requests.get(baseUrl)
    response = respuesta.json()
    datosJsonCorreo = response['value']
    datosJsonCorreo = json.loads(datosJsonCorreo)

    #Json que contiene los datos para el envio de correo en proceso general.
    if datosJsonCorreo['datosCorreo'] != "null":


        if datosJsonCorreo['datosCorreo']['responsables'] != "Prospectos":
            if "documentosRechazados" in datosJsonCorreo['datosCorreo']:
                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreo']['body']}</p>
                    <ul>
                """


                for d in datosJsonCorreo['datosCorreo']['documentosRechazados']:
                    elementoHtml = f"<li><p><b>{d['documento']}:</b> {d['motivoRechazo']}</p></li>"
                    contenidoCorreo = contenidoCorreo + elementoHtml

                contenidoCorreo = contenidoCorreo + "</ul></body></html>"
            
            else:

                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreo']['body']}</p>
                    </body>
                    </html>
                """

            conexion = DB()
            with conexion.cursor() as cursor:

                cursor.execute(f"select correo,activo from usuarios where rol = '{datosJsonCorreo['datosCorreo']['responsables']}'")
                resultadoConsultaUsuarios = cursor.fetchall()
                Destinatarios = []

                for rcu in resultadoConsultaUsuarios:
                    numeroBytes = rcu[1]
                    numeroEntero = int.from_bytes(numeroBytes, "big")
                    if numeroEntero == 1:
                        Destinatarios.append(rcu[0])
                        print(Destinatarios)
        else:
            if "documentosRechazados" in datosJsonCorreo['datosCorreo']:
                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreo']['body']}</p>
                    <ul>
                """


                for d in datosJsonCorreo['datosCorreo']['documentosRechazados']:
                    elementoHtml = f"<li><p><b>{d['documento']}:</b> {d['motivoRechazo']}</p></li>"
                    contenidoCorreo = contenidoCorreo + elementoHtml

                contenidoCorreo = contenidoCorreo + "</ul></body></html>"
            
            else:

                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreo']['body']}</p>
                    </body>
                    </html>
                """
            
            Destinatarios = jsonProceso['cliente']['email']
            print(Destinatarios)

        btnEnlace = f"<a rel=\"nofollow\" style=\"font-weight:normal; text-decoration:none; display:inline-block; color: white; font-size:16px;\" href=\"https://altas.alquimiapay.com/login\">Login</a>"

        url = "https://api.elasticemail.com/v2/email/send"
        data = {
            'from' : 'jcrivera@vitaebeneficios.com',
            'fromName' : 'Alquimia',
            'apikey' : '0CCF441FD6276D0BB56AEE771C46AB9CC888A0DBF8E18D1A525D49B4E2A9DE9C1FC7D81006F3A545F73FF244EF465BF4',
            'subject' : {datosJsonCorreo['datosCorreo']['subtitle']},
            'to' : Destinatarios,
            'template' : 'notificacionesWorkflow',
            'merge_encabezado' : {datosJsonCorreo['datosCorreo']['subtitle']},
            'merge_contenidoHtml' :  contenidoCorreo,
            'merge_tituloBoton' :  btnEnlace,
        }

        res = requests.post(url, params = data)
        resp = '' + res.text
        jsonA = json.loads(resp)

        print(jsonA)
        evento = jsonA["success"]

    #Json que contiene los datos para el envio de correo sobre la ruta Prospecto.
    if datosJsonCorreo['datosCorreoRutaProspecto'] != "null":


        if datosJsonCorreo['datosCorreoRutaProspecto']['responsables'] != "Prospectos":
            if "documentosRechazados" in datosJsonCorreo['datosCorreoRutaProspecto']:
                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreoRutaProspecto']['body']}</p>
                    <ul>
                """


                for d in datosJsonCorreo['datosCorreoRutaProspecto']['documentosRechazados']:
                    elementoHtml = f"<li><p><b>{d['documento']}:</b> {d['motivoRechazo']}</p></li>"
                    contenidoCorreo = contenidoCorreo + elementoHtml

                contenidoCorreo = contenidoCorreo + "</ul></body></html>"
            
            else:

                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreoRutaProspecto']['body']}</p>
                    </body>
                    </html>
                """

            conexion = DB()
            with conexion.cursor() as cursor:

                cursor.execute(f"select correo,activo from usuarios where rol = '{datosJsonCorreo['datosCorreoRutaProspecto']['responsables']}'")
                resultadoConsultaUsuarios = cursor.fetchall()
                Destinatarios = []

                for rcu in resultadoConsultaUsuarios:
                    numeroBytes = rcu[1]
                    numeroEntero = int.from_bytes(numeroBytes, "big")
                    if numeroEntero == 1:
                        Destinatarios.append(rcu[0])
                        print(Destinatarios)
        else:
            if "documentosRechazados" in datosJsonCorreo['datosCorreoRutaProspecto']:
                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreoRutaProspecto']['body']}</p>
                    <ul>
                """


                for d in datosJsonCorreo['datosCorreoRutaProspecto']['documentosRechazados']:
                    elementoHtml = f"<li><p><b>{d['documento']}:</b> {d['motivoRechazo']}</p></li>"
                    contenidoCorreo = contenidoCorreo + elementoHtml

                contenidoCorreo = contenidoCorreo + "</ul></body></html>"
            
            else:

                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreoRutaProspecto']['body']}</p>
                    </body>
                    </html>
                """
            
            Destinatarios = jsonProceso['cliente']['email']
            print(Destinatarios)
        
        btnEnlace = f"<a rel=\"nofollow\" style=\"font-weight:normal; text-decoration:none; display:inline-block; color: white; font-size:16px;\" href=\"https://altas.alquimiapay.com/login\">Login</a>"

        url = "https://api.elasticemail.com/v2/email/send"
        data = {
            'from' : 'jcrivera@vitaebeneficios.com',
            'fromName' : 'Alquimia',
            'apikey' : '0CCF441FD6276D0BB56AEE771C46AB9CC888A0DBF8E18D1A525D49B4E2A9DE9C1FC7D81006F3A545F73FF244EF465BF4',
            'subject' : {datosJsonCorreo['datosCorreoRutaProspecto']['subtitle']},
            'to' : Destinatarios,
            'template' : 'notificacionesWorkflow',
            'merge_encabezado' : {datosJsonCorreo['datosCorreoRutaProspecto']['subtitle']},
            'merge_contenidoHtml' :  contenidoCorreo,
            'merge_tituloBoton' :  btnEnlace,
        }

        res = requests.post(url, params = data)
        resp = '' + res.text
        jsonA = json.loads(resp)

        print(jsonA)
        evento = jsonA["success"]

    #Json que contiene los datos para el envio de correo sobre la ruta de Mesa de control.
    if datosJsonCorreo['datosCorreoRutaMesaControl'] != "null":


        if datosJsonCorreo['datosCorreoRutaMesaControl']['responsables'] != "Prospectos":
            if "documentosRechazados" in datosJsonCorreo['datosCorreoRutaMesaControl']:
                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreoRutaMesaControl']['body']}</p>
                    <ul>
                """


                for d in datosJsonCorreo['datosCorreoRutaMesaControl']['documentosRechazados']:
                    elementoHtml = f"<li><p><b>{d['documento']}:</b> {d['motivoRechazo']}</p></li>"
                    contenidoCorreo = contenidoCorreo + elementoHtml

                contenidoCorreo = contenidoCorreo + "</ul></body></html>"
            
            else:

                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreoRutaMesaControl']['body']}</p>
                    </body>
                    </html>
                """

            conexion = DB()
            with conexion.cursor() as cursor:

                cursor.execute(f"select correo,activo from usuarios where rol = '{datosJsonCorreo['datosCorreoRutaMesaControl']['responsables']}'")
                resultadoConsultaUsuarios = cursor.fetchall()
                Destinatarios = []

                for rcu in resultadoConsultaUsuarios:
                    numeroBytes = rcu[1]
                    numeroEntero = int.from_bytes(numeroBytes, "big")
                    if numeroEntero == 1:
                        Destinatarios.append(rcu[0])
                        print(Destinatarios)
        else:
            if "documentosRechazados" in datosJsonCorreo['datosCorreoRutaMesaControl']:
                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreoRutaMesaControl']['body']}</p>
                    <ul>
                """


                for d in datosJsonCorreo['datosCorreoRutaMesaControl']['documentosRechazados']:
                    elementoHtml = f"<li><p><b>{d['documento']}:</b> {d['motivoRechazo']}</p></li>"
                    contenidoCorreo = contenidoCorreo + elementoHtml

                contenidoCorreo = contenidoCorreo + "</ul></body></html>"
            
            else:

                contenidoCorreo = f"""
                    <html>
                    <body>
                        <p>Buen dia.</p>
                        <p></p>
                        <p>{datosJsonCorreo['datosCorreoRutaMesaControl']['body']}</p>
                    </body>
                    </html>
                """
            
            Destinatarios = jsonProceso['cliente']['email']
            print(Destinatarios)
        
        btnEnlace = f"<a rel=\"nofollow\" style=\"font-weight:normal; text-decoration:none; display:inline-block; color: white; font-size:16px;\" href=\"https://altas.alquimiapay.com/login\">Login</a>"

        url = "https://api.elasticemail.com/v2/email/send"
        data = {
            'from' : 'jcrivera@vitaebeneficios.com',
            'fromName' : 'Alquimia',
            'apikey' : '0CCF441FD6276D0BB56AEE771C46AB9CC888A0DBF8E18D1A525D49B4E2A9DE9C1FC7D81006F3A545F73FF244EF465BF4',
            'subject' : {datosJsonCorreo['datosCorreoRutaMesaControl']['subtitle']},
            'to' : Destinatarios,
            'template' : 'notificacionesWorkflow',
            'merge_encabezado' : {datosJsonCorreo['datosCorreoRutaMesaControl']['subtitle']},
            'merge_contenidoHtml' :  contenidoCorreo,
            'merge_tituloBoton' :  btnEnlace,
        }

        res = requests.post(url, params = data)
        resp = '' + res.text
        jsonA = json.loads(resp)

        print(jsonA)
        evento = jsonA["success"]
    
    return True





def extraerDistribuidorMedianteRuta(rutaDistribuidor):
    conexion = DB()
    with conexion.cursor() as cursor:
        ##Consulta a tabla distribuidor
        cursor.execute(f"select distribuidor from distribuidor where ruta = '{rutaDistribuidor}';")
        resultadoConsulta = cursor.fetchall()
        
        for rc in resultadoConsulta:
            distribuidorProspecto = rc[0]
 
    return distribuidorProspecto


def extraerRutaDistribuidorMedianteCorreo(correoProspecto):
    conexion = DB()
    with conexion.cursor() as cursor:
        ##Consulta a tabla distribuidor
        cursor.execute(f"""select distribuidor.ruta, count(usuarios.correo) 
                            from distribuidor inner join razon_social 
                                inner join usuario_razonsocial 
                                inner join usuarios
                            on (distribuidor.id = razon_social.id_distribuidor)
                                and (razon_social.id = usuario_razonsocial.razon_social)
                                and (usuario_razonsocial.id_usuario = usuarios.id)
                            where usuarios.correo = '{correoProspecto}'
                            order by (distribuidor.ruta);""")
        resultadoConsulta = cursor.fetchall()
        
        if resultadoConsulta:
            for rc in resultadoConsulta:
                rutaDistribuidor = rc[0]
        else:
            rutaDistribuidor = False
 
    return rutaDistribuidor


def obtenerCandidatoGrupoTarea(listaProcesos):
    baseUrl = "http://"+host+"/engine-rest/group"
    response = requests.get(baseUrl)
    jsonListaGrupos = response.json()
    listaGrupos = []

    for jlg in jsonListaGrupos:
        if jlg['type'] == "workFlow-mesaControl":
            nombreGrupo = jlg['name']
            listaGrupos.append(nombreGrupo)

    for lg in listaGrupos:
        baseUrl = "http://"+host+"/engine-rest/task"
        data = {
            "candidateGroup": lg,
            "includeAssignedTasks": True
        }
        response = requests.post(baseUrl, json=data)
        jsonListaTask = response.json()

        if jsonListaTask:
            for jlt in jsonListaTask:
                for lp in listaProcesos:
                    if jlt['id'] == lp['idtask']:
                        jsonProceso = lp
                        jsonProceso['candidatoGrupoPerteneciente'] = lg

    return listaProcesos


def ocultarCorreo(correoUsuario):
    listCaracteres = list(correoUsuario)
    newString = ""

    for x in range(0,correoUsuario.find("@")-2):
        listCaracteres[x] = "#"

    for c in listCaracteres:
        if newString == "":
            newString = ""+c
        else:
            newString = newString + c

    return newString

def verificarExisteRutaDistribuidor(rutaDistribuidor):
    conexion = DB()
    with conexion.cursor() as cursor:

        cursor.execute(f"select id from distribuidor where ruta = '{rutaDistribuidor}';")
        resultadoConsultaDistribuidor = cursor.fetchall()

        if resultadoConsultaDistribuidor:
            existeRutaDistribuidor = True
        else:
            existeRutaDistribuidor = False

    return existeRutaDistribuidor