window.onload=function(){
    localStorage.clear();

    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("listaInstancias", "consultaInstancias");
        var URLbase = URLactual.replace("listaInstancias", "");

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);
                var tablebody = document.getElementById('bodytable');
                
                if (json.length > 0){
                    var parrafoInfoTablaInstancias = document.getElementById("parrafoInfoTablaInstancias");
                    parrafoInfoTablaInstancias.innerText = "";
                    for (var i = 0; i < json.length; i++) {
                        var pagina = json[i].tarea.nombreActividad;
                        pagina = camelCase(pagina);
                        pagina = removeAccents(pagina)
                        
                        var renglon = document.createElement("tr");
    
                        var idProceso = document.createElement("td");
                        var textoCampo = document.createTextNode(json[i].cliente.razonSocial);
                        idProceso.appendChild(textoCampo);
    
                        var rfc = document.createElement("td");
                        var textoCampo = document.createTextNode(json[i].cliente.rfc);
                        rfc.appendChild(textoCampo);
    
                        var tarea = document.createElement("td");
                        var textoCampo = document.createTextNode(json[i].tarea.nombreActividad);
                        tarea.appendChild(textoCampo);
    
                        if (json[i].gruposUsuario[0] == json[i].candidatoGrupoPerteneciente){
                            var responsable = document.createElement("td");
                            var textoCampo = document.createTextNode("Usted");
                            responsable.appendChild(textoCampo);
                        }else{
                            var responsable = document.createElement("td");
                            var textoCampo = document.createTextNode(json[i].candidatoGrupoPerteneciente);
                            responsable.appendChild(textoCampo);
                        }
    
                        var fechahora = document.createElement("td");
                        var textoCampo = document.createTextNode(json[i].fechaHora);
                        fechahora.appendChild(textoCampo);
    
                        renglon.appendChild(idProceso);
                        renglon.appendChild(rfc);
                        renglon.appendChild(tarea);
                        renglon.appendChild(responsable);
                        renglon.appendChild(fechahora);
    
                        if (json[i].gruposUsuario[0] == json[i].candidatoGrupoPerteneciente){
                            var btn = document.createElement("td");
                            var btnInstancia = boton("Ver Tarea",URLbase+pagina+"/"+json[i].id+"/"+json[i].idtask,"btn btn-success","abrirInstancia");
                            btn.appendChild(btnInstancia);
                            renglon.appendChild(btn);
                        }else{
                            var status = document.createElement("td");
                            var textoCampo = document.createTextNode("En proceso");
                            status.appendChild(textoCampo);
                            renglon.appendChild(status);
                        }
    
                        tablebody.appendChild(renglon);
                    }
                }else{
                    var parrafoInfoTablaInstancias = document.getElementById("parrafoInfoTablaInstancias");
                    parrafoInfoTablaInstancias.innerText = "No tiene tareas pendientes por el momento.";
                }
            }
        };
    }
}

//Funcion para la creacion de botones submit.
function boton(texto,href,clase,id){
    var btnAceptar = document.createElement("a");
    //btnAceptar.setAttribute('type', 'submit');
    btnAceptar.setAttribute('id', id);
    btnAceptar.setAttribute('class', clase);
    btnAceptar.setAttribute('href', href);
    var textoBtn = document.createTextNode(texto);
    btnAceptar.appendChild(textoBtn);
    return btnAceptar
};


function camelCase(frase){
    var listaCadenas = frase.split(" ");
    for (let i = 0; i < listaCadenas.length; i++) {
        listaCadenas[i] = listaCadenas[i].replace(listaCadenas[i][0],listaCadenas[i][0].toUpperCase());
    }

    var nuevaCadena = listaCadenas.join("#");
    var cadenaSinSeparadores = nuevaCadena.replace(/#/g, " ");
    var cadenaSinConectores = cadenaSinSeparadores.replace(/ De | Y | A | Por /g, "");
    var cadenaFinal = cadenaSinConectores.replace(/ /g, "");
    return cadenaFinal
}

const removeAccents = (str) => {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  } 