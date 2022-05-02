window.onload=function(){
    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("listaInstancias", "consultaInstancias");
        var URLbase = URLactual.replace("listaInstancias", "");
        console.log(URLnew);

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);
                console.log(json);

                var tablebody = document.getElementById('bodytable');
                console.log(json.length);

                for (var i = 0; i < json.length; i++) {
                    
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
                    pagina = json[i].tarea;
                    pagina = pagina.split(" ").join("");
                    var btnInstancia = boton("Abrir Instancia",URLbase+pagina+"/"+json[i].id,"btn btn-success","abrirInstancia");
                    btn.appendChild(btnInstancia);

                    console.log(json[i].tarea);
                    

                    renglon.appendChild(idProceso);
                    renglon.appendChild(tarea);
                    renglon.appendChild(fechahora);
                    renglon.appendChild(btn);
                    console.log(renglon);
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