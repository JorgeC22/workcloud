window.onload=function(){
    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("registro", "obtenerDatosUsuarioProspecto");

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);

                var inputCorreo = document.getElementById('inputCorreo');
                inputCorreo.setAttribute("value", json.emailProspecto);
                inputCorreo.setAttribute("readonly", "");
            }
        }
    }
}