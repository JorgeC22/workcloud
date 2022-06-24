window.onload=function(){
    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("RevisionContratoDigital", "consultaJsonDocumentos");
        //var URLbaseFile = URLactual.replace("RevisionContratoDigital", "archivo");
        var dominio = document.domain;


        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);
                var URLbaseFile = "https://"+dominio+"/archivo/"+json.id;

                var inputRazonSocial = document.getElementById('razonSocial');
                inputRazonSocial.setAttribute("value", json.cliente.razonSocial);

                var inputRfc = document.getElementById('rfc');
                inputRfc.setAttribute("value", json.cliente.rfc);

                var inputDistribuidor = document.getElementById('distribuidor');
                inputDistribuidor.setAttribute("value", json.cliente.distribuidor);

                nombreArchivo = json.contrato.nombreArchivo;
                filaDocumento = json.contrato.nombreDoc;
                var tbody = document.getElementById('bodytable');
                var fila = document.createElement("tr");

                var inputCampo = document.createElement("input");
                inputCampo.setAttribute("type", "hidden");
                inputCampo.setAttribute("name", filaDocumento);
                inputCampo.setAttribute("value", filaDocumento);


                var campo = document.createElement("td");
                campo.setAttribute("class", filaDocumento)
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

                var btnAceptar = document.createElement("td");
                btnAceptar.setAttribute("class", filaDocumento);
                var inputAceptar = document.createElement("input");
                inputAceptar.setAttribute('class', 'form-check-input');
                inputAceptar.setAttribute('id', 'flexRadioDefault1');
                inputAceptar.setAttribute('type', 'radio');
                inputAceptar.setAttribute('required', "");
                inputAceptar.setAttribute('name', filaDocumento);
                inputAceptar.setAttribute('value', "true");
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

                fila.append(inputCampo);
                fila.append(campo);
                fila.append(ruta);
                fila.append(btnAceptar);
                fila.append(btnRechazar);
                tbody.append(fila);
                    
            }
        }
    }
}

const agregarCampoMotivoRechazado = (e) => {
    elemtPadreChechbox = e.parentNode;
    elemtPadreTd = elemtPadreChechbox.parentNode;
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
    elemtPadreChechbox = e.parentNode;
    elemtPadreTd = elemtPadreChechbox.parentNode;
    numeroElemntosFila = elemtPadreChechbox.parentNode.childElementCount;


    if (numeroElemntosFila > 5){
        indiceCampoTabla = numeroElemntosFila - 2;
        var campoTextoMotivo = document.getElementsByClassName(e.name)[indiceCampoTabla];
        elemtPadreTd.removeChild(campoTextoMotivo);
    }
}