window.onload=function(){
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
                for (var i = 0; i < json.length; i++) {
                    console.log(json[i]);
                    var pagina = json[i].tarea;
                    pagina = camelCase(pagina);
                    pagina = removeAccents(pagina)
                    
                    var renglon = document.createElement("tr");

                    var idProceso = document.createElement("td");
                    var textoCampo = document.createTextNode(json[i].id);
                    idProceso.appendChild(textoCampo);

                    var tarea = document.createElement("td");
                    var textoCampo = document.createTextNode(json[i].tarea);
                    tarea.appendChild(textoCampo);

                    var fechahora = document.createElement("td");
                    var textoCampo = document.createTextNode(json[i].fechaHora);
                    fechahora.appendChild(textoCampo);

                    var btn = document.createElement("td");
                    var btnInstancia = boton("Abrir Instancia",URLbase+pagina+"/"+json[i].id,"btn btn-success","abrirInstancia");
                    btn.appendChild(btnInstancia);

                    renglon.appendChild(idProceso);
                    renglon.appendChild(tarea);
                    renglon.appendChild(fechahora);
                    renglon.appendChild(btn);
                    tablebody.appendChild(renglon);
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