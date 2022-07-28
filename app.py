import base64
from io import BytesIO
import json
from urllib import response
from flask import Flask, render_template, request, redirect, send_file, url_for, flash, jsonify, session, g
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import controlador
import usuariosDatos
import io
from werkzeug.utils import secure_filename
import random
from models.usuario import usuario
from models.formCrsf import formProtectionCsrf
import datetime
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from werkzeug.datastructures import ImmutableDict


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
csrf = CSRFProtect(app)
WTF_CSRF_SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

app.jinja_options = ImmutableDict(
 extensions=[
  'jinja2.ext.autoescape', 'jinja2.ext.with_' #Turn auto escaping on
 ])

# Autoescaping depends on you
app.jinja_env.autoescape = True 

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)


login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return usuariosDatos.get_by_id(id)


@app.route("/")
def index():
    #flash('Mensaje de prueba!')
    return redirect(url_for('login'))


## Funciones de las vistas de la aplicacion.
@app.route("/listaInstancias")
@login_required
def listaInstancias():
    return render_template('listaInstancias.html')

@app.route("/consultaInstancias", methods=['GET'])
@login_required
def consultaInstancias():
    listaGrupoArea = controlador.obtenerGrupoArea(session['grupos'])
    if listaGrupoArea:
        if listaGrupoArea[0] == "Prospectos" or listaGrupoArea[0] == "MesaControl":
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
    else:
        listaProcesos = []
        response = jsonify(listaProcesos)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response 


@app.route("/<pagina>/<idproceso>/<idtask>")
@login_required
def paginaTarea(pagina,idproceso,idtask):
    formCsrf = formProtectionCsrf()
    return render_template('./paginasTareas/'+pagina+'.html', idproceso=idproceso, idtask=idtask, form=formCsrf)


@app.route("/consultaJsonDocumentos/<idproceso>/<idtask>", methods=['GET'])
@login_required
def consultaJsonDocumentos(idproceso,idtask):
    jsonProceso = controlador.getJsonProceso(idproceso)
    response = jsonify(jsonProceso)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/consultaJsonDocumentosAccionistas/<idproceso>/<idtask>", methods=['GET'])
@login_required
def consultaJsonDocumentosAccionistas(idproceso,idtask):
    jsonProceso = controlador.getJsonDatosProcesoAccionistas(idproceso)
    response = jsonify(jsonProceso)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/consultaJsonDocumentosRazonSocialAccionaria/<idproceso>/<variable>", methods=['GET'])
@login_required
def consultaJsonDocumentosRazonSocialAccionaria(idproceso,variable):
    jsonDatosProcesoAccionaria = controlador.getJsonDatosProcesoAccionistas(idproceso)
    rfcRazonSocialAccionaria = controlador.getRfcRazonSocialAccionaria(variable,jsonDatosProcesoAccionaria)
    jsonVariablesRazonSocialAccionaria = controlador.getJsonVariableRazonSocialAccionaria(idproceso,rfcRazonSocialAccionaria)
    response = jsonify(jsonVariablesRazonSocialAccionaria)
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
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
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
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
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
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
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
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
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
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
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
    controlador.sendEmailNotificarCreacionCuentaCliente(idproceso,jsonProceso)
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
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
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
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
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
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
        #jsonDatosContrato = controlador.conjuntarJsonProceso(jsonProceso,idproceso)
        jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
        controlador.CompleteTask(idtask,jsonProceso)
        controlador.registrarEvento(idproceso)
        controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
        #controlador.registrarDatosProcesoFinal(jsonDatosContrato,idproceso)
        controlador.actualizarStatusProceso(idproceso)
        return redirect(url_for('listaInstancias'))
    else:
        jsonProceso = controlador.getJsonProceso(idproceso)
        jsonProceso = controlador.actualizarJSONenvioContratoOriginalCliente(jsonProceso, jsonForm)
        jsonProceso = controlador.getProcesoActividad(jsonProceso)
        controlador.CompleteTask(idtask,jsonProceso)
        controlador.registrarEvento(idproceso)
        controlador.sendEmailTareasProceso(idproceso,jsonProceso)
        jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
        controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
        return redirect(url_for('listaInstancias'))

@app.route("/validarEstructuraAccionaria/<idproceso>/<idtask>", methods=['POST'])
@login_required
def validarEstructuraAccionaria(idproceso,idtask):
    listaValueForm = request.form.listvalues()
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    listaJsonVariablesRazonSocialAccionaria = controlador.getListaJsonVariableRazonSocialAccionaria(idproceso, jsonDatosProcesoAccionistas)
    variablesRazonSocialAccionaria = controlador.actualizarJSONdocumentosAccionistas(jsonDatosProcesoAccionistas,listaValueForm,listaJsonVariablesRazonSocialAccionaria)
    jsonDatosProcesoAccionistas = controlador.comprobarValidacionEstructuraAccionaria(listaValueForm,jsonDatosProcesoAccionistas)
    controlador.accionistasCompleteTask(idtask,jsonDatosProcesoAccionistas,variablesRazonSocialAccionaria)
    jsonProceso = controlador.getJsonProceso(idproceso)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
    return redirect(url_for('listaInstancias'))

