window.onload=function(){
    usuarios();
    function usuarios(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("pagina2", "consultaVariables");
        console.log(URLnew);

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var json = JSON.parse(this.responseText);
                
                var form_aceptarVariables = document.getElementById('form_aceptarVariables');
                form_aceptarVariables.setAttribute('action', URLnew);

                var inputIDinstanciaP = document.getElementById('idproceso');
                inputIDinstanciaP.setAttribute('value', json.idproceso);

                //var inputNombre = document.getElementById('nombre');
                //inputNombre.value = json.nombre.value;

                //var inputTarea = document.getElementById('actividad');

                console.log(json.tarea)
                if (json.tarea == "Carga documentación de razón social"){
                    
                    //var varEjemplo = boton(texto,formaction,name,value,class,id);
                    var btnAceptar = boton("Enviar Variables","/enviarVariables","","","btn btn-success","btnAceptarVar");
                    //var btnRechazar = boton("Rechazar","/acceso2","verificar","False","btn btn-danger","btnRechazarVar");

                    //form_aceptarVariables.appendChild(btnAceptar);
                    form_aceptarVariables.appendChild(btnAceptar);
                    //form_aceptarVariables.appendChild(btnRechazar);
                } 
                if (json.tarea == "Revision de Documentacion"){
                    
                    //var varEjemplo = boton(texto,formaction,name,value,class,id);
                    var btnAceptar = boton("Aceptar Variables","/acceso","valDocumentacion","true","btn btn-success","btnAceptarVar");
                    var btnRechazar = boton("Rechazar","/acceso2","valDocumentacion","false","btn btn-danger","btnRechazarVar");

                    //form_aceptarVariables.appendChild(btnAceptar);
                    form_aceptarVariables.appendChild(btnAceptar);
                    form_aceptarVariables.appendChild(btnRechazar);
                }
                if (json.tarea == "Elaboración de contrato"){
                    
                    var btnAceptar = boton("Enviar Contrato","/acceso","","","btn btn-success","btnAceptarVar");
                    //var btnRechazar = boton("Rechazar Contrato","/acceso2","verificar","False","btn btn-danger","btnRechazarVar");

                    form_aceptarVariables.appendChild(btnAceptar);
                    //form_aceptarVariables.appendChild(btnRechazar);
                }
                if (json.tarea == "Validar Contrato"){
                    
                    var btnAceptar = boton("Validar Contrato","/acceso","valContrato","true","btn btn-success","btnAceptarVar");
                    var btnRechazar = boton("Rechazar Contrato","/acceso2","valContrato","false","btn btn-danger","btnRechazarVar");

                    form_aceptarVariables.appendChild(btnAceptar);
                    form_aceptarVariables.appendChild(btnRechazar);
                }
                if (json.tarea == "Signado de contrato digital"){
                    
                    var btnAceptar = boton("Enviar Contrato Signado","/acceso","","","btn btn-success","btnAceptarVar");
                    //var btnRechazar = boton("Rechazar Contrato","/acceso2","valContrato","false","btn btn-danger","btnRechazarVar");

                    form_aceptarVariables.appendChild(btnAceptar);
                    //form_aceptarVariables.appendChild(btnRechazar);
                }
                if (json.tarea == "Descarga contrato digital"){
                    
                    var btnAceptar = boton("Descargar Contrato","/acceso","","","btn btn-success","btnAceptarVar");
                    //var btnRechazar = boton("Rechazar Contrato","/acceso2","valContrato","false","btn btn-danger","btnRechazarVar");

                    form_aceptarVariables.appendChild(btnAceptar);
                    //form_aceptarVariables.appendChild(btnRechazar);
                }
                if (json.tarea == "Carga de contrato digital firmado"){
                    
                    var btnAceptar = boton("Cargar Contrato Digital","/acceso","","","btn btn-success","btnAceptarVar");
                    //var btnRechazar = boton("Rechazar Contrato","/acceso2","valContrato","false","btn btn-danger","btnRechazarVar");

                    form_aceptarVariables.appendChild(btnAceptar);
                    //form_aceptarVariables.appendChild(btnRechazar);
                }
                if (json.tarea == "Revisión de contrato digital"){
                    
                    var btnAceptar = boton("Aceptar Contrato Digital","/acceso","valDigitalContrato","true","btn btn-success","btnAceptarVar");
                    var btnRechazar = boton("Rechazar Contrato Digital","/acceso2","valDigitalContrato","false","btn btn-danger","btnRechazarVar");

                    form_aceptarVariables.appendChild(btnAceptar);
                    form_aceptarVariables.appendChild(btnRechazar);
                }
            }
            
        };
    }
}

//Funcion para la creacion de botones submit.
function boton(texto,formaction,name,value,clase,id){
    var btnAceptar = document.createElement("button");
    btnAceptar.setAttribute('type', 'submit');
    btnAceptar.setAttribute('id', id);
    btnAceptar.setAttribute('class', clase);
    btnAceptar.setAttribute('formaction', formaction)
    btnAceptar.setAttribute('name', name),
    btnAceptar.setAttribute('value', value)
    var textoBtn = document.createTextNode(texto);
    btnAceptar.appendChild(textoBtn);
    return btnAceptar
};

//<div class="form-floating mb-3">
//                <input type="text" name="nombre" class="form-control" id="nombre" >
//               <label for="floatingInput">Nombre</label>
//            </div>

function input(type,name,classs,id){
    var divInput = document.createElement("div");
    divInput.setAttribute('class', 'form-floating mb-3');
    divInput.setAttribute('id', 'base'+id);

    var label = document.createElement("label");
    label.setAttribute('for', 'floatingInput');
    var textoLabel = document.createTextNode(texto);
    label.appendChild(textoLabel);

    var input = document.createElement("input");
    input.setAttribute('class', classs);
    input.setAttribute('name', name);
    input.setAttribute('id', id);

    divInput.append(label);
    divInput.append(input);

    return divInput
};







