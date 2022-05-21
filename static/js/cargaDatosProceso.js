window.onload=function(){
    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("CargaDocumentacionRazonSocial", "consultaJsonDocumentos");
        //var URLbaseFile = URLactual.replace("RevisionDocumentacion", "archivo");
        var dominio = document.domain;
        var prueba = location.pathname;
        console.log(prueba);

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);
                console.log("hola mundo");

                var inputRazonSocial = document.getElementById('razonSocial');
                inputRazonSocial.setAttribute("value", json.cliente.razonSocial);

                var inputRfc = document.getElementById('rfc');
                inputRfc.setAttribute("value", json.cliente.rfc);

                var inputDistribuidor = document.getElementById('distribuidor');
                inputDistribuidor.setAttribute("value", json.cliente.distribuidor);

            }
        }
    }
}