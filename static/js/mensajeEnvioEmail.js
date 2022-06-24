window.onload=function(){
    obtenerMesajeNotificacionCorreo();
    function obtenerMesajeNotificacionCorreo(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("DescargaContratoDigital", "extraerNotificacionEmail");
        var dominio = document.domain;

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
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