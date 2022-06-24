window.onload=function(){
    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("ElaboracionContrato", "consultaJsonDocumentos");

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);

                

                var formCargaContrato = document.getElementById("formCargaContrato");
                var inputRazonSocial = document.getElementById('razonSocial');
                inputRazonSocial.setAttribute("value", json.cliente.razonSocial);
                var inputRfc = document.getElementById('rfc');
                inputRfc.setAttribute("value", json.cliente.rfc);
                var inputDistribuidor = document.getElementById('distribuidor');
                inputDistribuidor.setAttribute("value", json.cliente.distribuidor);

                if (Object.keys(json.contrato).length == 0){
                    var divContenedorInputContratoRechazado = document.getElementById('contenedorInputContratoRechazado');
                    divContenedorInputContratoRechazado.setAttribute("style", "display: none;");
                }else{

                    var divContenedorInputContratoInicial = document.getElementById('contenedorInputContratoInicial');
                    formCargaContrato.removeChild(divContenedorInputContratoInicial);
                    var divContenedorInputContratoRechazado = document.getElementById('contenedorInputContratoRechazado');

                    if (json.contrato.validacion == false){

                        var divContenedorInputContrato = document.createElement("div");
                        divContenedorInputContrato.setAttribute("class", "mb-3 row");
    
                        var labelArchivo = document.createElement("label");
                        labelArchivo.setAttribute("for", "formFile");
                        labelArchivo.setAttribute("class", "form-label");
                        var tituloArchivo = document.createTextNode(json.contrato.nombreDoc);
                        labelArchivo.appendChild(tituloArchivo);

                        var divContenedorColumnaInputContrato = document.createElement("div");
                        divContenedorColumnaInputContrato.setAttribute("class", "col-sm-10");

                        var divContenedorColumnaValidacion = document.createElement("div");
                        divContenedorColumnaValidacion.setAttribute("class", "col-sm-2");

                        var inputArchivoSeccionReferencia = document.createElement("input");
                        inputArchivoSeccionReferencia.setAttribute("value", json.contrato.nombreDoc);
                        inputArchivoSeccionReferencia.setAttribute("name", json.contrato.nombreDoc);
                        inputArchivoSeccionReferencia.setAttribute("type", "hidden");
    
                        var inputArchivo = document.createElement("input");
                        inputArchivo.setAttribute("class", "form-control");
                        inputArchivo.setAttribute("type", "file");
                        inputArchivo.setAttribute("id", json.contrato.nombreDoc);
                        inputArchivo.setAttribute("name", json.contrato.nombreDoc);
                        inputArchivo.setAttribute("required", "");
                        divContenedorColumnaInputContrato.append(inputArchivo);
    
                        var elementoParrafoValidacion = document.createElement("p");
                        elementoParrafoValidacion.setAttribute("class", "btn btn-danger");
                        elementoParrafoValidacion.setAttribute("style", "width: 140px;");
                        var texto = document.createTextNode("Rechazado");
                        elementoParrafoValidacion.appendChild(texto);
                        divContenedorColumnaValidacion.append(elementoParrafoValidacion);
    
                        var elementoParrafoNotificacionRechazo = document.createElement("p");
                        elementoParrafoNotificacionRechazo.setAttribute("style", "font-size: 14px; background: rgba(235,230,119); border-radius: 8px;");
                        var textoNotificacionRechazo = document.createTextNode("Motivo del Rechazo: "+json.contrato.motivoRechazoContrato);
                        elementoParrafoNotificacionRechazo.appendChild(textoNotificacionRechazo);
    
                        divContenedorInputContrato.append(labelArchivo);
                        divContenedorInputContrato.append(inputArchivoSeccionReferencia);
                        divContenedorInputContrato.append(divContenedorColumnaInputContrato);
                        divContenedorInputContrato.append(divContenedorColumnaValidacion);
                        divContenedorInputContrato.append(elementoParrafoNotificacionRechazo);
                        divContenedorInputContratoRechazado.append(divContenedorInputContrato);
                    }

                }

            }
        }
    }
}