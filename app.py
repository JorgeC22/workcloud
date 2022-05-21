import base64
from distutils.archive_util import make_archive
from io import BytesIO
from lib2to3.pgen2 import token
from django.http import JsonResponse
from flask import Flask, make_response, render_template, request, redirect, send_file, url_for, flash, jsonify, session
from itsdangerous import json
import controlador
import io
#import magic
from werkzeug.utils import secure_filename
import random


app = Flask(__name__)
app.secret_key = 'dont tell anyone'


@app.route("/")
def index():
    #flash('Mensaje de prueba!')
    return redirect(url_for('acceso'))

@app.route("/startProceso")
def startProceso():
    idproceso = controlador.inicioProceso()
    return redirect(url_for('listaInstancias'))

@app.route("/listaInstancias")
def listaInstancias():
    return render_template('listaInstancias.html')

@app.route("/consultaInstancias", methods=['GET'])
def consultaInstancias():
    procesos = controlador.getProcesos()
    listaProcesos = controlador.getlistJsonProceso(procesos)
    listaProcesos = controlador.getactividadProcesos(listaProcesos)
    listaProcesos = controlador.getTaskProcesos(listaProcesos)
    #listaGrupos = controlador.extraerGruposUser(session['usuario'])
    listaActividades = controlador.getActividadesGrupos(session['grupos'])
    listaProcesos = controlador.filtroProcesos(listaProcesos,listaActividades)
    for g in session['grupos']:
        if g == "Prospectos":
            listaProcesos = controlador.verificarAsignacion(listaProcesos,session['usuario'])
            break
    listaProcesos = controlador.fechahoraActividad(listaProcesos)
    response = jsonify(listaProcesos)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/<pagina>/<idproceso>/<idtask>")
def paginaTarea(pagina,idproceso,idtask):
    return render_template('./paginasTareas/'+pagina+'.html', idproceso=idproceso, idtask=idtask)


@app.route("/consultaJsonDocumentos/<idproceso>/<idtask>", methods=['GET'])
def consultaJsonDocumentos(idproceso,idtask):
    jsonProceso = controlador.getJsonProceso(idproceso)
    response = jsonify(jsonProceso)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/cargarDocumentos/<idproceso>/<idtask>", methods=['POST'])
def cargarDocumentos(idproceso,idtask):
    listas = request.form.listvalues()
    files = request.files
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonDocumentos(listas,jsonProceso)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    jsonFiles = controlador.crearJsonFile(listas,files)
    controlador.filesCompleteTask(idtask,jsonProceso,jsonFiles)
    controlador.registrarEvento(idproceso)
    return redirect(url_for('listaInstancias'))

@app.route("/validarDocumentos/<idproceso>/<idtask>", methods=['POST'])
def validarDocumentos(idproceso,idtask):
    listas = request.form.listvalues()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.actualizarJSONdocumentos(jsonProceso, listas)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    return redirect(url_for('listaInstancias'))


@app.route("/cargarContrato/<idproceso>/<idtask>", methods=['POST'])
def cargarContrato(idproceso,idtask):
    listas = request.form.listvalues()
    files = request.files
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonContrato(listas,jsonProceso)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    jsonFiles = controlador.crearJsonFile(listas,files)
    controlador.filesCompleteTask(idtask,jsonProceso,jsonFiles)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    return redirect(url_for('listaInstancias'))


@app.route("/validarContrato/<idproceso>/<idtask>", methods=['POST'])
def validarContrato(idproceso,idtask):
    listas = request.form.listvalues()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.actualizarJSONcontrato(jsonProceso, listas)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    return redirect(url_for('listaInstancias'))

@app.route("/archivo/<idproceso>/<variable>")
def archivo(idproceso,variable):
    data = controlador.getObjectResponseFile(idproceso,variable)
    informacionArchivo = controlador.infoFile(idproceso,variable)
    return send_file(io.BytesIO(data.content), attachment_filename=informacionArchivo['valueInfo']['filename'], mimetype=informacionArchivo['valueInfo']['mimeType'])

