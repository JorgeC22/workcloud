window.onload=function(){
    cargaDatosProceso();
    function cargaDatosProceso(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("CargaDocumentacionRazonSocial", "consultaJsonDocumentos");
        //var URLbaseFile = URLactual.replace("RevisionDocumentacion", "archivo");
        var dominio = document.domain;

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var jsonDatosProceso = JSON.parse(this.responseText);
                var URLbaseFile = "https://"+dominio+"/archivo/"+jsonDatosProceso.id;

                var formCargaDocumentosProspecto = document.getElementById("formCargaDocumentosProspecto");
                var inputRazonSocial = document.getElementById('razonSocial');
                inputRazonSocial.setAttribute("value", jsonDatosProceso.cliente.razonSocial);
                var inputRfc = document.getElementById('rfc');
                inputRfc.setAttribute("value", jsonDatosProceso.cliente.rfc);
                var inputDistribuidor = document.getElementById('distribuidor');
                inputDistribuidor.setAttribute("value", jsonDatosProceso.cliente.distribuidor);

                if (jsonDatosProceso.documentos.length == 0){
                    var divContenedorInputsArchivos = document.getElementById('contenedorInputsArchivos');
                    divContenedorInputsArchivos.setAttribute("style", "display: none;");
                }else{
                    var inputNombreContactoProspecto = document.getElementById("nombreContactoProspecto");
                    inputNombreContactoProspecto.setAttribute("value", jsonDatosProceso.datosContactoProspecto.nombreContacto);
                    inputNombreContactoProspecto.setAttribute("readonly", "");
                    var inputTelefonoContactoProspecto = document.getElementById("telefonoContactoProspecto");
                    inputTelefonoContactoProspecto.setAttribute("value", jsonDatosProceso.datosContactoProspecto.telefonoContacto);
                    inputTelefonoContactoProspecto.setAttribute("readonly", "");
                    var inputCorreoContactoProspecto = document.getElementById("correoContactoProspecto");
                    inputCorreoContactoProspecto.setAttribute("value", jsonDatosProceso.datosContactoProspecto.correoContacto);
                    inputCorreoContactoProspecto.setAttribute("readonly", "");
                    var inputPuestoContactoProspecto = document.getElementById("puestoContactoProspecto");
                    inputPuestoContactoProspecto.setAttribute("value", jsonDatosProceso.datosContactoProspecto.puestoContacto);
                    inputPuestoContactoProspecto.setAttribute("readonly", "");



                    var divContenedorInputsArchivosInicial = document.getElementById('contenedorInputsArchivosInicial');
                    formCargaDocumentosProspecto.removeChild(divContenedorInputsArchivosInicial);
                    var divContenedorInputsArchivos = document.getElementById('contenedorInputsArchivos');

                    for (let i = 0; i < jsonDatosProceso.documentos.length; i++){
    
    
                        var xhttp = new XMLHttpRequest();
                        xhttp.open('GET',URLbaseFile+"/"+jsonDatosProceso.documentos[i].nombreDoc, true);
                        xhttp.send();
                        xhttp.onreadystatechange = function(){
                            if(this.readyState==4 && this.status==200){
                                var F = this.getResponseHeader('content-disposition').split('filename=')[1].split(';')[0];

    
                                var divContenedorInputArchivo = document.createElement("div");
                                divContenedorInputArchivo.setAttribute("class", "mb-3 row");
            
                                var labelArchivo = document.createElement("label");
                                labelArchivo.setAttribute("for", "formFile");
                                labelArchivo.setAttribute("class", "form-label");
                                var tituloArchivo = document.createTextNode(jsonDatosProceso.documentos[i].nombreDoc);
                                labelArchivo.appendChild(tituloArchivo);

                                var divContenedorColumnaInput = document.createElement("div");
                                divContenedorColumnaInput.setAttribute("class", "col-sm-10");

                                var divContenedorColumnaValidacion = document.createElement("div");
                                divContenedorColumnaValidacion.setAttribute("class", "col-sm-2");


                                if (jsonDatosProceso.documentos[i].validacion == true){
                                    var inputArchivo = document.createElement("input");
                                    inputArchivo.setAttribute("class", "form-control");
                                    inputArchivo.setAttribute("type", "text");
                                    inputArchivo.setAttribute("readonly", "");
                                    inputArchivo.setAttribute("id", jsonDatosProceso.documentos[i].nombreDoc);
                                    inputArchivo.setAttribute("value", F);
                                    divContenedorColumnaInput.append(inputArchivo);

                                    var elementoParrafoValidacion = document.createElement("p");
                                    elementoParrafoValidacion.setAttribute("class", "btn btn-success")
                                    elementoParrafoValidacion.setAttribute("style", "width: 140px;")
                                    var texto = document.createTextNode("Aceptado");
                                    elementoParrafoValidacion.appendChild(texto);
                                    divContenedorColumnaValidacion.append(elementoParrafoValidacion);

                                    divContenedorInputArchivo.append(labelArchivo);
                                }else{

                                    var inputArchivoSeccionReferencia = document.createElement("input");
                                    inputArchivoSeccionReferencia.setAttribute("value", jsonDatosProceso.documentos[i].nombreDoc);
                                    inputArchivoSeccionReferencia.setAttribute("name", jsonDatosProceso.documentos[i].nombreDoc);
                                    inputArchivoSeccionReferencia.setAttribute("type", "hidden");

                                    var inputArchivo = document.createElement("input");
                                    inputArchivo.setAttribute("class", "form-control");
                                    inputArchivo.setAttribute("type", "file");
                                    inputArchivo.setAttribute("oninput", "evaluarArchivo(this)");
                                    inputArchivo.setAttribute("id", jsonDatosProceso.documentos[i].nombreDoc);
                                    inputArchivo.setAttribute("name", jsonDatosProceso.documentos[i].nombreDoc);
                                    inputArchivo.setAttribute("required", "");
                                    divContenedorColumnaInput.append(inputArchivo);

                                    var elementoParrafoValidacion = document.createElement("p");
                                    elementoParrafoValidacion.setAttribute("class", "btn btn-danger");
                                    elementoParrafoValidacion.setAttribute("style", "width: 140px;");
                                    var texto = document.createTextNode("Rechazado");
                                    elementoParrafoValidacion.appendChild(texto);
                                    divContenedorColumnaValidacion.append(elementoParrafoValidacion);

                                    var elementoParrafoNotificacionRechazo = document.createElement("p");
                                    elementoParrafoNotificacionRechazo.setAttribute("style", "font-size: 14px; background: rgba(235,230,119); border-radius: 8px;");
                                    var textoNotificacionRechazo = document.createTextNode("Motivo del Rechazo: "+jsonDatosProceso.documentos[i].motivoRechazo);
                                    elementoParrafoNotificacionRechazo.appendChild(textoNotificacionRechazo);

                                    divContenedorInputArchivo.append(labelArchivo);
                                    divContenedorInputArchivo.append(inputArchivoSeccionReferencia);


                                }

                                var parrafoInfoArchivoCargado = document.createElement("p"); 
                                parrafoInfoArchivoCargado.setAttribute("id", jsonDatosProceso.documentos[i].nombreDoc);
                                parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");
            
                                divContenedorInputArchivo.append(divContenedorColumnaInput);
                                divContenedorInputArchivo.append(divContenedorColumnaValidacion);
                                divContenedorInputArchivo.append(parrafoInfoArchivoCargado);
                                if (jsonDatosProceso.documentos[i].validacion == false){
                                    divContenedorInputArchivo.append(elementoParrafoNotificacionRechazo);
                                }
                                divContenedorInputsArchivos.append(divContenedorInputArchivo);
                            }
                        }
                    }
                }



            }
        }
    }
}



const myFunction = (e) => {
    if(e.checked == true){
        var inputArchivo = document.getElementById(e.id);
        inputArchivo.removeAttribute("required");
        inputArchivo.removeAttribute("name");
        inputArchivo.setAttribute("readonly", "");
        inputArchivo.setAttribute("type", "text");
        inputArchivo.setAttribute("placeholder", "Ningun archivo selec.");
        var inputNodoReferencia = document.getElementById(e.id+" referencia");
        inputNodoReferencia.removeAttribute("name");
        inputNodoReferencia.removeAttribute("value");

        var parrafoInfoSeccion = document.querySelector("p[id='"+e.id+"']");
        parrafoInfoSeccion.innerHTML = "";
    }else{
        var inputArchivo = document.getElementById(e.id);
        inputArchivo.setAttribute("required", "");
        inputArchivo.setAttribute("name", e.id);
        inputArchivo.setAttribute("type", "file");
        inputArchivo.removeAttribute("readonly");
        inputArchivo.removeAttribute("placeholder");
        var inputNodoReferencia = document.getElementById(e.id+" referencia");
        inputNodoReferencia.setAttribute("name", e.id);
        inputNodoReferencia.setAttribute("value", e.id);
    }
}