window.onload=function(){
    cargaDatosProceso();
    function cargaDatosProceso(){
        var URLactual = document.URL;
        var URLnew = URLactual.replace("monitoreo", "datosMonitoreoProcesos");
        //var URLbaseFile = URLactual.replace("RevisionDocumentacion", "archivo");
        var dominio = document.domain;

        var xhttp = new XMLHttpRequest();
        xhttp.open('GET',URLnew, true);
        xhttp.send();
        xhttp.onreadystatechange = function(){
            if(this.readyState==4 && this.status==200){
                var jsonDatosProcesos = JSON.parse(this.responseText);

                //Si devuelve una respuesta vacia se muestra el siguiente mensaje
                if(jsonDatosProcesos.length == 0){
                    var texto = document.createTextNode("No existen movimientos en el periodo seleccionado");
                    document.getElementById("mensaje").appendChild(texto);
                }
                //De lo contrario agrega elementos al DOM HTML, creacion de la tabla
                else{
                    var tabla = document.createElement("table");
                    tabla.setAttribute("class","table");
                    tabla.setAttribute("style","font-size:13px");
                    tabla.setAttribute("id","tabla");
                    document.getElementById("data").appendChild(tabla)
                    var encabezado = document.createElement("thead");
                    encabezado.setAttribute("class", "table-dark")
                    encabezado.setAttribute("id","titulos");
                    document.getElementById("tabla").appendChild(encabezado);
                    var fila = document.createElement("tr");
                    fila.setAttribute("id","encabezado");
                    document.getElementById("titulos").appendChild(fila);
                    var cuerpo = document.createElement("tbody");
                    cuerpo.setAttribute("id","res");
                    document.getElementById("tabla").appendChild(cuerpo);
                    //Lista con los titulos de la tabla
                    var titulos =  ['Razón social','RFC','Distribuidor','Inicio de proceso','Tarea actual','Asignación de tarea actual','Responsable','Tiempo transacurrido']
                    //Genera elementos HTML al DOM, crea cada columna de la tabla con su respectivo titulo
                    for(var i of titulos){
                        var columna = document.createElement("th");
                        var texto = document.createTextNode(i);
                        columna.appendChild(texto);
                        document.getElementById("encabezado").appendChild(columna);
                    
                    } 

                    for (var i=0;i<jsonDatosProcesos.length;i++){
                        //Genera elementos HTML al DOM, pasandole el valor de cada una de las etiquetas el contenido de movimientos indicando 
                        //que elemento tomara de la lista de json contenidas en el
                        var renglon = document.createElement("tr");
                        //renglon.setAttribute("id",movimientos[i].id_cuenta_ahorro)
                        //document.getElementById("res").appendChild(renglon);
                        var celda = document.createElement("td");
                        var texto = document.createTextNode(jsonDatosProcesos[i].cliente.razonSocial);
                        celda.appendChild(texto);
                        renglon.appendChild(celda);
                        var celda = document.createElement("td");
                        var texto = document.createTextNode(jsonDatosProcesos[i].cliente.rfc);
                        celda.appendChild(texto);
                        renglon.appendChild(celda);
                        var celda = document.createElement("td");
                        var texto = document.createTextNode(jsonDatosProcesos[i].cliente.distribuidor);
                        celda.appendChild(texto);
                        renglon.appendChild(celda);
                        var celda = document.createElement("td");
                        var texto = document.createTextNode(jsonDatosProcesos[i].fechaHoraInicioProceso);
                        celda.appendChild(texto);
                        renglon.appendChild(celda);
                        var celda = document.createElement("td");
                        var texto = document.createTextNode(jsonDatosProcesos[i].tarea.nombreActividad);
                        celda.appendChild(texto);
                        renglon.appendChild(celda);
                        var celda = document.createElement("td");
                        var texto = document.createTextNode(jsonDatosProcesos[i].fechaHora);
                        celda.appendChild(texto);
                        renglon.appendChild(celda);
                        var celda = document.createElement("td");
                        var texto = document.createTextNode(jsonDatosProcesos[i].candidatoGrupoPerteneciente);
                        celda.appendChild(texto);
                        renglon.appendChild(celda);
                        var celda = document.createElement("td");
                        var texto = document.createTextNode(jsonDatosProcesos[i].tiempoTranscurrido);
                        celda.appendChild(texto);
                        renglon.appendChild(celda);
                        var celda = document.createElement("td");

                        document.getElementById("res").appendChild(renglon);
                    }

                    //Se llama a la libreria de Datatables para darle formato a la tabla y mostrar las opciones: boton, filtro, informacion, paginacion
                    $(function() {
                        $('#tabla').DataTable( {
                            language: {
                                url: "https://cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
                            },
                            dom: "<'row'<'col-sm-12 col-md-11'f><'col-sm-12 col-md-1'B>>" +
                                 "<'row'<'col-sm-12'tr>>" +
                                 "<'row'<'col-sm-12 col-md-6'li><'col-sm-12 col-md-6'p>>",
                            buttons: [
                                {
                                    extend: 'excel',
                                    footer: true,
                                    excelStyles: {
                                        //Seleccion del rango de columnas para definir el tipo de dato a moneda cuando se haga la exportacion de la tabla
                                        cells: 'E:Q',
                                        style: {
                                            numFmt: "[$$-en-ES] #,##0.00"
                                        }
                                    },
                                    text:      '<i class="fas fa-file-excel"></i> ',
                                    titleAttr: 'Exportar a Excel',
                                    className: 'btn btn-success'
                                }
                            ]
                        } );
                    } );
                }
            }
        }
    }
}




