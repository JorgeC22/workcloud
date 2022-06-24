import base64
from io import BytesIO
from flask import Flask, render_template, request, redirect, send_file, url_for, flash, jsonify, session, g
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import controlador
import usuariosDatos
import io
from werkzeug.utils import secure_filename
import random
from models.usuario import usuario
import datetime


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return usuariosDatos.get_by_id(id)


@app.route("/")
def index():
    #flash('Mensaje de prueba!')
    return redirect(url_for('login'))

@app.route("/listaInstancias")
@login_required
def listaInstancias():
    return render_template('listaInstancias.html')

@app.route("/consultaInstancias", methods=['GET'])
@login_required
def consultaInstancias():
    if session['grupos'][0] == "Prospectos" or session['grupos'][0] == "MesaControl":
        jsonProcesos = controlador.getProcesos()
        listaProcesos = controlador.getlistJsonProceso(jsonProcesos)
        listaProcesos = controlador.getactividadProcesos(listaProcesos)
        listaProcesos = controlador.getTaskProcesos(listaProcesos)
        if session['grupos'][0] == "Prospectos":
            listaProcesos = controlador.filtrarListaProcesosMedianteUsuario(listaProcesos,session['usuario'])
        #listaProcesos = controlador.obtenerCandidatoGrupoListaProcesos(listaProcesos,session['grupos'])
        listaProcesos = controlador.obtenerCandidatoGrupoTarea(listaProcesos)
        listaProcesos = controlador.fechahoraActividad(listaProcesos)
        for lp in listaProcesos:
            lp['gruposUsuario'] = session['grupos']
        response = jsonify(listaProcesos)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        jsonProcesos = controlador.getProcesos()
        listaProcesos = controlador.getlistJsonProceso(jsonProcesos)
        listaProcesos = controlador.getactividadProcesos(listaProcesos)
        listaProcesos = controlador.getTaskProcesos(listaProcesos)
        #listaGrupos = controlador.extraerGruposUser(session['usuario'])
        listaActividades = controlador.getActividadesGrupos(session['grupos'])
        listaProcesos = controlador.filtroProcesos(listaProcesos,listaActividades)
        for g in session['grupos']:
            if g == "Prospectos":
                listaProcesos = controlador.verificarAsignacion(listaProcesos,session['usuario'])
                break
        listaProcesos = controlador.obtenerCandidatoGrupoTarea(listaProcesos)
        listaProcesos = controlador.fechahoraActividad(listaProcesos)
        for lp in listaProcesos:
            lp['gruposUsuario'] = session['grupos']
        
        response = jsonify(listaProcesos)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route("/<pagina>/<idproceso>/<idtask>")
@login_required
def paginaTarea(pagina,idproceso,idtask):
    return render_template('./paginasTareas/'+pagina+'.html', idproceso=idproceso, idtask=idtask)


@app.route("/consultaJsonDocumentos/<idproceso>/<idtask>", methods=['GET'])
@login_required
def consultaJsonDocumentos(idproceso,idtask):
    jsonProceso = controlador.getJsonProceso(idproceso)
    response = jsonify(jsonProceso)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/cargarDocumentos/<idproceso>/<idtask>", methods=['POST'])
@login_required
def cargarDocumentos(idproceso,idtask):
    listas = request.form.listvalues()
    files = request.files
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonDocumentos(listas,jsonProceso,files)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    jsonFiles = controlador.crearJsonFile(listas,files,jsonProceso)
    jsonProceso = controlador.crearJsonDatosContacto(listas,jsonProceso,files)
    controlador.filesCompleteTask(idtask,jsonProceso,jsonFiles)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    return redirect(url_for('listaInstancias'))

@app.route("/validarDocumentos/<idproceso>/<idtask>", methods=['POST'])
@login_required
def validarDocumentos(idproceso,idtask):
    listasValueForm = request.form.listvalues()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.actualizarJSONdocumentos(jsonProceso, listasValueForm)
    jsonProceso = controlador.ingresarLinkAccionistas(jsonProceso,listasValueForm)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    return redirect(url_for('listaInstancias'))


@app.route("/cargarContrato/<idproceso>/<idtask>", methods=['POST'])
@login_required
def cargarContrato(idproceso,idtask):
    listas = request.form.listvalues()
    files = request.files
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonContrato(listas,jsonProceso,files)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    jsonFiles = controlador.crearJsonFile(listas,files,jsonProceso)
    controlador.filesCompleteTask(idtask,jsonProceso,jsonFiles)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    return redirect(url_for('listaInstancias'))


