import base64
from distutils.archive_util import make_archive
from io import BytesIO
import mimetypes
from flask import Flask, make_response, render_template, request, redirect, send_file, url_for, flash, jsonify
from itsdangerous import json
from requests import Response
import controlador
import io
#import magic
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'dont tell anyone'


@app.route("/")
def index():
    #flash('Mensaje de prueba!')
    return redirect(url_for('listaInstancias'))

#@app.route("/inciarProceso")
#def iniciarProceso():
#    return render_template('iniciarProceso.html')

@app.route("/startProceso")
def startProceso():
    #form_data = request.form.to_dict()
    #print(form_data)
    idproceso = controlador.inicioProceso()
    #datosP = controlador.getVariablesProceso(idproceso)
    #return render_template('pagina1.html', data=datosP)
    return redirect(url_for('listaInstancias'))

    

@app.route("/listaInstancias")
def listaInstancias():
    return render_template('listaInstancias.html')

@app.route("/consultaInstancias", methods=['GET'])
def consultaInstancias():
    procesos = controlador.getProcesos()
    listJsonP = controlador.getlistJsonProceso(procesos)
    listP = controlador.getactividadProcesos(listJsonP)
    listP = controlador.fechahoraActividad(listP)
    response = jsonify(listP)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response







@app.route("/<pagina>/<idproceso>")
def paginaTarea(pagina,idproceso):
    return render_template('./paginasTareas/'+pagina+'.html', idproceso=idproceso)


@app.route("/consultaJsonDocumentos/<idproceso>", methods=['GET'])
def consultaJsonDocumentos(idproceso):
    jsonProceso = controlador.getJsonProceso(idproceso)
    response = jsonify(jsonProceso)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/cargarDocumentos/<idproceso>", methods=['POST'])
def cargarDocumentos(idproceso):
    listas = request.form.listvalues()
    files = request.files
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonDocumentos(listas,jsonProceso)
    jsonFiles = controlador.crearJsonFile(listas,files)
    idTask = controlador.gettask(idproceso)
    controlador.filesCompleteTask(idTask,jsonProceso,jsonFiles)
    return redirect(url_for('listaInstancias'))

@app.route("/validarDocumentos/<idproceso>", methods=['POST'])
def validarDocumentos(idproceso):
    listas = request.form.listvalues()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.actualizarJSONdocumentos(jsonProceso, listas)
    idTask = controlador.gettask(idproceso)
    controlador.CompleteTask(idTask,jsonProceso)
    return redirect(url_for('listaInstancias'))


@app.route("/cargarContrato/<idproceso>", methods=['POST'])
def cargarContrato(idproceso):
    listas = request.form.listvalues()
    files = request.files
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.crearJsonContrato(listas,jsonProceso)
    jsonFiles = controlador.crearJsonFile(listas,files)
    idTask = controlador.gettask(idproceso)
    controlador.filesCompleteTask(idTask,jsonProceso,jsonFiles)
    return redirect(url_for('listaInstancias'))


@app.route("/validarContrato/<idproceso>", methods=['POST'])
def validarContrato(idproceso):
    listas = request.form.listvalues()
    jsonProceso = controlador.getJsonProceso(idproceso)
    jsonProceso = controlador.actualizarJSONcontrato(jsonProceso, listas)
    idTask = controlador.gettask(idproceso)
    controlador.CompleteTask(idTask,jsonProceso)
    return redirect(url_for('listaInstancias'))

@app.route("/archivo/<idproceso>/<variable>")
def archivo(idproceso,variable):
    data = controlador.getObjectResponseFile(idproceso,variable)
    informacionArchivo = controlador.infoFile(idproceso,variable)
    return send_file(io.BytesIO(data.content), attachment_filename=informacionArchivo['valueInfo']['filename'], mimetype=informacionArchivo['valueInfo']['mimeType'])

@app.route("/terminarDescarga/<idproceso>", methods=['POST'])
def terminarDescarga(idproceso):
    jsonProceso = controlador.getJsonProceso(idproceso)
    idTask = controlador.gettask(idproceso)
    controlador.CompleteTask(idTask,jsonProceso)
    return redirect(url_for('listaInstancias'))






@app.route("/cargarFile")
def cargarFile():
    return render_template('cargarFile.html')

@app.route("/cargar", methods=['POST'])
def cargar():
    filess = request.files['file']
    filess.save("./archivos/"+filess.filename)
    with open("./archivos/"+filess.filename, "rb") as data:
        code = base64.b64encode(data.read())
    
    print(code.decode())
    controlador.cargarArchivo(code.decode())
    return redirect(url_for('cargarFile'))
    return "exitoso"

@app.route("/File")
def File():
    data = controlador.file()
    #response = jsonify(data)
    #return render_template('file.html', data=data)
    #return Response(data.raw, mimetypes="application/pdf")
    return send_file(io.BytesIO(data.content), attachment_filename='hola3.pdf', mimetype='application/pdf') 


if __name__== "__main__":
    app.run(debug=True)
