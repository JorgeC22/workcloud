window.onload=function(){
    cargaDatosProceso();
    function cargaDatosProceso(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("CargaDocumentacionAdicional", "consultaJsonDocumentos");
        var URLdocumentosAccionistas = URLactual.replace("CargaDocumentacionAdicional", "consultaJsonDocumentosAccionistas");
        //var URLbaseFile = URLactual.replace("RevisionDocumentacion", "archivo");
        var dominio = document.domain;

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var jsonDatosProceso = JSON.parse(this.responseText);
                var URLbaseFile = location.origin+"/archivo/"+jsonDatosProceso.id;

                var formCargaDocumentosProspecto = document.getElementById("formCargaDocumentosProspecto");
                var inputRazonSocial = document.getElementById('razonSocial');
                inputRazonSocial.setAttribute("value", jsonDatosProceso.cliente.razonSocial);
                var inputRfc = document.getElementById('rfc');
                inputRfc.setAttribute("value", jsonDatosProceso.cliente.rfc);
                var inputDistribuidor = document.getElementById('distribuidor');
                inputDistribuidor.setAttribute("value", jsonDatosProceso.cliente.distribuidor);


                var xhttp = new XMLHttpRequest();
                xhttp.open('GET',URLdocumentosAccionistas, true);
                xhttp.send();
                xhttp.onreadystatechange = function(){
                    if(this.readyState==4 && this.status==200){
                        
                        var jsonDatosProcesoAccionista = JSON.parse(this.responseText);
                        var contenedorInputsArchivosInicial = document.getElementById("contenedorInputsArchivosInicial");

                        var textoRazonSocialaccionaria = "";
                        for (let i = 0; i < jsonDatosProcesoAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante.length; i++) {
                            console.log(jsonDatosProcesoAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante[i].razonSocial)
                            if (textoRazonSocialaccionaria == ""){
                                textoRazonSocialaccionaria = textoRazonSocialaccionaria+jsonDatosProcesoAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante[i].razonSocial;
                            }else{
                                textoRazonSocialaccionaria = textoRazonSocialaccionaria+", "+jsonDatosProcesoAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante[i].razonSocial;
                            }
                        }

                        var parrafoInfoCargaDocumentosRazonSocialAccionaria = document.getElementById("parrafoInfoCargaDocumentosRazonSocialAccionaria");
                        var textoTituloVistaTarea = document.createTextNode("Se requiere realizar la carga de documentación adicional de las siguientes razones sociales \""+textoRazonSocialaccionaria+"\"");
                        parrafoInfoCargaDocumentosRazonSocialAccionaria.appendChild(textoTituloVistaTarea);

                        

                        var listaRazonSocialAccionaria = jsonDatosProcesoAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante;
                        for (let rsa = 0; rsa < listaRazonSocialAccionaria.length; rsa++) {
                            
                            
                            if (jsonDatosProcesoAccionista.documentosAccionistas.length > 0){
                                for (let jrsa = 0; jrsa < jsonDatosProcesoAccionista.documentosAccionistas.length; jrsa++) {
                                    if (listaRazonSocialAccionaria[rsa].razonSocial == jsonDatosProcesoAccionista.documentosAccionistas[jrsa]['razonSocial']){
                                        //console.log("RSA Registrado");
                                        razonSocialDocumentosEncontrados = true;
                                        break;
                                    }else{
                                        razonSocialDocumentosEncontrados = false
                                    }
                                    
                                }
                            }else{
                                razonSocialDocumentosEncontrados = false
                            }
                            console.log()

                            if (razonSocialDocumentosEncontrados == true){
                                var URLbaseDocumentosRazonSocialAccionaria = location.origin+"/consultaJsonDocumentosRazonSocialAccionaria/"+jsonDatosProcesoAccionista.id+"/";
                                    
                                
                                var xhttp = new XMLHttpRequest();
                                xhttp.open('GET',URLbaseDocumentosRazonSocialAccionaria+listaRazonSocialAccionaria[rsa].razonSocial, true);
                                xhttp.send();
                                xhttp.onreadystatechange = function(){
                                    if(this.readyState==4 && this.status==200){
                                        var jsonRazonSocialAccionaria = JSON.parse(this.responseText);
                            
                                        //Se crea titulo de la razon social-seccion en cuestion.
                                        var tituloFormRazonSocialAccionaria = document.createElement("h4");
                                        var textoTituloSeccionFile = document.createTextNode("Documentacion de razon social \""+listaRazonSocialAccionaria[rsa].razonSocial+"\"");
                                        tituloFormRazonSocialAccionaria.appendChild(textoTituloSeccionFile);

                                        //Se crea campo no visible de referencia de la seccion.
                                        var inputTituloSeccionRazonSocial = document.createElement("input");
                                        inputTituloSeccionRazonSocial.setAttribute("type", "hidden");
                                        inputTituloSeccionRazonSocial.setAttribute("name", "razonSocialAccionaria");
                                        inputTituloSeccionRazonSocial.value = listaRazonSocialAccionaria[rsa].razonSocial;

                                        //Se crea contenedor de seccion.
                                        var divContenedorSeccionArchivos = document.createElement("div");

                                        //Se agrega titulo y campo referencia a seccion.
                                        divContenedorSeccionArchivos.append(tituloFormRazonSocialAccionaria);
                                        divContenedorSeccionArchivos.append(inputTituloSeccionRazonSocial);
                                        contenedorInputsArchivosInicial.append(divContenedorSeccionArchivos);

                                        //Se crea contenedor que contendra los campos de los documentos.
                                        var divContenedorInputsRazonSocialAccionaria = document.createElement("div");

                                        
                                        //Se recorren todos los documentos de la razon social.
                                        for (let drsa = 0; drsa < jsonRazonSocialAccionaria.documentos.length; drsa++) {
                                            
                                            //Funcion para obtener datos del documento en cuestion.
                                            var xhttp = new XMLHttpRequest();
                                            xhttp.open('GET',URLbaseFile+"/"+jsonRazonSocialAccionaria.documentos[drsa].nombreDoc, true);
                                            xhttp.send();
                                            xhttp.onreadystatechange = function(){
                                                if(this.readyState==4 && this.status==200){
                                                    //Se obtine nombre del archivo.
                                                    var nombreArchivo = this.getResponseHeader('content-disposition').split('filename=')[1].split(';')[0];
                                                    nombreCampoSeccion = jsonRazonSocialAccionaria.documentos[drsa].nombreDoc.replace(listaRazonSocialAccionaria[rsa].rfc+" ","");
                                                    nombreCampoFile = jsonRazonSocialAccionaria.documentos[drsa].nombreDoc.replace(listaRazonSocialAccionaria[rsa].rfc,"("+listaRazonSocialAccionaria[rsa].razonSocial+")");

                                                    var divContenedorInputArchivo = document.createElement("div");
                                                    divContenedorInputArchivo.setAttribute("class", "mb-3 row");
                                
                                                    //Se define el titulo del archivo a tratar.
                                                    var labelArchivo = document.createElement("label");
                                                    labelArchivo.setAttribute("for", "formFile");
                                                    labelArchivo.setAttribute("class", "form-label");
                                                    var tituloArchivo = document.createTextNode(nombreCampoSeccion);
                                                    labelArchivo.appendChild(tituloArchivo);

                                                    //Se crea el contenedor que contendra el campo archivo.
                                                    var divContenedorColumnaInput = document.createElement("div");
                                                    divContenedorColumnaInput.setAttribute("class", "col-sm-10");

                                                    //Se crea el contenedor que contendra el indicador de aceptacion/rechazo.
                                                    var divContenedorColumnaValidacion = document.createElement("div");
                                                    divContenedorColumnaValidacion.setAttribute("class", "col-sm-2");

                                                    //Se recorren revisa la validacion y determinar el tipo de indicador a visualizar
                                                    if (jsonRazonSocialAccionaria.documentos[drsa].validacion == true){

                                                        //Se crea el campo donde se mostrara el archivo que fue aceptado.
                                                        var inputArchivo = document.createElement("input");
                                                        inputArchivo.setAttribute("class", "form-control");
                                                        inputArchivo.setAttribute("type", "text");
                                                        inputArchivo.setAttribute("readonly", "");
                                                        inputArchivo.setAttribute("id", nombreCampoFile);
                                                        inputArchivo.setAttribute("value", nombreArchivo);
                                                        divContenedorColumnaInput.append(inputArchivo);

                                                        //Se crea el texto para mostrara el indicador de validacion.
                                                        var elementoParrafoValidacion = document.createElement("p");
                                                        elementoParrafoValidacion.setAttribute("class", "btn btn-success")
                                                        elementoParrafoValidacion.setAttribute("style", "width: 140px;")
                                                        var texto = document.createTextNode("Aceptado");
                                                        elementoParrafoValidacion.appendChild(texto);
                                                        divContenedorColumnaValidacion.append(elementoParrafoValidacion);

                                                        //Se agrega al contenedor general de la seccion el titulo.
                                                        divContenedorInputArchivo.append(labelArchivo);
                                                    }else{

                                                        //Se crea campo no viseble que contendra el dato referencia de la seccion. 
                                                        var inputArchivoSeccionReferencia = document.createElement("input");
                                                        inputArchivoSeccionReferencia.setAttribute("value", nombreCampoFile);
                                                        inputArchivoSeccionReferencia.setAttribute("name", nombreCampoFile);
                                                        inputArchivoSeccionReferencia.setAttribute("type", "hidden");

                                                        //Se crea el campo donde se introducira el nuevo archivo de la seccion rechazada.
                                                        var inputArchivo = document.createElement("input");
                                                        inputArchivo.setAttribute("class", "form-control");
                                                        inputArchivo.setAttribute("type", "file");
                                                        inputArchivo.setAttribute("oninput", "evaluarArchivosAccionarias(this)");
                                                        inputArchivo.setAttribute("id", nombreCampoFile);
                                                        inputArchivo.setAttribute("name", nombreCampoFile);
                                                        inputArchivo.setAttribute("required", "");
                                                        divContenedorColumnaInput.append(inputArchivo);

                                                        //Se crea el texto para mostrara el indicador de validacion.
                                                        var elementoParrafoValidacion = document.createElement("p");
                                                        elementoParrafoValidacion.setAttribute("class", "btn btn-danger");
                                                        elementoParrafoValidacion.setAttribute("style", "width: 140px;");
                                                        var texto = document.createTextNode("Rechazado");
                                                        elementoParrafoValidacion.appendChild(texto);
                                                        divContenedorColumnaValidacion.append(elementoParrafoValidacion);

                                                        //Se crea parrafo que visualizara el motivo de rechazo del documento.
                                                        var elementoParrafoNotificacionRechazo = document.createElement("p");
                                                        elementoParrafoNotificacionRechazo.setAttribute("style", "font-size: 14px; background: rgba(235,230,119); border-radius: 8px;");
                                                        var textoNotificacionRechazo = document.createTextNode("Motivo del Rechazo: "+jsonRazonSocialAccionaria.documentos[drsa].motivoRechazo);
                                                        elementoParrafoNotificacionRechazo.appendChild(textoNotificacionRechazo);

                                                        //Se agrega al contenedor general de la seccion el titulo y el campo referencia.
                                                        divContenedorInputArchivo.append(labelArchivo);
                                                        divContenedorInputArchivo.append(inputArchivoSeccionReferencia);


                                                    }

                                                    //Se crea el parrafo en el cual se visualizara cuando un archivo cargado no entra dentro de las caracteristicas permitidas.
                                                    var parrafoInfoArchivoCargado = document.createElement("p"); 
                                                    parrafoInfoArchivoCargado.setAttribute("id", nombreCampoFile);
                                                    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");
                                
                                                    //Se agregan elementos faltantes al contenedor general del documento-seccion en cuestion.
                                                    divContenedorInputArchivo.append(divContenedorColumnaInput);
                                                    divContenedorInputArchivo.append(divContenedorColumnaValidacion);
                                                    divContenedorInputArchivo.append(parrafoInfoArchivoCargado);
                                                    if (jsonRazonSocialAccionaria.documentos[drsa].validacion == false){ //Si es un archivo rechazado se agrega el parrafo notificacion de rechazo.
                                                        divContenedorInputArchivo.append(elementoParrafoNotificacionRechazo);
                                                        divContenedorInputArchivo.append(parrafoInfoArchivoCargado);
                                                    }
                                                    
                                                    //Se agrega contenedor de campos de documentos al contenedor general de la seccion.
                                                    divContenedorInputsRazonSocialAccionaria.append(divContenedorInputArchivo);
                                                    
                                                }
                                            }
                                        }
                                        
                                        //var formRazonSocialAccionaria = divContenedorInputsRazonSocialAccionaria;
                                        //Se agrega contenedor de la seccion al contenedor general de documentos de la vista.
                                        contenedorInputsArchivosInicial.append(divContenedorInputsRazonSocialAccionaria);
                                    }
                                }
                            }else{
                            
                                //Se crea titulo de la razon social-seccion en cuestion.
                                var tituloFormRazonSocialAccionaria = document.createElement("h4");
                                var textoTituloSeccionFile = document.createTextNode("Documentacion de razon social \""+listaRazonSocialAccionaria[rsa].razonSocial+"\"");
                                tituloFormRazonSocialAccionaria.appendChild(textoTituloSeccionFile);

                                //Se crea campo no visible de referencia de la seccion.
                                var inputTituloSeccionRazonSocial = document.createElement("input");
                                inputTituloSeccionRazonSocial.setAttribute("type", "hidden");
                                inputTituloSeccionRazonSocial.setAttribute("name", "razonSocialAccionaria");
                                inputTituloSeccionRazonSocial.value = listaRazonSocialAccionaria[rsa].razonSocial;

                                //Se crea contenedor de seccion.
                                var divContenedorSeccionArchivos = document.createElement("div");

                                //Se agrega titulo y campo referencia a seccion.
                                divContenedorSeccionArchivos.append(tituloFormRazonSocialAccionaria);
                                divContenedorSeccionArchivos.append(inputTituloSeccionRazonSocial);
                                contenedorInputsArchivosInicial.append(divContenedorSeccionArchivos);

                                //Se crean campos de los documentos.
                                var formRazonSocialAccionaria =  crearFormularioRazonSocial(listaRazonSocialAccionaria[rsa].razonSocial);
                                //Se agregan los campos al contenedor general de documentos de la vista.
                                contenedorInputsArchivosInicial.append(formRazonSocialAccionaria);
                            }   
                        }
                    }
                }
            }
        }
    }
}




