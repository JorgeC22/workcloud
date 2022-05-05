window.onload=function(){
    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("DescargaContratoDigital", "consultaJsonDocumentos");
        var URLbaseFile = URLactual.replace("DescargaContratoDigital", "archivo");

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);

                var baseDescarga = document.getElementById('base_descarga');
                nombreDoc = json.contrato.nombreDoc;

                var btnDescarga = document.getElementById('btnDescargar');
                btnDescarga.setAttribute("href", URLbaseFile+"/"+nombreDoc);
                var textofila = document.createTextNode("Descargar Contrato");
                btnDescarga.appendChild(textofila);
            }
        }
    }
}