@app.route("/validarContrato/<idproceso>/<idtask>", methods=['POST'])
@login_required
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
@login_required
def archivo(idproceso,variable):
    data = controlador.getObjectResponseFile(idproceso,variable)
    informacionArchivo = controlador.infoFile(idproceso,variable)
    return send_file(io.BytesIO(data.content), attachment_filename=informacionArchivo['valueInfo']['filename'], mimetype=informacionArchivo['valueInfo']['mimeType'])

@app.route("/terminarDescarga/<idproceso>/<idtask>", methods=['POST'])
@login_required
def terminarDescarga(idproceso,idtask):
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    return redirect(url_for('listaInstancias'))

@app.route("/cargaComisiones/<idproceso>/<idtask>", methods=['POST'])
@login_required
def cargaComisiones(idproceso,idtask):
    jsonForm = request.form.to_dict()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonComision(jsonForm, jsonProceso)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    return redirect(url_for('listaInstancias'))

@app.route("/cargarDatosCuenta/<idproceso>/<idtask>", methods=['POST'])
@login_required
def cargarDatosCuenta(idproceso,idtask):
    jsonForm = request.form.to_dict()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonCuenta(jsonForm, jsonProceso)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    return redirect(url_for('listaInstancias'))


@app.route("/cargarFechaEnvioContratoFisico/<idproceso>/<idtask>", methods=['POST'])
@login_required
def cargarFechaEnvioContratoFisico(idproceso,idtask):
    jsonForm = request.form.to_dict()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.agregarFechaEnvioContratoFisico(jsonProceso, jsonForm)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    return redirect(url_for('listaInstancias'))


@app.route("/cargarFechaImplantacionUsuario/<idproceso>/<idtask>", methods=['POST'])
@login_required
def cargarFechaImplantacionUsuario(idproceso,idtask):
    jsonForm = request.form.to_dict()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.actualizarJSONcuenta(jsonProceso, jsonForm)
    jsonProceso = controlador.getProcesoActividad(jsonProceso)
    controlador.CompleteTask(idtask,jsonProceso)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    return redirect(url_for('listaInstancias'))


@app.route("/cargaFechaActividadEnvio/<idproceso>/<idtask>", methods=['POST'])
@login_required
def cargaFechaActividadEnvio(idproceso,idtask):
    jsonForm = request.form.to_dict()
    if "señalProcesoFinaliza" in jsonForm:
        jsonForm.pop("señalProcesoFinaliza")
        jsonProceso = controlador.getJsonProceso(idproceso)
        jsonProceso = controlador.actualizarJSONenvioContratoOriginalCliente(jsonProceso, jsonForm)
        jsonProceso = controlador.getProcesoActividad(jsonProceso)
        controlador.CompleteTask(idtask,jsonProceso)
        controlador.registrarDatosProcesoFinal(jsonProceso,idproceso)
        controlador.actualizarStatusProceso(idproceso)
        return redirect(url_for('listaInstancias'))
    else:
        jsonProceso = controlador.getJsonProceso(idproceso)
        jsonProceso = controlador.actualizarJSONenvioContratoOriginalCliente(jsonProceso, jsonForm)
        jsonProceso = controlador.getProcesoActividad(jsonProceso)
        controlador.CompleteTask(idtask,jsonProceso)
        controlador.registrarEvento(idproceso)
        controlador.sendEmailTareasProceso(idproceso,jsonProceso)
        return redirect(url_for('listaInstancias'))

##Seccion de Login
@app.route("/login")
def login():
    return render_template('Login.html')

@app.route("/autenticando", methods=['POST'])
def autenticando():
    correoUsuario = request.form['correoUsuario']
    existeCorreoUsuario = controlador.validarCorreo(correoUsuario)
    codigo = ""
    if existeCorreoUsuario:
        session['correoUsuario'] = correoUsuario
        for i in range(6):
            numero = random.randrange(1,9,1)
            codigo = codigo + str(numero)
        tokenAcceso = codigo
        usuarioOperativo = controlador.extraerNombreUsuarioMedianteCorreo(session['correoUsuario'])
        controlador.registrarTokenUsuarioProspecto(usuarioOperativo,tokenAcceso)
        session['usuario'] = usuarioOperativo
        print(f"Codigo de Seguridad: {tokenAcceso}")
        controlador.sendEmail(session['correoUsuario'],tokenAcceso,"login")
        session['correoUsuarioMascara'] = controlador.ocultarCorreo(session['correoUsuario'])
        return redirect(url_for('tokenAccesoCorreoUsuario'))
    else:
        flash("El correo introducido no esta registrado.")
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))









@app.route("/<distribuidor>")
def acceso(distribuidor):
    existeRutaDistribuidor = controlador.verificarExisteRutaDistribuidor(distribuidor)
    if existeRutaDistribuidor:
        session['rutaDistribuidorAcceso'] = distribuidor
        return render_template('acceso.html', distribuidor=distribuidor)
    else:
        return render_template('rutaNoExiste.html')