function crearFormularioRazonSocial(razonSocialAccionaria){
    var divContenedorInputsRazonSocialAccionaria = document.createElement("div");
    divContenedorInputsRazonSocialAccionaria.setAttribute("class", "mb-5");

    //Seccion de Acta constitutiva.
    var divContenedorSeccionActaConstitutiva = document.createElement("div");
    divContenedorSeccionActaConstitutiva.setAttribute("class", "mb-4");

    var labelTituloSeccionFile = document.createElement("label");
    labelTituloSeccionFile.setAttribute("for", "formFile");
    labelTituloSeccionFile.setAttribute("class", "form-label");
    var textoTituloSeccionFile = document.createTextNode("Acta constitutiva");
    labelTituloSeccionFile.appendChild(textoTituloSeccionFile);

    var inputSeccionFile = document.createElement("input");
    inputSeccionFile.setAttribute("type", "hidden");
    inputSeccionFile.setAttribute("name", "("+razonSocialAccionaria+") Acta constitutiva");
    inputSeccionFile.setAttribute("id", "Acta constitutiva");
    inputSeccionFile.setAttribute("value", "("+razonSocialAccionaria+") Acta constitutiva");

    var inputFile = document.createElement("input");
    inputFile.setAttribute("type", "file");
    inputFile.setAttribute("name", "("+razonSocialAccionaria+") Acta constitutiva");
    inputFile.setAttribute("id", "Acta constitutiva");
    inputFile.setAttribute("class", "form-control");
    inputFile.setAttribute("oninput", "");
    inputFile.setAttribute("required", "");
    inputFile.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", "("+razonSocialAccionaria+") Acta constitutiva");
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    divContenedorSeccionActaConstitutiva.append(labelTituloSeccionFile);
    divContenedorSeccionActaConstitutiva.append(inputSeccionFile);
    divContenedorSeccionActaConstitutiva.append(inputFile);
    divContenedorSeccionActaConstitutiva.append(parrafoInfoArchivoCargado);

    
    //Seccion de Acta asamblea.
    var divContenedorSeccionActaAsamblea = document.createElement("div");
    divContenedorSeccionActaAsamblea.setAttribute("id", "contenedorInputs("+razonSocialAccionaria+") Acta asamblea");
    divContenedorSeccionActaAsamblea.setAttribute("class", "mb-4");

    var labelTituloSeccionFile = document.createElement("label");
    labelTituloSeccionFile.setAttribute("for", "formFile");
    labelTituloSeccionFile.setAttribute("class", "form-label");
    var textoTituloSeccionFile = document.createTextNode("Acta asamblea");
    labelTituloSeccionFile.appendChild(textoTituloSeccionFile);

    var inputSeccionFile = document.createElement("input");
    inputSeccionFile.setAttribute("type", "hidden");
    inputSeccionFile.setAttribute("name", "("+razonSocialAccionaria+") Acta asamblea");
    inputSeccionFile.setAttribute("id", "("+razonSocialAccionaria+") Acta asamblea referencia");
    inputSeccionFile.setAttribute("value", "("+razonSocialAccionaria+") Acta asamblea");

    var inputFile = document.createElement("input");
    inputFile.setAttribute("type", "file");
    inputFile.setAttribute("name", "("+razonSocialAccionaria+") Acta asamblea");
    inputFile.setAttribute("id", "("+razonSocialAccionaria+") Acta asamblea");
    inputFile.setAttribute("class", "form-control");
    inputFile.setAttribute("oninput", "");
    inputFile.setAttribute("required", "");
    inputFile.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var divContenedorCheckbox = document.createElement("div");
    divContenedorCheckbox.setAttribute("class", "contenedorCheckbox mb-4");
    var inputCheckbox = document.createElement("input");
    inputCheckbox.setAttribute("type", "checkbox");
    inputCheckbox.setAttribute("id", "("+razonSocialAccionaria+") Acta asamblea");
    inputCheckbox.setAttribute("onclick", "deshabilitarSeccionActaAsamblea(this)")
    var parrafoInfoCheckbox = document.createElement("p");
    var textoParrafoInfoCheckbox = document.createTextNode("Esta incluida en el acta constitutiva.");
    parrafoInfoCheckbox.appendChild(textoParrafoInfoCheckbox);

    divContenedorCheckbox.append(inputCheckbox);
    divContenedorCheckbox.append(parrafoInfoCheckbox);

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", "("+razonSocialAccionaria+") Acta asamblea");
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    var divContenedorButtonAgregarCampoActaAsamblea = document.createElement("div");
    //divContenedorButtonAgregarCampoActaAsamblea.setAttribute("id", "contenedorbtnAgregarCampoActaAsamblea");
    divContenedorButtonAgregarCampoActaAsamblea.setAttribute("id", "contenedorButtonAgregar("+razonSocialAccionaria+") Acta asamblea");
    divContenedorButtonAgregarCampoActaAsamblea.setAttribute("class", "contenedorbtnAgregarCampoActaAsamblea");
    var buttonAgregarCampoActaAsamblea = document.createElement("button");
    buttonAgregarCampoActaAsamblea.setAttribute("type", "button");
    //buttonAgregarCampoActaAsamblea.setAttribute("id", "contenedorbtnAgregarCampoActaAsamblea");
    buttonAgregarCampoActaAsamblea.setAttribute("id", "("+razonSocialAccionaria+") Acta asamblea");
    buttonAgregarCampoActaAsamblea.setAttribute("class", "btn btn-primary");
    buttonAgregarCampoActaAsamblea.setAttribute("onclick", "agregarCampoActaAsamblea(this)");
    var textoButtonAgregarCampoActaAsamblea = document.createTextNode("Agregar acta de asamblea adicional");
    buttonAgregarCampoActaAsamblea.appendChild(textoButtonAgregarCampoActaAsamblea);

    divContenedorButtonAgregarCampoActaAsamblea.append(buttonAgregarCampoActaAsamblea);

    divContenedorSeccionActaAsamblea.append(labelTituloSeccionFile);
    divContenedorSeccionActaAsamblea.append(inputSeccionFile);
    divContenedorSeccionActaAsamblea.append(inputFile);
    divContenedorSeccionActaAsamblea.append(parrafoInfoArchivoCargado);
    divContenedorSeccionActaAsamblea.append(divContenedorCheckbox);
    divContenedorSeccionActaAsamblea.append(divContenedorButtonAgregarCampoActaAsamblea);

    
    //Seccion de Poder representante legal.
    var divContenedorSeccionPoderRepresentanteLegal = document.createElement("div");
    divContenedorSeccionPoderRepresentanteLegal.setAttribute("class", "mb-4");

    var labelTituloSeccionFile = document.createElement("label");
    labelTituloSeccionFile.setAttribute("for", "formFile");
    labelTituloSeccionFile.setAttribute("class", "form-label");
    var textoTituloSeccionFile = document.createTextNode("Poder representante legal");
    labelTituloSeccionFile.appendChild(textoTituloSeccionFile);

    var inputSeccionFile = document.createElement("input");
    inputSeccionFile.setAttribute("type", "hidden");
    inputSeccionFile.setAttribute("name", "("+razonSocialAccionaria+") Poder representante legal");
    inputSeccionFile.setAttribute("id", "("+razonSocialAccionaria+") Poder representante legal referencia");
    inputSeccionFile.setAttribute("value", "("+razonSocialAccionaria+") Poder representante legal");

    var inputFile = document.createElement("input");
    inputFile.setAttribute("type", "file");
    inputFile.setAttribute("name", "("+razonSocialAccionaria+") Poder representante legal");
    inputFile.setAttribute("id", "("+razonSocialAccionaria+") Poder representante legal");
    inputFile.setAttribute("class", "form-control");
    inputFile.setAttribute("oninput", "");
    inputFile.setAttribute("required", "");
    inputFile.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var divContenedorCheckbox = document.createElement("div");
    divContenedorCheckbox.setAttribute("class", "contenedorCheckbox");
    var inputCheckbox = document.createElement("input");
    inputCheckbox.setAttribute("type", "checkbox");
    inputCheckbox.setAttribute("id", "("+razonSocialAccionaria+") Poder representante legal");
    inputCheckbox.setAttribute("onclick", "myFunction(this)");
    var parrafoInfoCheckbox = document.createElement("p");
    var textoParrafoInfoCheckbox = document.createTextNode("Esta incluida en el acta constitutiva.");
    parrafoInfoCheckbox.appendChild(textoParrafoInfoCheckbox);

    divContenedorCheckbox.append(inputCheckbox);
    divContenedorCheckbox.append(parrafoInfoCheckbox);

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", "("+razonSocialAccionaria+") Poder representante legal");
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    divContenedorSeccionPoderRepresentanteLegal.append(labelTituloSeccionFile);
    divContenedorSeccionPoderRepresentanteLegal.append(inputSeccionFile);
    divContenedorSeccionPoderRepresentanteLegal.append(inputFile);
    divContenedorSeccionPoderRepresentanteLegal.append(parrafoInfoArchivoCargado);
    divContenedorSeccionPoderRepresentanteLegal.append(divContenedorCheckbox);


    //Seccion de Registro publico de comercio.
    var divContenedorSeccionRegistroPublicoComercio = document.createElement("div");
    divContenedorSeccionRegistroPublicoComercio.setAttribute("class", "mb-4");

    var labelTituloSeccionFile = document.createElement("label");
    labelTituloSeccionFile.setAttribute("for", "formFile");
    labelTituloSeccionFile.setAttribute("class", "form-label");
    var textoTituloSeccionFile = document.createTextNode("Registro publico de comercio");
    labelTituloSeccionFile.appendChild(textoTituloSeccionFile);

    var inputSeccionFile = document.createElement("input");
    inputSeccionFile.setAttribute("type", "hidden");
    inputSeccionFile.setAttribute("name", "("+razonSocialAccionaria+") Registro publico de comercio");
    inputSeccionFile.setAttribute("id", "("+razonSocialAccionaria+") Registro publico de comercio referencia");
    inputSeccionFile.setAttribute("value", "("+razonSocialAccionaria+") Registro publico de comercio");

    var inputFile = document.createElement("input");
    inputFile.setAttribute("type", "file");
    inputFile.setAttribute("name", "("+razonSocialAccionaria+") Registro publico de comercio");
    inputFile.setAttribute("id", "("+razonSocialAccionaria+") Registro publico de comercio");
    inputFile.setAttribute("class", "form-control");
    inputFile.setAttribute("oninput", "");
    inputFile.setAttribute("required", "");
    inputFile.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var divContenedorCheckbox = document.createElement("div");
    divContenedorCheckbox.setAttribute("class", "contenedorCheckbox");
    var inputCheckbox = document.createElement("input");
    inputCheckbox.setAttribute("type", "checkbox");
    inputCheckbox.setAttribute("id", "("+razonSocialAccionaria+") Registro publico de comercio");
    inputCheckbox.setAttribute("onclick", "myFunction(this)");
    var parrafoInfoCheckbox = document.createElement("p");
    var textoParrafoInfoCheckbox = document.createTextNode("Esta incluida en el acta constitutiva.");
    parrafoInfoCheckbox.appendChild(textoParrafoInfoCheckbox);

    divContenedorCheckbox.append(inputCheckbox);
    divContenedorCheckbox.append(parrafoInfoCheckbox);

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", "("+razonSocialAccionaria+") Registro publico de comercio");
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    divContenedorSeccionRegistroPublicoComercio.append(labelTituloSeccionFile);
    divContenedorSeccionRegistroPublicoComercio.append(inputSeccionFile);
    divContenedorSeccionRegistroPublicoComercio.append(inputFile);
    divContenedorSeccionRegistroPublicoComercio.append(parrafoInfoArchivoCargado);
    divContenedorSeccionRegistroPublicoComercio.append(divContenedorCheckbox);

    //Seccion de Cedula de identificacion fiscal.
    var divContenedorSeccionCedulaIdentificacionFiscal = document.createElement("div");
    divContenedorSeccionCedulaIdentificacionFiscal.setAttribute("class", "mb-4");

    var labelTituloSeccionFile = document.createElement("label");
    labelTituloSeccionFile.setAttribute("for", "formFile");
    labelTituloSeccionFile.setAttribute("class", "form-label");
    var textoTituloSeccionFile = document.createTextNode("Cedula de identificacion fiscal");
    labelTituloSeccionFile.appendChild(textoTituloSeccionFile);

    var inputSeccionFile = document.createElement("input");
    inputSeccionFile.setAttribute("type", "hidden");
    inputSeccionFile.setAttribute("name", "("+razonSocialAccionaria+") Cedula de identificacion fiscal");
    inputSeccionFile.setAttribute("id", "Cedula de identificacion fiscal");
    inputSeccionFile.setAttribute("value", "("+razonSocialAccionaria+") Cedula de identificacion fiscal");

    var inputFile = document.createElement("input");
    inputFile.setAttribute("type", "file");
    inputFile.setAttribute("name", "("+razonSocialAccionaria+") Cedula de identificacion fiscal");
    inputFile.setAttribute("id", "Cedula de identificacion fiscal");
    inputFile.setAttribute("class", "form-control");
    inputFile.setAttribute("oninput", "");
    inputFile.setAttribute("required", "");
    inputFile.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", "("+razonSocialAccionaria+") Cedula de identificacion fiscal");
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    divContenedorSeccionCedulaIdentificacionFiscal.append(labelTituloSeccionFile);
    divContenedorSeccionCedulaIdentificacionFiscal.append(inputSeccionFile);
    divContenedorSeccionCedulaIdentificacionFiscal.append(inputFile);
    divContenedorSeccionCedulaIdentificacionFiscal.append(parrafoInfoArchivoCargado);


    //Seccion de Comprobante de domicilio.
    var divContenedorSeccionComprobanteDomicilio = document.createElement("div");
    divContenedorSeccionComprobanteDomicilio.setAttribute("class", "mb-4");

    var labelTituloSeccionFile = document.createElement("label");
    labelTituloSeccionFile.setAttribute("for", "formFile");
    labelTituloSeccionFile.setAttribute("class", "form-label");
    var textoTituloSeccionFile = document.createTextNode("Comprobante de domicilio");
    labelTituloSeccionFile.appendChild(textoTituloSeccionFile);

    var inputSeccionFile = document.createElement("input");
    inputSeccionFile.setAttribute("type", "hidden");
    inputSeccionFile.setAttribute("name", "("+razonSocialAccionaria+") Comprobante de domicilio");
    inputSeccionFile.setAttribute("id", "Comprobante de domicilio");
    inputSeccionFile.setAttribute("value", "("+razonSocialAccionaria+") Comprobante de domicilio");

    var inputFile = document.createElement("input");
    inputFile.setAttribute("type", "file");
    inputFile.setAttribute("name", "("+razonSocialAccionaria+") Comprobante de domicilio");
    inputFile.setAttribute("id", "Comprobante de domicilio");
    inputFile.setAttribute("class", "form-control");
    inputFile.setAttribute("oninput", "");
    inputFile.setAttribute("required", "");
    inputFile.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", "("+razonSocialAccionaria+") Comprobante de domicilio");
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    divContenedorSeccionComprobanteDomicilio.append(labelTituloSeccionFile);
    divContenedorSeccionComprobanteDomicilio.append(inputSeccionFile);
    divContenedorSeccionComprobanteDomicilio.append(inputFile);
    divContenedorSeccionComprobanteDomicilio.append(parrafoInfoArchivoCargado);

    //Seccion de Identificacion oficial de representante legal.
    var divContenedorSeccionIdentificacionOficialRespresentanteLegal = document.createElement("div");
    divContenedorSeccionIdentificacionOficialRespresentanteLegal.setAttribute("class", "mb-4");

    var labelTituloSeccionFile = document.createElement("label");
    labelTituloSeccionFile.setAttribute("for", "formFile");
    labelTituloSeccionFile.setAttribute("class", "form-label");
    var textoTituloSeccionFile = document.createTextNode("Identificacion oficial de representante legal");
    labelTituloSeccionFile.appendChild(textoTituloSeccionFile);

    var inputSeccionFile = document.createElement("input");
    inputSeccionFile.setAttribute("type", "hidden");
    inputSeccionFile.setAttribute("name", "("+razonSocialAccionaria+") Identificacion oficial de representante legal");
    inputSeccionFile.setAttribute("id", "Identificacion oficial de representante legal");
    inputSeccionFile.setAttribute("value", "("+razonSocialAccionaria+") Identificacion oficial de representante legal");

    var inputFile = document.createElement("input");
    inputFile.setAttribute("type", "file");
    inputFile.setAttribute("name", "("+razonSocialAccionaria+") Identificacion oficial de representante legal");
    inputFile.setAttribute("id", "Identificacion oficial de representante legal");
    inputFile.setAttribute("class", "form-control");
    inputFile.setAttribute("oninput", "");
    inputFile.setAttribute("required", "");
    inputFile.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", "("+razonSocialAccionaria+") Identificacion oficial de representante legal");
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    divContenedorSeccionIdentificacionOficialRespresentanteLegal.append(labelTituloSeccionFile);
    divContenedorSeccionIdentificacionOficialRespresentanteLegal.append(inputSeccionFile);
    divContenedorSeccionIdentificacionOficialRespresentanteLegal.append(inputFile);
    divContenedorSeccionIdentificacionOficialRespresentanteLegal.append(parrafoInfoArchivoCargado);


    //Seccion de Comprobante de la generacion de la e.firma (Razon social).
    var divContenedorSeccionComprobanteGeneracionEFirmaRazonSocial = document.createElement("div");
    divContenedorSeccionComprobanteGeneracionEFirmaRazonSocial.setAttribute("class", "mb-4");

    var labelTituloSeccionFile = document.createElement("label");
    labelTituloSeccionFile.setAttribute("for", "formFile");
    labelTituloSeccionFile.setAttribute("class", "form-label");
    var textoTituloSeccionFile = document.createTextNode("Comprobante de la generacion de la e.firma (Razon social)");
    labelTituloSeccionFile.appendChild(textoTituloSeccionFile);

    var inputSeccionFile = document.createElement("input");
    inputSeccionFile.setAttribute("type", "hidden");
    inputSeccionFile.setAttribute("name", "("+razonSocialAccionaria+") Comprobante de la generacion de la e.firma (Razon social)");
    inputSeccionFile.setAttribute("id", "Comprobante de la generacion de la e.firma (Razon social)");
    inputSeccionFile.setAttribute("value", "("+razonSocialAccionaria+") Comprobante de la generacion de la e.firma (Razon social)");

    var inputFile = document.createElement("input");
    inputFile.setAttribute("type", "file");
    inputFile.setAttribute("name", "("+razonSocialAccionaria+") Comprobante de la generacion de la e.firma (Razon social)");
    inputFile.setAttribute("id", "Comprobante de la generacion de la e.firma (Razon social)");
    inputFile.setAttribute("class", "form-control");
    inputFile.setAttribute("oninput", "");
    inputFile.setAttribute("required", "");
    inputFile.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", "("+razonSocialAccionaria+") Comprobante de la generacion de la e.firma (Razon social)");
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    divContenedorSeccionComprobanteGeneracionEFirmaRazonSocial.append(labelTituloSeccionFile);
    divContenedorSeccionComprobanteGeneracionEFirmaRazonSocial.append(inputSeccionFile);
    divContenedorSeccionComprobanteGeneracionEFirmaRazonSocial.append(inputFile);
    divContenedorSeccionComprobanteGeneracionEFirmaRazonSocial.append(parrafoInfoArchivoCargado);

    //Seccion de Comprobante de la generacion de la e.firma (Representante legal).
    var divContenedorSeccionComprobanteGeneracionEFirmaRepresentanteLegal = document.createElement("div");
    divContenedorSeccionComprobanteGeneracionEFirmaRepresentanteLegal.setAttribute("class", "mb-4");

    var labelTituloSeccionFile = document.createElement("label");
    labelTituloSeccionFile.setAttribute("for", "formFile");
    labelTituloSeccionFile.setAttribute("class", "form-label");
    var textoTituloSeccionFile = document.createTextNode("Comprobante de la generacion de la e.firma (Representante legal)");
    labelTituloSeccionFile.appendChild(textoTituloSeccionFile);

    var inputSeccionFile = document.createElement("input");
    inputSeccionFile.setAttribute("type", "hidden");
    inputSeccionFile.setAttribute("name", "("+razonSocialAccionaria+") Comprobante de la generacion de la e.firma (Representante legal)");
    inputSeccionFile.setAttribute("id", "Comprobante de la generacion de la e.firma (Representante legal)");
    inputSeccionFile.setAttribute("value", "("+razonSocialAccionaria+") Comprobante de la generacion de la e.firma (Representante legal)");

    var inputFile = document.createElement("input");
    inputFile.setAttribute("type", "file");
    inputFile.setAttribute("name", "("+razonSocialAccionaria+") Comprobante de la generacion de la e.firma (Representante legal)");
    inputFile.setAttribute("id", "Comprobante de la generacion de la e.firma (Representante legal)");
    inputFile.setAttribute("class", "form-control");
    inputFile.setAttribute("oninput", "");
    inputFile.setAttribute("required", "");
    inputFile.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", "("+razonSocialAccionaria+") Comprobante de la generacion de la e.firma (Representante legal)");
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    divContenedorSeccionComprobanteGeneracionEFirmaRepresentanteLegal.append(labelTituloSeccionFile);
    divContenedorSeccionComprobanteGeneracionEFirmaRepresentanteLegal.append(inputSeccionFile);
    divContenedorSeccionComprobanteGeneracionEFirmaRepresentanteLegal.append(inputFile);
    divContenedorSeccionComprobanteGeneracionEFirmaRepresentanteLegal.append(parrafoInfoArchivoCargado);
    

    //Agregar inputs a seccion de Razon social accionaria
    divContenedorInputsRazonSocialAccionaria.append(divContenedorSeccionActaConstitutiva);
    divContenedorInputsRazonSocialAccionaria.append(divContenedorSeccionActaAsamblea);
    divContenedorInputsRazonSocialAccionaria.append(divContenedorSeccionPoderRepresentanteLegal);
    divContenedorInputsRazonSocialAccionaria.append(divContenedorSeccionRegistroPublicoComercio);
    divContenedorInputsRazonSocialAccionaria.append(divContenedorSeccionCedulaIdentificacionFiscal);
    divContenedorInputsRazonSocialAccionaria.append(divContenedorSeccionComprobanteDomicilio);
    divContenedorInputsRazonSocialAccionaria.append(divContenedorSeccionIdentificacionOficialRespresentanteLegal);
    divContenedorInputsRazonSocialAccionaria.append(divContenedorSeccionComprobanteGeneracionEFirmaRazonSocial);
    divContenedorInputsRazonSocialAccionaria.append(divContenedorSeccionComprobanteGeneracionEFirmaRepresentanteLegal);

    return divContenedorInputsRazonSocialAccionaria;
}







