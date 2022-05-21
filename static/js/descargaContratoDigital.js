window.onload=function(){
    var URLactual = document.URL;
        var URLobtenerJsonDocumentos = URLactual.replace("DescargaContratoDigital", "consultaJsonDocumentos");
        var URLobtenerJsonNotifiacionCorreo = URLactual.replace("DescargaContratoDigital", "extraerNotificacionEmail");
        var URLbaseFile = URLactual.replace("DescargaContratoDigital", "archivo");

    usuarios();
    obtenerMesajeNotificacionCorreo();
    function usuarios(){
        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLobtenerJsonDocumentos, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);

                var inputRazonSocial = document.getElementById('razonSocial');
                inputRazonSocial.setAttribute("value", json.cliente.razonSocial);

                var inputRfc = document.getElementById('rfc');
                inputRfc.setAttribute("value", json.cliente.rfc);

                var inputDistribuidor = document.getElementById('distribuidor');
                inputDistribuidor.setAttribute("value", json.cliente.distribuidor);

                var baseDescarga = document.getElementById('base_descarga');
                nombreDoc = json.contrato.nombreDoc;

                var btnDescarga = document.getElementById('btnDescargar');
                btnDescarga.setAttribute("href", URLbaseFile+"/"+nombreDoc);
            }
        }
    }

    function obtenerMesajeNotificacionCorreo(){

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLobtenerJsonNotifiacionCorreo, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);

                var mensajeEmail = document.getElementById("msgEnvioEmail");
                var textoCampo = document.createTextNode(json.notificacion);
                mensajeEmail.appendChild(textoCampo);
            }
        }
    }
}