@app.route("/registro")
@login_required
def registro():
    return render_template('iniciarProceso.html')
    

@app.route("/iniciarProceso", methods=['POST'])
@login_required
def iniciarProceso():
    jsonForm = request.form.to_dict()
    existeRfcProspecto = controlador.validarRfcProspecto(jsonForm['rfcProspecto'])
    if existeRfcProspecto:
        flash("El RFC introducido ya esta registrado.")
        return redirect(url_for('registro'))
    else:
        jsonProceso = controlador.crearJsonCliente(jsonForm)
        idInstanciaProceso = controlador.iniciarProceso(jsonProceso,session['usuario'])
        controlador.registrarProceso(jsonProceso,session['usuario'],idInstanciaProceso,session['ruta'])
        return redirect(url_for('listaInstancias'))

@app.route("/extraerNotificacionEmail/<idproceso>/<idtask>", methods=['GET'])
def extraerNotificacionEmail(idproceso,idtask):
    notificacion = controlador.notificacion(idproceso)
    response = jsonify(notificacion)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response














@app.route("/<distribuidor>/registroNuevaRazonSocial")
def registroNuevaRazonSocial(distribuidor):
    session.clear()
    return render_template('capturarRFC.html',distribuidor=distribuidor)

@app.route("/<distribuidor>/cargarRfcProspecto", methods=['POST'])
def cargarRfcProspecto(distribuidor):
    rfcProspecto = request.form['rfc']
    existeRfcProspecto = controlador.validarRfcProspecto(rfcProspecto)
    codigo = ""
    if existeRfcProspecto:
        session['rfcProspecto'] = rfcProspecto
        correoProspecto = controlador.obtenerCorreoMedianteRfc(session['rfcProspecto'])
        for i in range(6):
            numero = random.randrange(1,9,1)
            codigo = codigo + str(numero)
        tokenAcceso = codigo 
        session['usuario'] = controlador.extraerNombreUsuarioMedianteRfc(session['rfcProspecto'])
        controlador.registrarTokenUsuarioProspecto(session['usuario'],tokenAcceso)
        print(f"Codigo de Seguridad: {tokenAcceso}")
        session['correoProspecto'] = correoProspecto
        controlador.sendEmail(correoProspecto,tokenAcceso,"ExisteRFC",distribuidor)
        session['correoUsuarioMascara'] = controlador.ocultarCorreo(session['correoProspecto'])
        session['rfcProspectoMascara'] = '#######'+session['rfcProspecto'][-4:]
        return redirect(url_for('tokenAccesoExisteRFC',distribuidor=distribuidor))
    else:
        session['rfcProspecto'] = rfcProspecto
        return redirect(url_for('datosEmpresa',distribuidor=distribuidor))

@app.route("/<distribuidor>/datosEmpresa")
def datosEmpresa(distribuidor):
    return render_template('datosEmpresa.html',distribuidor=distribuidor)

@app.route("/<distribuidor>/cargarDatosEmpresa", methods=['POST'])
def cargarDatosEmpresa(distribuidor):
    session['razonSocial'] = request.form['razonSocial']
    session['correoProspecto'] = request.form['correoProspecto']
    distribuidorProspecto = controlador.extraerDistribuidorMedianteRuta(distribuidor)
    distribuidorUsuario = controlador.extraerRutaDistribuidorMedianteCorreo(session['correoProspecto'])
    if distribuidorUsuario:
        flash("El correo introducido ya esta registrado.")
        return redirect(url_for('datosEmpresa',distribuidor=distribuidor))
    else:
        session['distribuidor'] = distribuidorProspecto
        codigo = ""
        for i in range(6):
            numero = random.randrange(1,9,1)
            codigo = codigo + str(numero)
        tokenAcceso = codigo
        usuarioProspecto = controlador.crearUsuario(session)
        controlador.asignarGrupoProspectos(usuarioProspecto)
        controlador.registrarTokenUsuarioProspecto(usuarioProspecto,tokenAcceso)
        session['usuario'] = usuarioProspecto
        print(f"Codigo de Seguridad: {tokenAcceso}")

        controlador.sendEmail(session['correoProspecto'],tokenAcceso,"noExisteRFC",distribuidor)
        session['correoUsuarioMascara'] = controlador.ocultarCorreo(session['correoProspecto'])
        return redirect(url_for('tokenAccesoNoExisteRFC',distribuidor=distribuidor))

@app.route("/<distribuidor>/tokenAccesoExisteRFC")
def tokenAccesoExisteRFC(distribuidor):
    return render_template('tokenAccesoExisteRFC.html',distribuidor=distribuidor)

