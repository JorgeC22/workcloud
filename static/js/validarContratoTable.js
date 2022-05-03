window.onload=function(){
    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("ValidarContrato", "consultaJsonDocumentos");

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);

                var tbody = document.getElementById('bodytable');
                var fila = document.createElement("tr");

                var inputCampo = document.createElement("input");
                inputCampo.setAttribute("type", "hidden");
                inputCampo.setAttribute("name", json.contrato.campo);
                inputCampo.setAttribute("value", json.contrato.campo);


                var campo = document.createElement("td");
                var textofila = document.createTextNode(json.contrato.campo);
                campo.appendChild(textofila);

                var ruta = document.createElement("td");
                var textofila = document.createTextNode(json.contrato.ruta);
                ruta.appendChild(textofila);

                var btnAceptar = document.createElement("td");
                var inputAceptar = document.createElement("input");
                inputAceptar.setAttribute('type', 'radio');
                inputAceptar.setAttribute('name', json.contrato.campo);
                inputAceptar.setAttribute('value', "true");
                btnAceptar.appendChild(inputAceptar);

                var btnRechazar = document.createElement("td");
                var inputRechazar = document.createElement("input");
                inputRechazar.setAttribute('type', 'radio');
                inputRechazar.setAttribute('name', json.contrato.campo);
                inputRechazar.setAttribute('value', "");
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