@app.route("/cargarDocumentosRazonSocialAccionaria/<idproceso>/<idtask>", methods=['POST'])
@login_required
def cargarDocumentosRazonSocialAccionaria(idproceso,idtask):
    listas = request.form.listvalues()
    files = request.files
    jsonDatosProcesoAccionistas = controlador.getJsonDatosProcesoAccionistas(idproceso)
    jsonRazonSocialAccionarias = controlador.crearJsonDocumentosRazonSocialAccionaria(listas,jsonDatosProcesoAccionistas,files)
    jsonDatosProcesoAccionistas = controlador.actualizarJsonDatosProcesoAccionistas(jsonDatosProcesoAccionistas)
    jsonFiles = controlador.crearJsonFileAccionistas(listas,files,jsonDatosProcesoAccionistas)
    controlador.filesAccionistasCompleteTask(idtask,jsonDatosProcesoAccionistas,jsonFiles,jsonRazonSocialAccionarias)
    jsonProceso = controlador.getJsonProceso(idproceso)
    controlador.registrarEvento(idproceso)
    controlador.sendEmailTareasProceso(idproceso,jsonProceso)
    controlador.actualizarJsonProcesoDB(idproceso,jsonProceso,jsonDatosProcesoAccionistas)
    return redirect(url_for('listaInstancias'))




##Seccion - Puntos de acceso Login.
@app.route("/login")
def login():
    formCsrf = formProtectionCsrf()
    return render_template('Login.html', form=formCsrf)

@app.route("/autenticando", methods=['POST'])
def autenticando():
    correoUsuario = request.form['correoUsuario']
    existeCorreoUsuario = controlador.validarCorreo(correoUsuario)
    codigo = ""
    formCsrf = formProtectionCsrf()
    if existeCorreoUsuario:
        session['correoUsuario'] = correoUsuario
        usuarioOperativo = controlador.extraerNombreUsuarioMedianteCorreo(session['correoUsuario'])
        usuarioGruposProspecto = controlador.extraerGruposUser(usuarioOperativo)
        if usuarioGruposProspecto[0] == "Prospectos":
            session['ruta'] = controlador.extraerRutaDistribuidorMedianteCorreo(session['correoUsuario'])
            if session['ruta']:
                print("Usuario ya esta registrado.")
            else:
                flash("El correo introducido no esta registrado o no se registro correctamente.")
                return redirect(url_for('login', form=formCsrf))

        for i in range(6):
            numero = random.randrange(1,9,1)
            codigo = codigo + str(numero)
        tokenAcceso = codigo
        controlador.registrarTokenUsuarioProspecto(usuarioOperativo,tokenAcceso)
        session['usuario'] = usuarioOperativo
        print(f"Codigo de Seguridad: {tokenAcceso}")
        controlador.sendEmail(session['correoUsuario'],tokenAcceso,"login")
        session['correoUsuarioMascara'] = controlador.ocultarCorreo(session['correoUsuario'])
        return redirect(url_for('tokenAccesoCorreoUsuario', form=formCsrf))
    else:
        flash("El correo introducido no esta registrado o no se registro correctamente.")
        return redirect(url_for('login', form=formCsrf))

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
    formCsrf = formProtectionCsrf()
    return render_template('iniciarProceso.html', form=formCsrf)
    

@app.route("/iniciarProceso", methods=['POST'])
@login_required
def iniciarProceso():
    jsonForm = request.form.to_dict()
    existeRfcProspecto = controlador.validarRfcProspecto(jsonForm['rfcProspecto'])
    if existeRfcProspecto:
        flash("El RFC introducido ya esta registrado.")
        return redirect(url_for('registro'))
    else:
        jsonProcesoCliente = controlador.crearJsonCliente(jsonForm)
        idInstanciaProceso = controlador.iniciarProceso(jsonProcesoCliente,session['usuario'])
        controlador.registrarProceso(jsonProcesoCliente,session['usuario'],idInstanciaProceso,session['ruta'])
        jsonProceso = controlador.getJsonProceso(idInstanciaProceso)
        jsonDatosProcesosAccionistas = controlador.getJsonDatosProcesoAccionistas(idInstanciaProceso)
        controlador.registrarDatosProceso(idInstanciaProceso,jsonProceso,jsonDatosProcesosAccionistas)
        return redirect(url_for('listaInstancias'))

@app.route("/extraerNotificacionEmail/<idproceso>/<idtask>", methods=['GET'])
def extraerNotificacionEmail(idproceso,idtask):
    notificacion = controlador.notificacion(idproceso)
    response = jsonify(notificacion)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