@app.route("/<distribuidor>/tokenAccesoNoExisteRFC")
def tokenAccesoNoExisteRFC(distribuidor):
    return render_template('tokenAccesoNoExisteRFC.html',distribuidor=distribuidor)

@app.route("/tokenAccesoCorreoUsuario")
def tokenAccesoCorreoUsuario():
        return render_template('tokenAccesoCorreoUsuario.html')


@app.route("/validarTokenAccesoCorreoExistente", methods=['POST'])
def validarTokenAccesoCorreoExistente():
    
    tokenAcceso = request.form['tokenAcceso']
    tokenAccesoExiste = controlador.validaTokenAcceso(session,tokenAcceso)
    if tokenAccesoExiste:
        usuarioGruposProspecto = controlador.extraerGruposUser(session['usuario'])
        session['grupos'] = usuarioGruposProspecto
        if session['grupos'][0] == "Prospectos":
            session['ruta'] = controlador.extraerRutaDistribuidorMedianteCorreo(session['correoUsuario'])
            session['distribuidor'] = controlador.extraerDistribuidorMedianteRuta(session['ruta'])

        logger_user = usuariosDatos.loggin_user(session['usuario'],session['correoUsuario'])
        login_user(logger_user)
        return redirect(url_for('listaInstancias'))
    else:
        flash("EL codigo ingresado es incorrecto o ya no esta vigente.")
        return redirect(url_for('login'))


@app.route("/<distribuidor>/validarTokenAccesoRfcExiste", methods=['POST'])
def validarTokenAccesoRfcExiste(distribuidor):
    tokenAcceso = request.form['tokenAcceso']
    tokenAccesoExiste = controlador.validaTokenAcceso(session,tokenAcceso)
    if tokenAccesoExiste:
        session['distribuidor'] = controlador.extraerDistribuidorMedianteRuta(distribuidor)
        session['ruta'] = distribuidor
        usuarioGruposProspecto = controlador.extraerGruposUser(session['usuario'])
        session['grupos'] = usuarioGruposProspecto
        session['correoUsuario'] = session['correoProspecto']
        session.pop('rfcProspecto')
        session.pop('correoProspecto')
        session.pop('correoUsuarioMascara')

        logger_user = usuariosDatos.loggin_user(session['usuario'],session['correoUsuario'])
        login_user(logger_user)
        return redirect(url_for('listaInstancias'))
    else:
        return redirect(url_for('capturarRFC',distribuidor=distribuidor))

@app.route("/<distribuidor>/validarTokenAccesoRfcNoExiste", methods=['POST'])
def validarTokenAccesoRfcNoExiste(distribuidor):
    tokenAcceso = request.form['tokenAcceso']
    tokenAccesoExiste = controlador.validaTokenAcceso(session,tokenAcceso)
    if tokenAccesoExiste:
        usuarioProspecto = session['usuario']
        correoUsuario = session['correoProspecto']

        jsonProceso = controlador.crearJsonCliente(session)
        idInstanciaProceso = controlador.iniciarProceso(jsonProceso,session['usuario'])
        controlador.registrarProceso(jsonProceso,session['usuario'],idInstanciaProceso,distribuidor)
        session.clear()

        session['distribuidor'] = controlador.extraerDistribuidorMedianteRuta(distribuidor)
        session['ruta'] = distribuidor
        usuarioGruposProspecto = controlador.extraerGruposUser(usuarioProspecto)
        session['grupos'] = usuarioGruposProspecto
        session['usuario'] = usuarioProspecto
        session['correoUsuario'] = correoUsuario

        controlador.actualizarStatusCuenta(session['usuario'])
        logger_user = usuariosDatos.loggin_user(session['usuario'],session['correoUsuario'])
        login_user(logger_user)
        return redirect(url_for('listaInstancias'))
    else:
        flash("EL codigo ingresado es incorrecto o ya no esta vigente.")
        return redirect(url_for('datosEmpresa',distribuidor=distribuidor))



@app.route("/obtenerDatosUsuarioProspecto", methods=['GET'])
@login_required
def obtenerDatosUsuarioProspecto():
    jsonDatosUsuarioProspecto = controlador.getDatosUsuario(session['usuario'])
    response = jsonify(jsonDatosUsuarioProspecto)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




@app.route("/registrarEvento", methods=['POST'])
def registrarEvento():
    jsonEventoTarea = request.get_json()
    controlador.registrarEventoFinal(jsonEventoTarea)
    return "exitoso"

@app.route("/privacidad")
def privacidad():
    return render_template('privacidad.html')





@app.errorhandler(401)
def status_401(error):
    return redirect(url_for('privacidad')), 401

@app.errorhandler(404)
def status_404(error):
    return redirect('/')


if __name__== "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