const agregarCampoActaAsamblea = (e) => {

    
    var listaInputsActaAsamblea = document.querySelectorAll("input[id='"+e.id+" referencia']");
    indiceActual = listaInputsActaAsamblea.length;
    

    var div = document.createElement("div");
    div.setAttribute("class", "mb-3");
    div.setAttribute("id", "contenedor:"+e.id+"No."+(indiceActual + 1));

    //Titulo de la seccion (documento) a tratar.
    var label = document.createElement("label");
    label.setAttribute("for", "formFile");
    label.setAttribute("class", "form-label");
    var textoNotificacionRechazo = document.createTextNode("Acta de asamblea No."+(indiceActual + 1));
    label.appendChild(textoNotificacionRechazo);

    var div2 = document.createElement("div");
    div2.setAttribute("class", "row");

    var div3 = document.createElement("div");
    div3.setAttribute("class", "col-sm-10");

    var div4 = document.createElement("div");
    div4.setAttribute("class", "col-sm-2");


    var inputSeccion = document.createElement("input");
    inputSeccion.setAttribute("type", "hidden");
    inputSeccion.setAttribute("name", e.id+" No."+(indiceActual + 1));
    inputSeccion.setAttribute("id", ""+e.id+" referencia");
    inputSeccion.value = e.id+" No."+(indiceActual + 1);
    var input = document.createElement("input");
    input.setAttribute("type", "file");
    input.setAttribute("class", "form-control");
    input.setAttribute("name", e.id+" No."+(indiceActual + 1));
    input.setAttribute("id", e.id+" No."+(indiceActual + 1));
    input.setAttribute("required", "");
    input.setAttribute("oninput", "evaluarArchivosAccionarias(this)");

    var btnEliminar = document.createElement("button");
    btnEliminar.setAttribute("type", "button");
    btnEliminar.setAttribute("class", "btn btn-danger");
    btnEliminar.setAttribute("onclick", "eliminarCampoActaAsamblea(this)");
    var textoBtnEliminar = document.createTextNode("Eliminar");
    btnEliminar.appendChild(textoBtnEliminar);

    div3.append(input);
    div4.append(btnEliminar);

    div2.append(div3);
    div2.append(div4);

    var parrafoInfoArchivoCargado = document.createElement("p");
    parrafoInfoArchivoCargado.setAttribute("id", e.id+" No."+(indiceActual + 1));
    parrafoInfoArchivoCargado.setAttribute("class", "parrafoInfo");

    var contenedorInputsActaAsamblea = document.querySelector("div[id='contenedorInputs"+e.id+"']");
    var contenedorButtonAgregarActaAsamblea = document.querySelector("div[id='contenedorButtonAgregar"+e.id+"']");

    div.append(label);
    div.append(inputSeccion);
    div.append(div2);
    div.append(parrafoInfoArchivoCargado);
    contenedorInputsActaAsamblea.insertBefore(div,contenedorButtonAgregarActaAsamblea);

}

