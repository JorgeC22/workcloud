window.onload=function(){
    cargaDatosProceso();
    function cargaDatosProceso(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("RevisionEstructuraAccionaria", "consultaJsonDocumentos");
        var URLdocumentosAccionistas = URLactual.replace("RevisionEstructuraAccionaria", "consultaJsonDocumentosAccionistas");
        //var URLbaseFile = URLactual.replace("RevisionDocumentacion", "archivo");
        var dominio = document.domain;

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);
                //var tbody = document.getElementById('bodytable');
                //var URLbaseFile = "https://"+dominio+"/archivo/"+json.id;

                var inputRazonSocial = document.getElementById('razonSocial');
                inputRazonSocial.setAttribute("value", json.cliente.razonSocial);

                var inputRfc = document.getElementById('rfc');
                inputRfc.setAttribute("value", json.cliente.rfc);

                var inputDistribuidor = document.getElementById('distribuidor');
                inputDistribuidor.setAttribute("value", json.cliente.distribuidor);

                //Tabla para la validacion de documentos de Razon social accionaria.
                var xhttp = new XMLHttpRequest();
                xhttp.open('GET',URLdocumentosAccionistas, true);
                xhttp.send();
                xhttp.onreadystatechange = function(){
                    if(this.readyState==4 && this.status==200){
                        var jsonDocumentosAccionista = JSON.parse(this.responseText);
                        
                        if (jsonDocumentosAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante != null){
                            
                            //var tbody = document.getElementById('bodytable');
                            //var URLbaseFile = "https://"+dominio+"/archivo/"+jsonDocumentosAccionista.id;
                            

                            var checkboxValidarEstructuraAccionista = document.querySelectorAll("input[id='checkboxValidarEstructuraAccionista']");
                            var labelBtnOpcionValidarEstructuraAccionista = document.querySelectorAll("label[id='labelBtnOpcionValidarEstructuraAccionista']");
                            var labelSeccionValidarEstructuraAccionista = document.getElementById("labelSeccionValidarEstructuraAccionista");
                            var inputNombreSeccionValidarEstructuraAccionista = document.getElementById("inputNombreSeccionValidarEstructuraAccionista");
                            for (let lbovea = 0; lbovea < labelBtnOpcionValidarEstructuraAccionista.length; lbovea++) {
                                labelBtnOpcionValidarEstructuraAccionista[lbovea].setAttribute("style", "color: rgb(114, 114, 114);")
                                
                            }
                            for (let ck = 0; ck < checkboxValidarEstructuraAccionista.length; ck++) {
                                checkboxValidarEstructuraAccionista[ck].disabled = true;
                                checkboxValidarEstructuraAccionista[ck].removeAttribute("name");
                                checkboxValidarEstructuraAccionista[ck].removeAttribute("required");
                                
                            }
                            labelSeccionValidarEstructuraAccionista.setAttribute("style", "color: rgb(114, 114, 114);")
                            inputNombreSeccionValidarEstructuraAccionista.removeAttribute("name");

                            var inputRazonSocialAccionista = document.getElementById("inputRazonSocialAccionista");
                            inputRazonSocialAccionista.removeAttribute("name");
                            inputRazonSocialAccionista.removeAttribute("required");
                            var inputRFC = document.getElementById("inputRFC");
                            inputRFC.removeAttribute("name");
                            inputRFC.removeAttribute("required");
                            


                            var contenedorTablasRazonSocialAccinariaDocumentos = document.getElementById("contenedorTablasRazonSocialAccinariaDocumentos");
                            var listaRazonSocialAccionariaSolicitada = jsonDocumentosAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante
                            var URLbaseFile = location.origin+"/archivo/"+jsonDocumentosAccionista.id;

                            for (let rsa = 0; rsa < jsonDocumentosAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante.length; rsa++) {
                                
                                var nombreRazonSocialAccionaria = jsonDocumentosAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante[rsa].razonSocial;
                                
                                var URLbaseDocumentosRazonSocialAccionaria = location.origin+"/consultaJsonDocumentosRazonSocialAccionaria/"+jsonDocumentosAccionista.id+"/";
                                
                                
                                //console.log(URLbaseDocumentosRazonSocialAccionaria+jsonDocumentosAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante[rsa].razonSocial);
                                //Se buscan los documentos asociados a la razon social en cuestion.
                                var xhttp = new XMLHttpRequest();
                                xhttp.open('GET',URLbaseDocumentosRazonSocialAccionaria+jsonDocumentosAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante[rsa].razonSocial, true);
                                xhttp.send();
                                xhttp.onreadystatechange = function(){
                                    if(this.readyState==4 && this.status==200){
                                        var jsonRazonSocialAccionaria = JSON.parse(this.responseText);
                                        

                                        var divContenedortablaRazonSocialAccionaria = document.createElement("div");
                                        divContenedortablaRazonSocialAccionaria.setAttribute("class", "mb-5");

                                        var labelTablaRazonSocialAccionaria = document.createElement("label");
                                        labelTablaRazonSocialAccionaria.setAttribute("class", "mb-3");
                                        var textoNombreTablaRazonSocialAccionaria = document.createTextNode("Documentos de razon social "+jsonDocumentosAccionista.validacionEstructuraAccionaria.razonSocialAccionariaDocumentacionFaltante[rsa].razonSocial);
                                        labelTablaRazonSocialAccionaria.appendChild(textoNombreTablaRazonSocialAccionaria);

                                        //Se crea elemento tabla
                                        var tablaRazonSocialAccionaria = document.createElement("table");
                                        tablaRazonSocialAccionaria.setAttribute("class", "table");

                                        //Se crea elemento tHead para encabezado de la tabla.
                                        var tHeadTabla = document.createElement("thead");
                                        tHeadTabla.setAttribute("class", "table-dark");
                                        var trCabeceraTabla = document.createElement("tr");

                                        //Se crea el renglo con los campos que tendra la tabla.
                                        var thCampoDocumento = document.createElement("th");
                                        var textoNombreCampo = document.createTextNode("Documento");
                                        thCampoDocumento.appendChild(textoNombreCampo);

                                        var thCampoLink = document.createElement("th");

                                        var thCampoAceptar = document.createElement("th");
                                        var textoNombreCampo = document.createTextNode("Aceptar");
                                        thCampoAceptar.appendChild(textoNombreCampo);

                                        var thCampoRechazar = document.createElement("th");
                                        var textoNombreCampo = document.createTextNode("Rechazar");
                                        thCampoRechazar.appendChild(textoNombreCampo);

                                        var thCampoMotivo = document.createElement("th");
                                        var textoNombreCampo = document.createTextNode("Motivo");
                                        thCampoMotivo.appendChild(textoNombreCampo);                                

                                        //Se introduce el reglo creado en el seccion de Encabezado.
                                        trCabeceraTabla.append(thCampoDocumento);
                                        trCabeceraTabla.append(thCampoLink);
                                        trCabeceraTabla.append(thCampoAceptar);
                                        trCabeceraTabla.append(thCampoRechazar);
                                        trCabeceraTabla.append(thCampoMotivo);
                                        tHeadTabla.appendChild(trCabeceraTabla);

                                        //Se agrega el Encabezado a la tabla.
                                        tablaRazonSocialAccionaria.appendChild(tHeadTabla);




                                        
                                        //Se crea el elemento tbody para definir el cuerpo de la tabla.
                                        var tBodyTabla = document.createElement("tbody");
                                        tBodyTabla.setAttribute("class", "bodyTable"); 
                                        
                                        
                                        //Se recorren todo los documentos de la razon social y se listan.
                                        for (let drsa = 0; drsa < jsonRazonSocialAccionaria.documentos.length; drsa++) {
                                            nombreArchivo = jsonRazonSocialAccionaria.documentos[drsa].nombreArchivo;
                                            filaDocumento = jsonRazonSocialAccionaria.documentos[drsa].nombreDoc;

                                            var fila = document.createElement("tr");

                                            var inputCampo = document.createElement("input");
                                            inputCampo.setAttribute("type", "hidden");
                                            inputCampo.setAttribute("name", filaDocumento);
                                            inputCampo.setAttribute("value", filaDocumento);

                                            var campo = document.createElement("td");
                                            campo.setAttribute("class", filaDocumento);
                                            var textofila = document.createTextNode(nombreArchivo);
                                            campo.appendChild(textofila);
    
                                            var ruta = document.createElement("td");
                                            ruta.setAttribute("class", filaDocumento);
                                            var btnlink = document.createElement("a");
                                            btnlink.setAttribute("href", URLbaseFile+"/"+filaDocumento);
                                            btnlink.setAttribute("target", "_blank");
                                            btnlink.setAttribute("rel", "noopener noreferrer");
                                            var textofila = document.createTextNode("Ver");
                                            btnlink.appendChild(textofila);
                                            ruta.appendChild(btnlink);
    
                                            //fila.append(inputCampo);
                                            fila.append(inputCampo);
                                            fila.append(campo);
                                            fila.append(ruta);
    
                                            //Si la validacion del documento no es "true" se permite visualizar botones para su proxima validacion del mismo.
                                            if (jsonRazonSocialAccionaria.documentos[drsa].validacion != true){
                                                var btnAceptar = document.createElement("td");
                                                btnAceptar.setAttribute("class", filaDocumento);
                                                var inputAceptar = document.createElement("input");
                                                inputAceptar.setAttribute('class', 'form-check-input');
                                                inputAceptar.setAttribute('id', 'flexRadioDefault1');
                                                inputAceptar.setAttribute('type', 'radio');
                                                inputAceptar.setAttribute('required', "");
                                                inputAceptar.setAttribute('name', filaDocumento);
                                                inputAceptar.setAttribute('value', true);
                                                inputAceptar.setAttribute('onclick', "removerCampoMotivoRechazado(this)");
                                                btnAceptar.appendChild(inputAceptar);
    
                                                var btnRechazar = document.createElement("td");
                                                btnRechazar.setAttribute("class", filaDocumento);
                                                var inputRechazar = document.createElement("input");
                                                inputRechazar.setAttribute('class', 'form-check-input');
                                                inputRechazar.setAttribute('id', 'flexRadioDefault1');
                                                inputRechazar.setAttribute('type', 'radio');
                                                inputRechazar.setAttribute('name', filaDocumento);
                                                inputRechazar.setAttribute('value', "");
                                                inputRechazar.setAttribute('onclick', "agregarCampoMotivoRechazado(this)");
                                                btnRechazar.appendChild(inputRechazar);
    
                                                fila.appendChild(btnAceptar);
                                                fila.appendChild(btnRechazar);
                                            }
                                            tBodyTabla.appendChild(fila);
                                        }
                                        tablaRazonSocialAccionaria.appendChild(tBodyTabla);

                                        divContenedortablaRazonSocialAccionaria.append(labelTablaRazonSocialAccionaria);
                                        divContenedortablaRazonSocialAccionaria.append(tablaRazonSocialAccionaria);
                                        contenedorTablasRazonSocialAccinariaDocumentos.append(divContenedortablaRazonSocialAccionaria);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


const evaluarEstructuraAccionistaCompleta = (e) => {
    var contenedorInputsRevisionEstructuraAccionistas = document.getElementById("contenedorInputsRevisionEstructuraAccionistas");
    
    if (e.checked){
        if (e.value == "true"){
            

            var contenedorInputRazonSocialAccionista = document.getElementById("contenedorInputRazonSocialAccionista");
            var inputRazonSocialAccionista = document.getElementById("inputRazonSocialAccionista");
            contenedorInputRazonSocialAccionista.setAttribute("style", "display: none;");
            inputRazonSocialAccionista.removeAttribute("name");
            inputRazonSocialAccionista.removeAttribute("required");
            inputRazonSocialAccionista.value = "";
            var inputRFC = document.getElementById("inputRFC");
            inputRFC.removeAttribute("name");
            inputRFC.removeAttribute("required");
            inputRFC.value = "";
            var contenedorNuevosInputsRazonSocialAccionaria = document.getElementById("contenedorNuevosInputsRazonSocialAccionaria");
            contenedorNuevosInputsRazonSocialAccionaria.innerHTML = "";
            //if (contenedorInputRazonSocialAccionista != null){
            //    contenedorInputsRevisionEstructuraAccionistas.removeChild(contenedorInputRazonSocialAccionista);
            //}

        }else{
            var contenedorInputRazonSocialAccionista = document.getElementById("contenedorInputRazonSocialAccionista");
            var inputRazonSocialAccionista = document.getElementById("inputRazonSocialAccionista");
            contenedorInputRazonSocialAccionista.removeAttribute("style");
            inputRazonSocialAccionista.setAttribute("name", "razonSocialAccionista");
            inputRazonSocialAccionista.setAttribute("required", "");
            var inputRFC = document.getElementById("inputRFC");
            inputRFC.setAttribute("name", "razonSocialAccionista");
            inputRFC.setAttribute("required", "");

        }
    }
}



const agregarCampoMotivoRechazado = (e) => {
    var d = document.querySelectorAll("input[onclick='removerCampoMotivoRechazado(this)']");
    c = 0;
    for (let i = 0; i < d.length; i++) {
        if (d[i].checked){
            c-=1;
        } 
    }

    if (c == d.length){
        //var checkboxValidarEstructuraAccionista = document.getElementById("checkboxValidarEstructuraAccionista");
        var checkboxValidarEstructuraAccionista = document.querySelectorAll("input[id='checkboxValidarEstructuraAccionista");
        var labelBtnOpcionValidarEstructuraAccionista = document.querySelectorAll("label[id='labelBtnOpcionValidarEstructuraAccionista']");
        var labelSeccionValidarEstructuraAccionista = document.getElementById("labelSeccionValidarEstructuraAccionista");
        var inputNombreSeccionValidarEstructuraAccionista = document.getElementById("inputNombreSeccionValidarEstructuraAccionista");
        //var contenedorInputLinkDocumentosAccionistas = document.getElementById("contenedorInputLinkDocumentosAccionistas");
        
        for (let lbovea = 0; lbovea < labelBtnOpcionValidarEstructuraAccionista.length; lbovea++) {
            labelBtnOpcionValidarEstructuraAccionista[lbovea].removeAttribute("style")
            
        }
        for (let ck = 0; ck < checkboxValidarEstructuraAccionista.length; ck++) {
            checkboxValidarEstructuraAccionista[ck].disabled = false;
            checkboxValidarEstructuraAccionista[ck].setAttribute("name", "checkboxValidarEstructuraAccionista");
            checkboxValidarEstructuraAccionista[ck].setAttribute("required", "");
            
        }
        
        ///checkboxValidarEstructuraAccionista.removeAttribute("disabled");
        labelSeccionValidarEstructuraAccionista.removeAttribute("style")
        inputNombreSeccionValidarEstructuraAccionista.setAttribute("name", "checkboxValidarEstructuraAccionista");
        //if (checkboxValidarEstructuraAccionista.checked){
        //    contenedorInputLinkDocumentosAccionistas.removeAttribute("style");
        //}
    }else{
        //var checkboxValidarEstructuraAccionista = document.getElementById("checkboxValidarEstructuraAccionista");
        var checkboxValidarEstructuraAccionista = document.querySelectorAll("input[id='checkboxValidarEstructuraAccionista");

        var labelBtnOpcionValidarEstructuraAccionista = document.querySelectorAll("label[id='labelBtnOpcionValidarEstructuraAccionista']");
        var labelSeccionValidarEstructuraAccionista = document.getElementById("labelSeccionValidarEstructuraAccionista");
        var inputNombreSeccionValidarEstructuraAccionista = document.getElementById("inputNombreSeccionValidarEstructuraAccionista");
        //var contenedorInputLinkDocumentosAccionistas = document.getElementById("contenedorInputLinkDocumentosAccionistas");
        //var linkDocumentosAccionistas = document.getElementById("linkDocumentosAccionistas");

        for (let lbovea = 0; lbovea < labelBtnOpcionValidarEstructuraAccionista.length; lbovea++) {
            labelBtnOpcionValidarEstructuraAccionista[lbovea].setAttribute("style", "color: rgb(114, 114, 114);")
            
        }
        for (let ck = 0; ck < checkboxValidarEstructuraAccionista.length; ck++) {
            checkboxValidarEstructuraAccionista[ck].disabled = true;
            checkboxValidarEstructuraAccionista[ck].removeAttribute("name");
            checkboxValidarEstructuraAccionista[ck].removeAttribute("required");
            
        }
        ///checkboxValidarEstructuraAccionista.setAttribute("disabled", ""); 
        labelSeccionValidarEstructuraAccionista.setAttribute("style", "color: rgb(114, 114, 114);")
        inputNombreSeccionValidarEstructuraAccionista.removeAttribute("name");
        //contenedorInputLinkDocumentosAccionistas.setAttribute("style", "display: none");
        //linkDocumentosAccionistas.value = "";
    }

    elemtPadreChechbox = e.parentNode;
    elemtPadreTd = elemtPadreChechbox.parentNode;
    console.log(elemtPadreTd);
    numeroElemntosFila = elemtPadreChechbox.parentNode.childElementCount;

    if (numeroElemntosFila == 5){
        var nuevoCampo = document.createElement("td");
        nuevoCampo.setAttribute("class", e.name);
        var nuevoInputTextoMotivo = document.createElement("input");
        nuevoInputTextoMotivo.setAttribute("name", e.name);
        nuevoInputTextoMotivo.setAttribute("id", e.name+" Motivo");
        nuevoInputTextoMotivo.setAttribute("required", "");
        nuevoCampo.appendChild(nuevoInputTextoMotivo);
        elemtPadreTd.appendChild(nuevoCampo);
    }
}


const removerCampoMotivoRechazado = (e) => {

    var d = document.querySelectorAll("input[onclick='removerCampoMotivoRechazado(this)']");
    c = 0;
    for (let i = 0; i < d.length; i++) {
        if (d[i].checked){
            c+=1;
        } 
    }

    if (c == d.length){
        ///var checkboxValidarEstructuraAccionista = document.getElementById("checkboxValidarEstructuraAccionista");
        var checkboxValidarEstructuraAccionista = document.querySelectorAll("input[id='checkboxValidarEstructuraAccionista']");
        var labelBtnOpcionValidarEstructuraAccionista = document.querySelectorAll("label[id='labelBtnOpcionValidarEstructuraAccionista']");
        var labelSeccionValidarEstructuraAccionista = document.getElementById("labelSeccionValidarEstructuraAccionista");
        var inputNombreSeccionValidarEstructuraAccionista = document.getElementById("inputNombreSeccionValidarEstructuraAccionista");
        //var contenedorInputLinkDocumentosAccionistas = document.getElementById("contenedorInputLinkDocumentosAccionistas");

        for (let lbovea = 0; lbovea < labelBtnOpcionValidarEstructuraAccionista.length; lbovea++) {
            labelBtnOpcionValidarEstructuraAccionista[lbovea].removeAttribute("style")
            
        }
        for (let ck = 0; ck < checkboxValidarEstructuraAccionista.length; ck++) {
            checkboxValidarEstructuraAccionista[ck].disabled = false;
            checkboxValidarEstructuraAccionista[ck].setAttribute("name", "checkboxValidarEstructuraAccionista");
            checkboxValidarEstructuraAccionista[ck].setAttribute("required", "");
            
        }

        ///checkboxValidarEstructuraAccionista.removeAttribute("disabled");
        labelSeccionValidarEstructuraAccionista.removeAttribute("style")
        inputNombreSeccionValidarEstructuraAccionista.setAttribute("name", "checkboxValidarEstructuraAccionista");
        //if (checkboxValidarEstructuraAccionista.checked){
        //    contenedorInputLinkDocumentosAccionistas.removeAttribute("style");
        //}
    }else{
        ///var checkboxValidarEstructuraAccionista = document.getElementById("checkboxValidarEstructuraAccionista");
        var checkboxValidarEstructuraAccionista = document.querySelectorAll("input[id='checkboxValidarEstructuraAccionista");
        var labelBtnOpcionValidarEstructuraAccionista = document.querySelectorAll("label[id='labelBtnOpcionValidarEstructuraAccionista']");
        var labelSeccionValidarEstructuraAccionista = document.getElementById("labelSeccionValidarEstructuraAccionista");
        var inputNombreSeccionValidarEstructuraAccionista = document.getElementById("inputNombreSeccionValidarEstructuraAccionista");
        //var contenedorInputLinkDocumentosAccionistas = document.getElementById("contenedorInputLinkDocumentosAccionistas");
        //var linkDocumentosAccionistas = document.getElementById("linkDocumentosAccionistas");

        for (let lbovea = 0; lbovea < labelBtnOpcionValidarEstructuraAccionista.length; lbovea++) {
            labelBtnOpcionValidarEstructuraAccionista[lbovea].setAttribute("style", "color: rgb(114, 114, 114);")
            
        }
        for (let ck = 0; ck < checkboxValidarEstructuraAccionista.length; ck++) {
            checkboxValidarEstructuraAccionista[ck].disabled = true;
            checkboxValidarEstructuraAccionista[ck].removeAttribute("name");
            checkboxValidarEstructuraAccionista[ck].removeAttribute("required");
            
        }
        ///checkboxValidarEstructuraAccionista.setAttribute("disabled", ""); 
        labelSeccionValidarEstructuraAccionista.setAttribute("style", "color: rgb(114, 114, 114);")
        inputNombreSeccionValidarEstructuraAccionista.removeAttribute("name");
        //contenedorInputLinkDocumentosAccionistas.setAttribute("style", "display: none");
        //linkDocumentosAccionistas.value = "";
    }

    elemtPadreChechbox = e.parentNode;
    elemtPadreTd = elemtPadreChechbox.parentNode;
    numeroElemntosFila = elemtPadreChechbox.parentNode.childElementCount;


    if (numeroElemntosFila > 5){
        indiceCampoTabla = numeroElemntosFila - 2;
        var campoTextoMotivo = document.getElementsByClassName(e.name)[indiceCampoTabla];
        elemtPadreTd.removeChild(campoTextoMotivo);
    }
}


//funcion para agregar nuevo campo de Razon social accionaria.
const agregarCampoRazonSocialAccionaria = (e) => {
    

    var contenedorNuevosInputsRazonSocialAccionaria = document.getElementById("contenedorNuevosInputsRazonSocialAccionaria");

    //Selecciona todos los inputs referencia para crear un indice exacto.
    var inputRazonSocialAccionista = document.querySelectorAll("input[name='razonSocialAccionariaDocumentacionSolicitada']");
    indiceActual = inputRazonSocialAccionista.length;

    //Se crea el contenedor que princal de la nueva seccion.
    var div = document.createElement("div");
    div.setAttribute("class", "mb-3");
    div.setAttribute("id", "contenedor:inputRazonSocialAccionista No."+(indiceActual));

    //Se crea titulo del campo Razon social accionaria.
    var labelCampoRazonSocialAccinaria = document.createElement("label");
    labelCampoRazonSocialAccinaria.setAttribute("for", "formFile");
    labelCampoRazonSocialAccinaria.setAttribute("class", "form-label");
    var textoNotificacionRechazo = document.createTextNode("Razon Social No."+(indiceActual));
    labelCampoRazonSocialAccinaria.appendChild(textoNotificacionRechazo);

    //Se crea titulo del campo RFC.
    var labelCampoRFC = document.createElement("label");
    labelCampoRFC.setAttribute("for", "formFile");
    labelCampoRFC.setAttribute("class", "form-label");
    var textoNotificacionRechazo = document.createTextNode("RFC");
    labelCampoRFC.appendChild(textoNotificacionRechazo);

    //Se crea el contenedor que contendra los inputs de la fila requerida.
    var div2 = document.createElement("div");
    div2.setAttribute("class", "row");
    div2.setAttribute("style","align-items: end;");

    //Se crea el contenedor para el campo "Razon social accionaria".
    var div3 = document.createElement("div");
    div3.setAttribute("class", "col-sm-5");

    //Se crea contenedor para el boton eliminar campo.
    var div4 = document.createElement("div");
    div4.setAttribute("class", "col-sm-2");

    //Se crea contenedor para el boton eliminar campo.
    var div5 = document.createElement("div");
    div5.setAttribute("class", "col-sm-5");

    //Se crea input no visible utilizado como referencia de la seccion. 
    var inputSeccion = document.createElement("input");
    inputSeccion.setAttribute("type", "hidden");
    inputSeccion.setAttribute("name", "razonSocialAccionariaDocumentacionSolicitada");
    inputSeccion.setAttribute("id", "inputRazonSocialAccionista No."+(indiceActual)+"Lista");
    //inputSeccion.value = "inputRazonSocialAccionista No."+(indiceActual);
    
    //Se crea input para ingresar rason social accionaria.
    var inputRazonSocialAccionaria = document.createElement("input");
    inputRazonSocialAccionaria.setAttribute("type", "text");
    inputRazonSocialAccionaria.setAttribute("class", "form-control");
    inputRazonSocialAccionaria.setAttribute("name", "inputRazonSocialAccionista No."+(indiceActual));
    inputRazonSocialAccionaria.setAttribute("id", "inputRazonSocialAccionista No."+(indiceActual));
    inputRazonSocialAccionaria.setAttribute("oninput", "evaluarRazonSocial(this)")
    inputRazonSocialAccionaria.setAttribute("required", "")

    //Se crea input para ingresar RFC de razon social accionaria.
    var inputRFC = document.createElement("input");
    inputRFC.setAttribute("type", "text");
    inputRFC.setAttribute("class", "form-control");
    inputRFC.setAttribute("name", "inputRazonSocialAccionista No."+(indiceActual));
    inputRFC.setAttribute("id", "inputRFC");
    inputRFC.setAttribute("required", "");

    //Se crea boton para eliminar campo razon social accionaria.
    var btnEliminar = document.createElement("button");
    btnEliminar.setAttribute("type", "button");
    btnEliminar.setAttribute("class", "btn btn-danger");
    btnEliminar.setAttribute("onclick", "eliminarCampoRazonSocialAccionaria(this)");
    var textoBtnEliminar = document.createTextNode("Eliminar");
    btnEliminar.appendChild(textoBtnEliminar);

    //Se agregan nuevos elementos a sus campos correspondientes.
    div3.append(labelCampoRazonSocialAccinaria);
    div3.append(inputRazonSocialAccionaria);
    div4.append(btnEliminar);
    div5.append(labelCampoRFC);
    div5.append(inputRFC);

    //Se agregan contenedores al contenedor fila de la razon social accionaria.
    div2.append(div3);
    div2.append(div5);
    div2.append(div4);

    //Se obtiene el contenedo en donde se introducira nueva seccion.
    var contenedorInputRazonSocialAccionista = document.getElementById("contenedorInputRazonSocialAccionista");
    //Se obtiene contenedor que se utilizara como referencia para insercion de la nueva seccion.
    var contenedorbtnAgregarRazonSocialAccionaria = document.getElementById("contenedorbtnAgregarRazonSocialAccionaria");

    //Se agregan elementos al contenedor principal.
    //div.append(label);
    div.append(inputSeccion);
    div.append(div2);
    contenedorNuevosInputsRazonSocialAccionaria.append(div);
    //Se agrega nueva seccion al contenedor general de Razon Social accionaria.
    //contenedorInputRazonSocialAccionista.insertBefore(div,contenedorbtnAgregarRazonSocialAccionaria);
}

const eliminarCampoRazonSocialAccionaria = (e) => {
    //Se obtiene el nodo principal de la seccion.
    nodePadreBtn = e.parentNode;
    nodePadreDiv4 = nodePadreBtn.parentNode;
    nodePadreDiv2 = nodePadreDiv4.parentNode;

    //Se obtiene el contenedor que contiene las secciones agregadas.
    //var contenedorInputRazonSocialAccionista = document.getElementById("contenedorInputRazonSocialAccionista");
    var contenedorNuevosInputsRazonSocialAccionaria = document.getElementById("contenedorNuevosInputsRazonSocialAccionaria");
    contenedorNuevosInputsRazonSocialAccionaria.removeChild(nodePadreDiv2);//Se elimina el nodo dentro del contenedor.
}



const evaluarRazonSocial = (e) => {
    //id="prueba" name="razonSocialAccionariaDocumentacionSolicitada"

    var p = document.querySelector("input[id='"+e.id+"Lista'][name='razonSocialAccionariaDocumentacionSolicitada']");
    p.value = e.value;
}