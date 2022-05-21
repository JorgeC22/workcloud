import os
import uuid
from xmlrpc.client import boolean
import requests
import json
from datetime import datetime, timedelta
import base64
from flask import *
from conexion import *

host = "localhost:8080"

##Funciones que permiten obtener una lista de las instancias de procesos existentes y la actividad en la que se ubican.
def getProcesos():
    baseUrl = "http://"+host+"/engine-rest/process-instance?processDefinitionKey=Process_0w2618a"
    response = requests.get(baseUrl)
    procesosJson = response.json()
    return procesosJson



def getactividadProcesos(procesos):
    nuevaListaProcesos = []
    for p in procesos:
        baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(p['id'])+"/activity-instances"
        response = requests.get(baseUrl)
        actividadesJson = json.loads(response.content)
        childActivityInstances = actividadesJson['childActivityInstances']
        
        for a in childActivityInstances:
            data = dict(p).copy()
            data["tarea"] = {
                "idActividad": a['id'], 
                "nombreActividad": a['activityName']
            }
            nuevaListaProcesos.append(data)
    
    return nuevaListaProcesos

def getProcesoActividad(jsonProceso):
    Proceso = jsonProceso
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(Proceso['id'])+"/activity-instances"
    response = requests.get(baseUrl)
    actividadJson = response.json()
    childActivityInstances = actividadJson['childActivityInstances']
    for a in childActivityInstances:
        Proceso["tarea"] = {
            "idActividad": a['id'], 
            "nombreActividad": a['activityName']
        }
      
    return Proceso

##Funciones que permiten obtener informacion y concluir las tareas de una Instancia de proceso.
def getTaskProcesos(jsonProceso):
    for j in jsonProceso:
        baseUrl = "http://"+host+"/engine-rest/task?processInstanceId="+str(j['id'])+"&activityInstanceIdIn="+str(j['tarea']['idActividad'])+""
        response = requests.get(baseUrl)
        taskJson = response.json()
        for x in taskJson:
            j['idtask'] = x['id']

    return jsonProceso


def getTaskProceso(idProceso):
    baseUrl = "http://"+host+"/engine-rest/task"
    data = {
            "processInstanceId": idProceso
        }
    response = requests.post(baseUrl, json=data)
    taskJson = response.json()

    for tj in taskJson:
        idTask = tj['id']

    return idTask


def CompleteTask(idTask,dataJson):
    
    #if "id" in dataJson:
    #    dataJson.pop('id')
    if "tarea" in dataJson:
        dataJson.pop('tarea')
    baseUrl = "http://"+host+"/engine-rest/task/"+str(idTask)+"/complete"
    jsonD = json.dumps(dataJson)
    data = {
        "variables": {
            "datosProceso": {
                "value": ""+jsonD,
                "type": "String"
            }
        }
    }

    response = requests.post(baseUrl, json=data)

    print("La respuesta del servidor es: ")
    print(f"Tarea  Completado: {idTask}")

