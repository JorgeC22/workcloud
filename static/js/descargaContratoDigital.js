window.onload=function(){
    var URLactual = document.URL;
    var URLobtenerJsonDocumentos = URLactual.replace("DescargaContratoDigital", "consultaJsonDocumentos");
    var dominio = document.domain;

    localStorage.setItem('descarga', 0);
    var variableDescarga = localStorage.getItem('descarga');

    if (variableDescarga == 0){
        var btnSiguienteTarea = document.getElementById('btnSiguienteTarea');
        btnSiguienteTarea.setAttribute("disabled", "");
    }

    cargarJsonDatosProceso();
    function cargarJsonDatosProceso(){
        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLobtenerJsonDocumentos, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);
                var URLbaseFile = "https://"+dominio+"/archivo/"+json.id;
                var URLbaseFile = location.origin+"/archivo/"+json.id;

                var inputRazonSocial = document.getElementById('razonSocial');
                inputRazonSocial.setAttribute("value", json.cliente.razonSocial);

                var inputRfc = document.getElementById('rfc');
                inputRfc.setAttribute("value", json.cliente.rfc);

                var inputDistribuidor = document.getElementById('distribuidor');
                inputDistribuidor.setAttribute("value", json.cliente.distribuidor);

                var baseDescarga = document.getElementById('base_descarga');
                nombreDoc = json.contrato.nombreDoc;

                var btnDescarga = document.getElementById('btnDescargar');
                btnDescarga.setAttribute("href", URLbaseFile+"/"+json.contrato.nombreDoc);
            }
        }
    }
}

var btnDescarga = document.getElementById('btnDescargar');

btnDescarga.addEventListener("click", () => {
    localStorage.setItem('descarga', 1);

    var variableDescarga = localStorage.getItem('descarga');
    if (variableDescarga == 1){
        var btnSiguienteTarea = document.getElementById('btnSiguienteTarea');
        btnSiguienteTarea.removeAttribute("disabled");
    }
})

window.close=function(){
    localStorage.removeItem("descarga");
}