const eliminarCampoActaAsamblea = (e) => {
    nodePadreBtn = e.parentNode;
    nodePadreDiv4 = nodePadreBtn.parentNode;
    nodePadreDiv2 = nodePadreDiv4.parentNode;

    contenedorInputsActaAsamblea = nodePadreDiv2.parentNode;
    contenedorInputsActaAsamblea.removeChild(nodePadreDiv2);
}

const myFunction = (e) => {
    if(e.checked == true){
        //var inputArchivo = document.getElementById(e.id);
        var inputArchivo = document.querySelector("input[id='"+e.id+"']");
        inputArchivo.removeAttribute("required");
        inputArchivo.removeAttribute("name");
        inputArchivo.setAttribute("readonly", "");
        inputArchivo.setAttribute("type", "text");
        inputArchivo.setAttribute("placeholder", "Ningun archivo selec.");
        //var btnAgregarCampoAsamblea = document.getElementById("btnAgregarCampoAsamblea");
        //btnAgregarCampoAsamblea.classList.add("not-active");
        var inputNodoReferencia = document.getElementById(e.id+" referencia");
        inputNodoReferencia.removeAttribute("name");
        inputNodoReferencia.removeAttribute("value");

        var parrafoInfoSeccion = document.querySelector("p[id='"+e.id+"']");
        parrafoInfoSeccion.innerHTML = "";
    }else{
        //var inputArchivo = document.getElementById(e.id);
        var inputArchivo = document.querySelector("input[id='"+e.id+"']");
        inputArchivo.setAttribute("required", "");
        inputArchivo.setAttribute("name", e.id);
        inputArchivo.setAttribute("type", "file");
        inputArchivo.removeAttribute("readonly");
        inputArchivo.removeAttribute("placeholder");
        //var btnAgregarCampoAsamblea = document.getElementById("btnAgregarCampoAsamblea");
        //sbtnAgregarCampoAsamblea.classList.remove("not-active");
        var inputNodoReferencia = document.getElementById(e.id+" referencia");
        inputNodoReferencia.setAttribute("name", e.id);
        inputNodoReferencia.setAttribute("value", e.id);
    }
}

