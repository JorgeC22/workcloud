window.onload=function(){
    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("RevisiondeDocumentacion", "consultaJsonDocumentos");
        var URLbaseFile = URLactual.replace("RevisiondeDocumentacion", "archivo");
        console.log(URLnew);

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);
                console.log(json);

                var tbody = document.getElementById('bodytable');
                
                for (let i = 0; i < json.documentos.length; i++) {
                    
                    nombreDoc = json.documentos[i].nombreDoc
                    var fila = document.createElement("tr");

                    var inputCampo = document.createElement("input");
                    inputCampo.setAttribute("type", "hidden");
                    inputCampo.setAttribute("name", nombreDoc);
                    inputCampo.setAttribute("value", nombreDoc);


                    var campo = document.createElement("td");
                    var textofila = document.createTextNode(nombreDoc);
                    campo.appendChild(textofila);

                    var ruta = document.createElement("td");
                    var btnlink = document.createElement("a");
                    btnlink.setAttribute("href", URLbaseFile+"/"+nombreDoc);
                    btnlink.setAttribute("target", "_blank");
                    btnlink.setAttribute("rel", "noopener noreferrer");
                    var textofila = document.createTextNode(URLbaseFile+"/"+nombreDoc);
                    btnlink.appendChild(textofila);
                    ruta.appendChild(btnlink);

                    var btnAceptar = document.createElement("td");
                    var inputAceptar = document.createElement("input");
                    inputAceptar.setAttribute('type', 'radio');
                    inputAceptar.setAttribute('name', nombreDoc);
                    inputAceptar.setAttribute('value', true);
                    btnAceptar.appendChild(inputAceptar);

                    var btnRechazar = document.createElement("td");
                    var inputRechazar = document.createElement("input");
                    inputRechazar.setAttribute('type', 'radio');
                    inputRechazar.setAttribute('name', nombreDoc);
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
}