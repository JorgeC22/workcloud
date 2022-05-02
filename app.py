from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import controlador


app = Flask(__name__)


@app.route("/")
def index():
    #flash('Mensaje de prueba!')
    return redirect(url_for('listaVerificarDatos'))

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
    datosP = controlador.getJsonProceso(idproceso)
    response = jsonify(datosP)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/cargarDocumentos", methods=['POST'])
def cargarDocumentos():
    listas = request.form.listvalues()
    data = controlador.getVariableJson(request.form['idproceso'])
    dataJson = controlador.datosProcesos(listas,data)
    idtask = controlador.gettask(request.form['idproceso'])
    controlador.CompleteTask(idtask,dataJson)
    return redirect(url_for('listaInstancias'))

@app.route("/validarDocumentos", methods=['POST'])
def validarDocumentos():
    listas = request.form.listvalues()
    jsonData = controlador.getJsonProceso(request.form['idproceso'])
    jsonActualizado = controlador.actualizarJSON(jsonData, listas)
    idtask = controlador.gettask(request.form['idproceso'])
    controlador.CompleteTask(idtask,jsonActualizado)
    return redirect(url_for('listaInstancias'))
    #print(listas)
    #print("#############################")
    #print(jsonActualizado)
    #return "Exitoso"

#@app.route("/RevisiondeDocumentacion/<idproceso>")
#def RevisiondeDocumentacion(idproceso):
#    return render_template('RevisiondeDocumentacion.html')





if __name__== "__main__":
    app.run(debug=True)