const deshabilitarSeccionActaAsamblea = (e) => {
    var listaInputsActaAsamblea = document.querySelectorAll("input[id='"+e.id+" referencia']");
    console.log(listaInputsActaAsamblea.length);
    if(e.checked == true){
        //var inputArchivo = document.getElementById("Acta de asamblea");
        var inputArchivo = document.querySelector("input[id='"+e.id+"']")
        inputArchivo.removeAttribute("required");
        inputArchivo.removeAttribute("name");
        inputArchivo.setAttribute("readonly", "");
        inputArchivo.setAttribute("type", "text");
        inputArchivo.setAttribute("placeholder", "Ningun archivo selec.");
        //var btnAgregarCampoActaAsamblea = document.getElementById("btnAgregarCampoActaAsamblea");
        var btnAgregarCampoActaAsamblea = document.querySelector("button[id='"+e.id+"']");
        btnAgregarCampoActaAsamblea.setAttribute("disabled", "");
        var inputNodoReferencia = document.getElementById(e.id+" referencia");
        inputNodoReferencia.removeAttribute("name");
        inputNodoReferencia.removeAttribute("value");

        var parrafoInfoSeccion = document.querySelector("p[id='"+e.id+"']");
        parrafoInfoSeccion.innerHTML = "";

        for (let i = 1; i < listaInputsActaAsamblea.length; i++) {
            console.log(listaInputsActaAsamblea[i].name);
            var lg = document.getElementById("contenedor:"+e.id+"No."+(i+1));
            //var nodePadreInput = lg.parentNode;
            //var nodePadreDiv3 = nodePadreInput.parentNode;
            //var nodePadreDiv2 = nodePadreDiv3.parentNode;
            console.log(lg);
            var contenedorInputsActaAsamblea = document.getElementById("contenedorInputs"+e.id);

            contenedorInputsActaAsamblea.removeChild(lg);
        }
    }else{
        //var inputArchivo = document.getElementById(e.id);
        var inputArchivo = document.querySelector("input[id='"+e.id+"']")
        inputArchivo.setAttribute("required", "");
        inputArchivo.setAttribute("name", e.id);
        inputArchivo.setAttribute("type", "file");
        inputArchivo.removeAttribute("readonly");
        inputArchivo.removeAttribute("placeholder");
        //var btnAgregarCampoActaAsamblea = document.getElementById("btnAgregarCampoActaAsamblea");
        var btnAgregarCampoActaAsamblea = document.querySelector("button[id='"+e.id+"']");
        btnAgregarCampoActaAsamblea.removeAttribute("disabled");
        var inputNodoReferencia = document.getElementById(e.id+" referencia");
        inputNodoReferencia.setAttribute("name", e.id);
        inputNodoReferencia.setAttribute("value", e.id);
    }
}