def filesCompleteTask(idTask,dataJson,jsonFiles):
    
    #if "id" in dataJson:
    #    dataJson.pop('id')
    if "tarea" in dataJson:
        dataJson.pop('tarea')
    baseUrl = "http://"+host+"/engine-rest/task/"+str(idTask)+"/complete"
    jsonD = json.dumps(dataJson)
    data = {
        "variables": {
            "datosProceso": {
                "value": ""+jsonD,
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
    respuesta = requests.get(baseUrl)
    response = respuesta.json()
    datosJson = response['datosProceso']['value']
    datosJson = json.loads(datosJson)
    datosJson['id'] = idProceso

    return datosJson

def getlistJsonProceso(procesos):
    listJsonProcesos = []
    for p in procesos:
        #print(p['id'])
        baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(p['id'])+"/variables"
        respuesta = requests.get(baseUrl)
        response = respuesta.json()
        datosJson = response['datosProceso']['value']
        datosJson = json.loads(datosJson)
        datosJson['id'] = p['id']
        listJsonProcesos.append(datosJson)
    return listJsonProcesos


#Funciones para actualizar el json segun la seccion.
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

def actualizarJSONcuenta(jsonData,jsonForm):
    for f in jsonForm.keys():
        key = f
    jsonData['cuentaCliente'][f] = jsonForm[f]
    return jsonData


#Creacion de json segun la seccion.
def crearJsonCliente(jsonForm):
    json = {
        "razonSocial": jsonForm['razonSocial'],
        "rfc": jsonForm['rfcProspecto'],
        "email": jsonForm['correoProspecto'],
        "distribuidor": jsonForm['distribuidor'],
        "grupoTrabajo": "GTprueba"
    }
    return json

def crearJsonDocumentos(listas,jsonData):
    data = []
    for l in listas:
        json = {
            "nombreDoc": l[0],
            "validacion": ""
        }
        data.append(json)
    
    jsonData['documentos'] = data
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
    
    for p in procesos:
        baseUrl = "http://"+host+"/engine-rest/task?processInstanceId="+str(p['id'])+""
        respuesta = requests.get(baseUrl)
        como_json = respuesta.json()
        for x in como_json:
            p['fechaHora'] = x['created']
    return procesos


##Funciones manipulacion de Archivos Camunda
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
    #print(instanciaProceso)

def getObjectResponseFile(idproceso,variable):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idproceso)+"/variables/"+str(variable)+"/data"
    respuesta = requests.get(baseUrl)
    return respuesta

def infoFile(idproceso,variable):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idproceso)+"/variables/"+str(variable)+""
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
    respuesta = requests.post(baseUrl, json=data)
    dataFile = respuesta.json()
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

        print(usuarioProspecto)

    return usuarioProspecto

def extraerNombreUsuarioMedianteCorreo(correoProspecto):
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select nombre from usuarios where correo = '{correoProspecto}';")
        resultadoSql = cursor.fetchall()

        for r in resultadoSql:
            usuarioProspecto = r[0]

    return usuarioProspecto

def extraerGruposUser(idUsuarioProspecto):
    grupos = []
    baseUrl = "http://"+host+"/engine-rest/identity/groups?userId="+idUsuarioProspecto+""
    respuesta = requests.get(baseUrl)
    gruposJson = respuesta.json()

    for g in gruposJson['groups']:
        grupos.append(g['name'])
    
    return grupos

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

def getActividadesGrupos(listaGrupos):
    baseUrl = "http://"+host+"/engine-rest/task"
    listaActividades = []
    for g in listaGrupos:
        data = {
            "candidateGroup": g,
            "includeAssignedTasks": True
        }
        respuesta = requests.post(baseUrl, json=data)
        dataFile = respuesta.json()
        
        for d in dataFile:
            if (len(listaActividades) == 0):
                listaActividades.append(d['name'])
            else:
                for l in listaActividades:
                    if (d['name'] != l):
                        existencia = False
                    else:
                        existencia = True
                        break
            
                if existencia == False:
                    listaActividades.append(d['name'])

    return listaActividades

def filtroProcesos(listaProcesos,ListaActividades):
    listaProcesosFiltrada = []
    for lp in listaProcesos:
        for la in ListaActividades:
            if lp['tarea']['nombreActividad'] == la:
                listaProcesosFiltrada.append(lp)

    return listaProcesosFiltrada


##Funciones para la creacion de usuarios en Camunda.
def crearUsuario(session):
    baseUrl = "http://"+host+"/engine-rest/user/create"
    usuarioProspecto = session['correoProspecto'].replace("@", "")
    usuarioProspecto = usuarioProspecto.replace(".", "")
    data = {
        "profile": {
            "id": usuarioProspecto,
            "firstName": "",
            "lastName": "",
            "email": session['correoProspecto']
        },
        "credentials": {
            "password": usuarioProspecto
        }
    }
    respuesta = requests.post(baseUrl, json=data)

    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select id from usuarios where nombre = '{usuarioProspecto}';")
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
                            values({nuevoIdUsuario},'{usuarioProspecto}','{session['correoProspecto']}',0);""")
            else:
                cursor.execute(f"""insert into usuarios (id,nombre,correo,activo)
                            values(1,'{usuarioProspecto}','{session['correoProspecto']}',0);""")
            
            conexion.commit()

    return usuarioProspecto


def asignarGrupoProspectos(usuarioProspecto):
    

    baseUrl = "http://"+host+"/engine-rest/group/Prospectos/members/"+str(usuarioProspecto)+""
    respuesta = requests.put(baseUrl)
    print(respuesta)

    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"update usuarios set rol = 'Prospectos' where nombre = '{usuarioProspecto}';")
        conexion.commit()
    
    return True



#Funcion para el inicio de un proceso.
def iniciarProceso(jsonCliente,usuario):
    cadena = str(jsonCliente)
    cadena = cadena.replace("\'","\"")
    baseUrl = "http://"+host+"/engine-rest/process-definition/key/Process_0w2618a/start"
    data = {
        "variables": {
            "datosProceso": {
                "value": "{\"cliente\": "+str(cadena)+", \"documentos\": [], \"contrato\": {}, \"comision\": {}, \"cuentaCliente\": {}}",
                "type": "String"
            },
            "idUsuarioProspecto": {
                "value": usuario,
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
        Proceso = response.json()

    baseUrl = "http://"+host+"/engine-rest/task?processInstanceId="+str(Proceso['id'])+""
    response = requests.get(baseUrl)
    task = response.json()
    
    return idInstanciaProceso


##Funciones para asignar y verificar las tareas a las que fue asigna un usuario.
def asignarUsuarioTarea(jsonProceso,usuario):
    for t in jsonProceso:
        baseUrl = "http://"+host+"/engine-rest/task/"+t['id']+"/assignee"
        data = {
            "userId": usuario
        }

        response = requests.post(baseUrl, json=data)
    return "exito"

def asignarUsuarioListaTareas(jsonTask,usuario):
    for t in jsonTask:
        baseUrl = "http://"+host+"/engine-rest/task/"+t['id']+"/assignee"
        data = {
            "userId": usuario
        }

        response = requests.post(baseUrl, json=data)
    return "exito"

def verificarAsignacion(listaProcesos,usuario):
    print(usuario)
    nuevaListaProcesos = []
    for l in listaProcesos:
        baseUrl = "http://"+host+"/engine-rest/task/"+str(l['idtask'])+""
        response = requests.get(baseUrl)
        task = response.json()
        print(task)
        if task['assignee'] == usuario:
            print("Esta asignado")
            nuevaListaProcesos.append(l)
        else:
            print("Asignado a otro")

    return nuevaListaProcesos


##Funcion para obtener los mensaje de la notificacion con relacion al Envio de Correos.
def notificacion(idProceso):
    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idProceso)+"/variables"
    respuesta = requests.get(baseUrl)
    response = respuesta.json()
    json = {
        "notificacion": response['mensajeEnvioCorreo']['value']
    }
    return json


##Funciones para validar la existencia de un Usuario.
def validarCorreo(correoProspecto):
    baseUrl = "http://"+host+"/engine-rest/user"
    respuesta = requests.get(baseUrl)
    response = respuesta.json()

    for usuario in response:
        if correoProspecto == usuario['email']:
            idUsuarioProspecto = usuario['id']
            break
        else:
            idUsuarioProspecto = False
    
    return idUsuarioProspecto

def validarRfcProspecto(rfcProspecto):
    conexion = DB()
    with conexion.cursor() as cursor:
        cursor.execute(f"select rfc from razon_social where rfc = '{rfcProspecto}';")
        record = cursor.fetchall()
        print(record)

        if record:
            existeRfcProspecto = True
        else:
            existeRfcProspecto = False

    return existeRfcProspecto

    
##Funcion para obtener datos de un UsuariosProspecto.
def getDatosUsuario(idUsuarioProspectoCamunda):
    baseUrl = "http://"+host+"/engine-rest/user/"+idUsuarioProspectoCamunda+"/profile"
    respuesta = requests.get(baseUrl)
    response = respuesta.json()

    jsonDatosUsuarioProspecto = {
        "emailProspecto": response['email'],
    }

    return jsonDatosUsuarioProspecto


##Funciones para registrar y verificar los Codigos de seguridad para el acceso a la aplicacion.
def registrarTokenUsuarioProspecto(usuarioProspecto,tokenAcceso):
    fechaHoraActualCreacionTokenAcceso = datetime.now()
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
    fechaHoraActual = datetime.now()
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
                    print("Codigo de Seguridad Expirado.")
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

"""    
def registrarProceso(jsonProceso,usuarioProspecto,gruposProspecto,idInstanciaProceso):
    conexion = DB()
    with conexion.cursor() as cursor:

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

            cursor.execute(f"insert into distribuidor values({nuevoIdDistribuidor},'{jsonProceso['distribuidor']}','{jsonProceso['rfc']}');")
        else:
            cursor.execute(f"insert into distribuidor values(100001,'{jsonProceso['distribuidor']}','{jsonProceso['rfc']}');")

        cursor.execute(f"select id from distribuidor where distribuidor = '{jsonProceso['distribuidor']}';")
        resultadoSqldistribuidor = cursor.fetchall()

        for rd in resultadoSqldistribuidor:
            idDistribuidorProceso = rd[0]

        print(idDistribuidorProceso)


        ##Consulta a tabla grupo_trabajo
        cursor.execute(f"select id from grupo_trabajo order by id;")
        resultadoSqlGrupoTrabajo = cursor.fetchall()
        listaIdGrupoTrabajo = []


        if resultadoSqlGrupoTrabajo:
            for rg in resultadoSqlGrupoTrabajo:
                listaIdGrupoTrabajo.append(rg[0])

            longitudListaConsultaGrupoTrabajo = len(listaIdGrupoTrabajo)
            indice = longitudListaConsultaGrupoTrabajo - 1
            ultimoIdGrupoTrabajo = listaIdDistribuidores[indice]
            nuevoIdGrupoTrabajo = ultimoIdGrupoTrabajo + 1
            cursor.execute(f"insert into grupo_trabajo values({nuevoIdGrupoTrabajo},'{jsonProceso['grupoTrabajo']}');")
        else:
            cursor.execute(f"insert into grupo_trabajo values(100001,'{jsonProceso['grupoTrabajo']}');")

        cursor.execute(f"select id from grupo_trabajo where grupo_trabajo = '{jsonProceso['grupoTrabajo']}';")
        resultadoSqlGrupoTrabajo = cursor.fetchall()

        for rgt in resultadoSqlGrupoTrabajo:
            idGrupoTrabajoProceso = rgt[0]

        print(idGrupoTrabajoProceso)


        cursor.execute(f"select Id,nombre from usuarios where nombre = '{usuarioProspecto}' group by nombre;")
        resultadoSql = cursor.fetchall()

        if resultadoSql:
            for ru in resultadoSql:
                
                ##Consulta a tabla razon social
                cursor.execute(f"select id from razon_social order by id;")
                resultadoSqlRazonSocial = cursor.fetchall()
                listaIdRazonSocial = []


                if resultadoSqlRazonSocial:
                    for rzs in resultadoSqlRazonSocial:
                        listaIdRazonSocial.append(rzs[0])

                    longitudListaConsultaRazonSocial = len(listaIdRazonSocial)
                    indice = longitudListaConsultaRazonSocial - 1
                    ultimoIdRazonSocial = listaIdDistribuidores[indice]
                    nuevoIdRazonSocial = ultimoIdRazonSocial + 1
                    cursor.execute(f"insert into razon_social values({nuevoIdRazonSocial},{ru[0]},'{idInstanciaProceso}','{jsonProceso['rfc']}','{jsonProceso['razonSocial']}',{idDistribuidorProceso},{idGrupoTrabajoProceso});")
                else:
                    cursor.execute(f"insert into razon_social values(100001,{ru[0]},'{idInstanciaProceso}','{jsonProceso['rfc']}','{jsonProceso['razonSocial']}',{idDistribuidorProceso},{idGrupoTrabajoProceso});")

                

        conexion.commit()

    return True
"""

def registrarProceso(jsonProceso,usuarioProspecto,idInstanciaProceso):
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

                cursor.execute(f"insert into distribuidor values({nuevoIdDistribuidor},'{jsonProceso['distribuidor']}','{jsonProceso['rfc']}');")
            else:
                cursor.execute(f"insert into distribuidor values(100001,'{jsonProceso['distribuidor']}','{jsonProceso['rfc']}');")

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
            cursor.execute(f"insert into razon_social values({nuevoIdRazonSocial},'{idInstanciaProceso}','{jsonProceso['rfc']}','{jsonProceso['razonSocial']}',{idDistribuidor},{idGrupoTrabajo});")
            cursor.execute(f"insert into usuario_razonsocial values({idUsuario},{nuevoIdRazonSocial});")
        else:
            cursor.execute(f"insert into razon_social values(100001,'{idInstanciaProceso}','{jsonProceso['rfc']}','{jsonProceso['razonSocial']}',{idDistribuidor},{idGrupoTrabajo});")
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

def registrarEvento(idProceso):
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

            if resultadoConsultaEventos:
                for rce in resultadoConsultaEventos:
                    listaIdEventos.append(rce[0])

                longitudListaConsultaEventos = len(listaIdEventos)
                indice = longitudListaConsultaEventos - 1
                ultimoIdEventos = listaIdEventos[indice]
                nuevoIdEvento = ultimoIdEventos + 1

                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values({nuevoIdEvento},'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{jsonRegistroTarea['fechaHoraInicio']}','{jsonRegistroTarea['fechaHoraFin']}');")

            else:
                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values(1,'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{jsonRegistroTarea['fechaHoraInicio']}','{jsonRegistroTarea['fechaHoraFin']}');")

            conexion.commit()


        if "datosRegistroTareaAnteriorRutaProspecto" in responseVariables:
            jsonRegistroTarea = responseVariables['datosRegistroTareaAnteriorRutaProspecto']['value']
            jsonRegistroTarea = json.loads(jsonRegistroTarea)

            cursor.execute(f"select id from usuarios where nombre = '{jsonRegistroTarea['usuarioProspecto']}'")
            resultadoConsultaUsuarios = cursor.fetchall()

            cursor.execute(f"select id from eventos order by id")
            resultadoConsultaEventos = cursor.fetchall()
            listaIdEventos = []

            if resultadoConsultaEventos:
                for rce in resultadoConsultaEventos:
                    listaIdEventos.append(rce[0])

                longitudListaConsultaEventos = len(listaIdEventos)
                indice = longitudListaConsultaEventos - 1
                ultimoIdEventos = listaIdEventos[indice]
                nuevoIdEvento = ultimoIdEventos + 1

                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values({nuevoIdEvento},'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{jsonRegistroTarea['fechaHoraInicio']}','{jsonRegistroTarea['fechaHoraFin']}');")

            else:
                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values(1,'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{jsonRegistroTarea['fechaHoraInicio']}','{jsonRegistroTarea['fechaHoraFin']}');")

            conexion.commit()

        if "datosRegistroTareaAnteriorRutaMesaControl" in responseVariables:
            jsonRegistroTarea = responseVariables['datosRegistroTareaAnteriorRutaMesaControl']['value']
            jsonRegistroTarea = json.loads(jsonRegistroTarea)

            cursor.execute(f"select id from usuarios where nombre = '{jsonRegistroTarea['usuarioProspecto']}'")
            resultadoConsultaUsuarios = cursor.fetchall()

            cursor.execute(f"select id from eventos order by id")
            resultadoConsultaEventos = cursor.fetchall()
            listaIdEventos = []

            if resultadoConsultaEventos:
                for rce in resultadoConsultaEventos:
                    listaIdEventos.append(rce[0])

                longitudListaConsultaEventos = len(listaIdEventos)
                indice = longitudListaConsultaEventos - 1
                ultimoIdEventos = listaIdEventos[indice]
                nuevoIdEvento = ultimoIdEventos + 1

                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values({nuevoIdEvento},'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{jsonRegistroTarea['fechaHoraInicio']}','{jsonRegistroTarea['fechaHoraFin']}');")

            else:
                for rcu in resultadoConsultaUsuarios:
                    cursor.execute(f"insert into eventos values(1,'{jsonRegistroTarea['proceso']}','{rcu[0]}','{jsonRegistroTarea['tarea']}','{jsonRegistroTarea['fechaHoraInicio']}','{jsonRegistroTarea['fechaHoraFin']}');")

            conexion.commit()

    return True


def sendEmail(correoProspecto,tokenAcceso):
    codigo = 865936
    contenidoCorreo = f"""
        <html>
        <body>
            <p>Buen dia.</p>
            <p>Se te hace envio del codigo de seguridad para validar la pertenencia del correo.</p>

            <h2>{tokenAcceso}</h2>
        </body>
        </html>
    """

    url = "https://api.elasticemail.com/v2/email/send"
    data = {
        'from' : 'jcrivera@vitaebeneficios.com',
		'fromName' : 'Alquimia',
		'apikey' : 'F587643D85CC9A48D901A779D7C0639443A1CFA35EC8E942765ACFEAF0A29521E38954549808FA9A3638E3B498050E15',
		'subject' : 'Prueba Notificacion Worlflow',
		'to' : correoProspecto,
		'template' : 'notificacionesWorkflow',
        'merge_encabezado' : "Codigo de Seguridad",
        'merge_contenidoHtml' :  contenidoCorreo,
        'merge_tituloBoton' :  "Link",
        'isTransactional': True
    }

    res = requests.post(url, params = data)
    resp = '' + res.text
    jsonA = json.loads(resp)

    print(jsonA)
    evento = jsonA["success"]
    return

def sendEmailTareasProceso(idProceso,jsonProceso):

    baseUrl = "http://"+host+"/engine-rest/process-instance/"+str(idProceso)+"/variables/datosCorreoNotificacion"
    respuesta = requests.get(baseUrl)
    response = respuesta.json()
    datosJsonCorreo = response['value']
    datosJsonCorreo = json.loads(datosJsonCorreo)

    if datosJsonCorreo['datosCorreo'] != "null":
        contenidoCorreo = f"""
            <html>
            <body>
                <p>Buen dia.</p>
                <p></p>
                <p>{datosJsonCorreo['datosCorreo']['body']}</p>
            </body>
            </html>
        """
        

        url = "https://api.elasticemail.com/v2/email/send"
        data = {
            'from' : 'jcrivera@vitaebeneficios.com',
            'fromName' : 'Alquimia',
            'apikey' : 'F587643D85CC9A48D901A779D7C0639443A1CFA35EC8E942765ACFEAF0A29521E38954549808FA9A3638E3B498050E15',
            'subject' : {datosJsonCorreo['datosCorreo']['subtitle']},
            'to' : jsonProceso['cliente']['email'],
            'template' : 'notificacionesWorkflow',
            'merge_encabezado' : "Codigo de Seguridad",
            'merge_contenidoHtml' :  contenidoCorreo,
            'merge_tituloBoton' :  "Link",
            'isTransactional': True
        }

        res = requests.post(url, params = data)
        resp = '' + res.text
        jsonA = json.loads(resp)

        print(jsonA)
        evento = jsonA["success"]
    
    return


def sendEmailTareas(jsonProceso,tipoNotificacion):
    
    if tipoNotificacion == "Contrato":
        contenidoCorreo = f"""
            <html>
            <body>
                <p>Buen dia.</p>
                <p>Ya puedes descargar el contrato correspondiente a la razon social "{jsonProceso['cliente']['razonSocial']}" asociado al RFC "{jsonProceso['cliente']['rfcProspecto']}\"</p>
                <p>Accede con tu correo asociado al mismo y completar la actividad correspondiente.</p>
            </body>
            </html>
        """
    if tipoNotificacion == "AcuseEnvio":
        contenidoCorreo = f"""
            <html>
            <body>
                <p>Buen dia.</p>
                <p></p>
                <p>Accede con tu correo asociado al mismo y completar la actividad correspondiente.</p>
            </body>
            </html>
        """
    

    url = "https://api.elasticemail.com/v2/email/send"
    data = {
        'from' : 'jcrivera@vitaebeneficios.com',
		'fromName' : 'Alquimia',
		'apikey' : 'F587643D85CC9A48D901A779D7C0639443A1CFA35EC8E942765ACFEAF0A29521E38954549808FA9A3638E3B498050E15',
		'subject' : 'Prueba Notificacion Worlflow',
		'to' : jsonProceso['cliente']['correoProspecto'],
		'template' : 'notificacionesWorkflow',
        'merge_encabezado' : "Codigo de Seguridad",
        'merge_contenidoHtml' :  contenidoCorreo,
        'merge_tituloBoton' :  "Link",
        'isTransactional': True
    }

    res = requests.post(url, params = data)
    resp = '' + res.text
    jsonA = json.loads(resp)

    print(jsonA)
    evento = jsonA["success"]
    return


def extraerDistribuidorMedianteCorreo(correoProspecto):
    conexion = DB()
    with conexion.cursor() as cursor:
        ##Consulta a tabla distribuidor
        cursor.execute(f"""select distribuidor.distribuidor, count(usuarios.correo) 
                            from distribuidor inner join razon_social 
                                inner join usuario_razonsocial 
                                inner join usuarios
                            on (distribuidor.id = razon_social.id_distribuidor)
                                and (razon_social.id = usuario_razonsocial.razon_social)
                                and (usuario_razonsocial.id_usuario = usuarios.id)
                            where usuarios.correo = '{correoProspecto}'
                            order by (distribuidor.distribuidor);""")
        resultadoConsulta = cursor.fetchall()
        
        for rc in resultadoConsulta:
            distribuidorProspecto = rc[0]
 
    return distribuidorProspecto