## Seccion - Vistas y funciones para inicio de registro "Razon social".
@app.route("/<distribuidor>/registroNuevaRazonSocial")
def registroNuevaRazonSocial(distribuidor):
    session.clear()
    formCsrf = formProtectionCsrf()
    return render_template('capturarRFC.html',distribuidor=distribuidor, form=formCsrf)

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
    formCsrf = formProtectionCsrf()
    return render_template('datosEmpresa.html',distribuidor=distribuidor, form=formCsrf)

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
    formCsrf = formProtectionCsrf()
    return render_template('tokenAccesoExisteRFC.html',distribuidor=distribuidor, form=formCsrf)

@app.route("/<distribuidor>/tokenAccesoNoExisteRFC")
def tokenAccesoNoExisteRFC(distribuidor):
    formCsrf = formProtectionCsrf()
    return render_template('tokenAccesoNoExisteRFC.html',distribuidor=distribuidor, form=formCsrf)

@app.route("/tokenAccesoCorreoUsuario")
def tokenAccesoCorreoUsuario():
    formCsrf = formProtectionCsrf()
    return render_template('tokenAccesoCorreoUsuario.html', form=formCsrf)


@app.route("/validarTokenAccesoCorreoExistente", methods=['POST'])
def validarTokenAccesoCorreoExistente():
    formCsrf = formProtectionCsrf()
    tokenAcceso = request.form['tokenAcceso']
    tokenAccesoExiste = controlador.validaTokenAcceso(session,tokenAcceso)
    if tokenAccesoExiste:
        usuarioGruposProspecto = controlador.extraerGruposUser(session['usuario'])
        session['grupos'] = usuarioGruposProspecto
        if session['grupos'][0] == "Prospectos":
            session['ruta'] = controlador.extraerRutaDistribuidorMedianteCorreo(session['correoUsuario'])
            if session['ruta']:
                session['distribuidor'] = controlador.extraerDistribuidorMedianteRuta(session['ruta'])
            else:
                return redirect(url_for('login', form=formCsrf))

        logger_user = usuariosDatos.loggin_user(session['usuario'],session['correoUsuario'])
        login_user(logger_user)
        return redirect(url_for('listaInstancias'))
    else:
        flash("EL codigo ingresado es incorrecto o ya no esta vigente.")
        return redirect(url_for('login', form=formCsrf))


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

        jsonProcesoCliente = controlador.crearJsonCliente(session)
        idInstanciaProceso = controlador.iniciarProceso(jsonProcesoCliente,session['usuario'])
        controlador.registrarProceso(jsonProcesoCliente,session['usuario'],idInstanciaProceso,distribuidor)
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

        jsonProceso = controlador.getJsonProceso(idInstanciaProceso)
        jsonDatosProcesosAccionistas = controlador.getJsonDatosProcesoAccionistas(idInstanciaProceso)
        controlador.registrarDatosProceso(idInstanciaProceso,jsonProceso,jsonDatosProcesosAccionistas)
        return redirect(url_for('listaInstancias'))
        #return "exitoso"
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



@app.route("/monitoreo")
def monitoreo():
    return render_template('vistaMonitoreo.html')

@app.route("/datosMonitoreoProcesos", methods=['GET'])
def datosMonitoreoProcesos():
    jsonProcesos = controlador.getProcesos()
    listaProcesos = controlador.getlistJsonProceso(jsonProcesos)
    listaProcesos = controlador.getactividadProcesos(listaProcesos)
    listaProcesos = controlador.getTaskProcesos(listaProcesos)
    listaProcesos = controlador.obtenerCandidatoGrupoTarea(listaProcesos)
    listaProcesos = controlador.fechahoraActividad(listaProcesos)
    listaProcesos = controlador.fechaHoraInicioProceso(listaProcesos)
    listaProcesos = controlador.tiempoTranscurridoTarea(listaProcesos)
    response = jsonify(listaProcesos)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




@app.after_request
def apply_caching(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Content-Security-Policy'] = """script-src http://ajax.googleapis.com/ https://cdn.jsdelivr.net/npm/ https://cdn.datatables.net/ https://cdnjs.cloudflare.com/ https://www.googletagmanager.com/ 'self' """ # Permite definir que script pueden ejecutar o desplegarse dentro de la aplicacion indicando el origen del mismo.
    response.headers['Content-Security-Policy'] = """style-src 'unsafe-inline' https://cdn.jsdelivr.net/npm/ https://cdnjs.cloudflare.com/ https://cdn.datatables.net/ https://use.fontawesome.com/ 'self' """ # Permite definir que archivos de estilo pueden ejecutar o desplegarse dentro de la aplicacion indicando el origen del mismo.
    response.headers["X-Frame-Options"] = "SAMEORIGIN" # Obliga al navegador a respetar el tipo de contenido de la respuesta.
    response.headers['X-Content-Type-Options'] = 'nosniff' # Evita que sitios externos incrusten su sitio en un iframe.
    return response

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