@app.route("/terminarDescarga/<idproceso>/<idtask>", methods=['POST'])
def terminarDescarga(idproceso,idtask):
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    print(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    return redirect(url_for('listaInstancias'))

@app.route("/cargaComisiones/<idproceso>/<idtask>", methods=['POST'])
def cargaComisiones(idproceso,idtask):
    jsonForm = request.form.to_dict()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonComision(jsonForm, jsonProceso)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    return redirect(url_for('listaInstancias'))

@app.route("/cargarDatosCuenta/<idproceso>/<idtask>", methods=['POST'])
def cargarDatosCuenta(idproceso,idtask):
    jsonForm = request.form.to_dict()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonCuenta(jsonForm, jsonProceso)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    return redirect(url_for('listaInstancias'))

@app.route("/cargarFechaRealizado/<idproceso>/<idtask>", methods=['POST'])
def cargarFechaRealizado(idproceso,idtask):
    jsonForm = request.form.to_dict()
    if "señalProcesoFinaliza" in jsonForm:
        jsonProceso = controlador.getJsonProceso(idproceso)
        jsonProceso = controlador.actualizarJSONcuenta(jsonProceso, jsonForm)
        jsonProceso = controlador.getProcesoActividad(jsonProceso)
        controlador.CompleteTask(idtask,jsonProceso)
        controlador.registrarEvento(idproceso)
        controlador.registrarDatosProcesoFinal(jsonProceso,idproceso)
        return redirect(url_for('finalizarProceso', idproceso=idproceso))
    else:
        jsonProceso = controlador.getJsonProceso(idproceso)
        jsonProceso = controlador.actualizarJSONcuenta(jsonProceso, jsonForm)
        jsonProceso = controlador.getProcesoActividad(jsonProceso)
        controlador.CompleteTask(idtask,jsonProceso)
        controlador.registrarEvento(idproceso)
        return redirect(url_for('listaInstancias'))


@app.route("/finalizarProceso/<idproceso>")
def finalizarProceso(idproceso):
    jsonProceso = controlador.getJsonProceso(idproceso)
    idtask = controlador.getTaskProceso(idproceso)
    controlador.CompleteTask(idtask,jsonProceso)
    return redirect(url_for('listaInstancias'))

@app.route("/login")
def login():
    session.clear()
    return render_template('login.html')

@app.route("/autenticando", methods=['POST'])
def autenticando():
    autenticacionUsuario = controlador.auntenticacion(request.form['usuario'],request.form['password'])
    if autenticacionUsuario:
        usuarioGrupos = controlador.extraerGruposUser(request.form['usuario'])
        session['usuario'] = request.form['usuario']
        session['grupos'] = usuarioGrupos
        return redirect(url_for('listaInstancias'))
    else:
        return redirect(url_for('login'))

@app.route("/logout/<distribuidor>")
@app.route("/logout")
def logout(distribuidor = None):
    if session['grupos'][0] == "Prospectos":
        session.clear()
        return redirect(url_for('validarCorreo',distribuidor=distribuidor))
    else:
        session.clear()
        return redirect(url_for('login'))









@app.route("/acceso/<distribuidor>")
def acceso(distribuidor):
    return render_template('acceso.html', distribuidor=distribuidor)


@app.route("/registro")
def registro():
    return render_template('iniciarProceso.html')
    

@app.route("/iniciarProceso", methods=['POST'])
def iniciarProceso():
    jsonForm = request.form.to_dict()
    existeRfcProspecto = controlador.validarRfcProspecto(jsonForm['rfcProspecto'])
    if existeRfcProspecto:
        flash("El RFC introducido ya esta registrado.")
        return redirect(url_for('registro'))
    else:
        jsonProceso = controlador.crearJsonCliente(jsonForm)
        idInstanciaProceso = controlador.iniciarProceso(jsonProceso,session['usuario'])
        controlador.registrarProceso(jsonProceso,session['usuario'],idInstanciaProceso)
        return redirect(url_for('listaInstancias'))

@app.route("/extraerNotificacionEmail/<idproceso>/<idtask>", methods=['GET'])
def extraerNotificacionEmail(idproceso,idtask):
    notificacion = controlador.notificacion(idproceso)
    response = jsonify(notificacion)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response














@app.route("/capturarRFC/<distribuidor>")
def capturarRFC(distribuidor):
    session.clear()
    return render_template('capturarRFC.html',distribuidor=distribuidor)

@app.route("/cargarRfcProspecto/<distribuidor>", methods=['POST'])
def cargarRfcProspecto(distribuidor):
    rfcProspecto = request.form['rfc']
    existeRfcProspecto = controlador.validarRfcProspecto(rfcProspecto)
    codigo = ""
    if existeRfcProspecto:
        session['rfcProspecto'] = rfcProspecto
        correoProspecto = controlador.obtenerCorreoMedianteRfc(session['rfcProspecto'])
        for i in range(6):
            numero = random.randrange(0,9,1)
            codigo = codigo + str(numero)
        tokenAcceso = codigo 
        session['usuario'] = controlador.extraerNombreUsuarioMedianteRfc(session['rfcProspecto'])
        controlador.registrarTokenUsuarioProspecto(session['usuario'],tokenAcceso)
        print(f"Codigo de Seguridad: {tokenAcceso}")

        controlador.sendEmail(correoProspecto,tokenAcceso)
        return redirect(url_for('tokenAccesoExisteRFC',distribuidor=distribuidor))
    else:
        session['rfcProspecto'] = rfcProspecto
        return redirect(url_for('datosEmpresa',distribuidor=distribuidor))

@app.route("/datosEmpresa/<distribuidor>")
def datosEmpresa(distribuidor):
    return render_template('datosEmpresa.html',distribuidor=distribuidor)

@app.route("/cargarDatosEmpresa/<distribuidor>", methods=['POST'])
def cargarDatosEmpresa(distribuidor):
    session['razonSocial'] = request.form['razonSocial']
    session['correoProspecto'] = request.form['correoProspecto']
    session['distribuidor'] = distribuidor
    codigo = ""
    for i in range(6):
        numero = random.randrange(0,9,1)
        codigo = codigo + str(numero)
    tokenAcceso = codigo
    usuarioProspecto = controlador.crearUsuario(session)
    controlador.asignarGrupoProspectos(usuarioProspecto)
    controlador.registrarTokenUsuarioProspecto(usuarioProspecto,tokenAcceso)
    session['usuario'] = usuarioProspecto
    print(f"Codigo de Seguridad: {tokenAcceso}")

    controlador.sendEmail(session['correoProspecto'],tokenAcceso)
    return redirect(url_for('tokenAccesoNoExisteRFC',distribuidor=distribuidor))

@app.route("/validarCorreo/<distribuidor>")
def validarCorreo(distribuidor):
    session.clear()
    return render_template('validarCorreo.html',distribuidor=distribuidor)

@app.route("/tokenAccesoExisteRFC/<distribuidor>")
def tokenAccesoExisteRFC(distribuidor):
    return render_template('tokenAccesoExisteRFC.html',distribuidor=distribuidor)

@app.route("/tokenAccesoNoExisteRFC/<distribuidor>")
def tokenAccesoNoExisteRFC(distribuidor):
    return render_template('tokenAccesoNoExisteRFC.html',distribuidor=distribuidor)

@app.route("/tokenAccesoCorreoProspecto/<distribuidor>")
def tokenAccesoCorreoProspecto(distribuidor):
    return render_template('tokenAccesoCorreoProspecto.html',distribuidor=distribuidor)


@app.route("/evaluarCorreoProspecto/<distribuidor>", methods=['POST'])
def evaluarCorreoProspecto(distribuidor):
    correoProspecto = request.form['correoProspecto']
    existeCorreoProspecto = controlador.validarCorreo(correoProspecto)
    codigo = ""
    if existeCorreoProspecto:
        session['correoProspecto'] = correoProspecto
        for i in range(6):
            numero = random.randrange(0,9,1)
            codigo = codigo + str(numero)
        tokenAcceso = codigo
        usuarioProspecto = controlador.extraerNombreUsuarioMedianteCorreo(session['correoProspecto'])
        controlador.registrarTokenUsuarioProspecto(usuarioProspecto,tokenAcceso)
        session['usuario'] = usuarioProspecto
        print(f"Codigo de Seguridad: {tokenAcceso}")

        controlador.sendEmail(session['correoProspecto'],tokenAcceso)
        return redirect(url_for('tokenAccesoCorreoProspecto',distribuidor=distribuidor))
        #return "Exitoso"
    else:
        return redirect(url_for('validarCorreo',distribuidor=distribuidor))


@app.route("/validarTokenAccesoCorreoExistente/<distribuidor>", methods=['POST'])
def validarTokenAccesoCorreoExistente(distribuidor):
    tokenAcceso = request.form['tokenAcceso']
    tokenAccesoExiste = controlador.validaTokenAcceso(session,tokenAcceso)
    if tokenAccesoExiste:
        session['distribuidor'] = controlador.extraerDistribuidorMedianteCorreo(session['correoProspecto'])
        usuarioGruposProspecto = controlador.extraerGruposUser(session['usuario'])
        session['grupos'] = usuarioGruposProspecto
        session.pop('correoProspecto')
        return redirect(url_for('listaInstancias'))
    else:
        return redirect(url_for('validarCorreo',distribuidor=distribuidor))


@app.route("/validarTokenAccesoRfcExiste/<distribuidor>", methods=['POST'])
def validarTokenAccesoRfcExiste(distribuidor):
    tokenAcceso = request.form['tokenAcceso']
    tokenAccesoExiste = controlador.validaTokenAcceso(session,tokenAcceso)
    if tokenAccesoExiste:
        usuarioGruposProspecto = controlador.extraerGruposUser(session['usuario'])
        session['grupos'] = usuarioGruposProspecto
        session.pop('rfcProspecto')
        return redirect(url_for('listaInstancias',distribuidor=distribuidor))
    else:
        return redirect(url_for('capturarRFC',distribuidor=distribuidor))

@app.route("/validarTokenAccesoRfcNoExiste/<distribuidor>", methods=['POST'])
def validarTokenAccesoRfcNoExiste(distribuidor):
    tokenAcceso = request.form['tokenAcceso']
    tokenAccesoExiste = controlador.validaTokenAcceso(session,tokenAcceso)
    if tokenAccesoExiste:
        usuarioProspecto = session['usuario']

        jsonProceso = controlador.crearJsonCliente(session)
        idInstanciaProceso = controlador.iniciarProceso(jsonProceso,session['usuario'])
        controlador.registrarProceso(jsonProceso,session['usuario'],idInstanciaProceso)
        session.clear()

        usuarioGruposProspecto = controlador.extraerGruposUser(usuarioProspecto)
        session['grupos'] = usuarioGruposProspecto
        session['usuario'] = usuarioProspecto

        controlador.actualizarStatusCuenta(session['usuario'])
        return redirect(url_for('listaInstancias'))
    else:
        flash("EL codigo ingresado es incorrecto o ya no esta vigente.")
        return redirect(url_for('datosEmpresa',distribuidor=distribuidor))



@app.route("/obtenerDatosUsuarioProspecto", methods=['GET'])
def obtenerDatosUsuarioProspecto():
    jsonDatosUsuarioProspecto = controlador.getDatosUsuario(session['usuario'])
    response = jsonify(jsonDatosUsuarioProspecto)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response





if __name__== "__main__":
    app.run(debug=True)
