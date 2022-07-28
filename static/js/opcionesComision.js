var inputCashOutCantidad = document.getElementById('inputCashOutCantidad');
inputCashOutCantidad.setAttribute("oninput", "caracteristicasCampoPorcentual(this);");
inputCashOutCantidad.setAttribute("placeholder", "0.00%");
var inputCashInCantidad = document.getElementById('inputCashInCantidad');
inputCashInCantidad.setAttribute("oninput", "caracteristicasCampoPorcentual(this);");
inputCashInCantidad.setAttribute("placeholder", "0.00%");

function getValorSelectOut(e){
    var inputCashOutCantidad = document.getElementById('inputCashOutCantidad');

    if (e.value == "Porcentaje"){
        inputCashOutCantidad.value = "";
        inputCashOutCantidad.setAttribute("oninput", "caracteristicasCampoPorcentual(this);");
        inputCashOutCantidad.setAttribute("placeholder", "0.00%");
    }else if (e.value == "Fijo"){
        inputCashOutCantidad.value = "";
        inputCashOutCantidad.setAttribute("oninput", "caracteristicasCampoFijo(this);");
        inputCashOutCantidad.setAttribute("placeholder", "0.00");
    }
};

function getValorSelectIn(e){
    var inputCashInCantidad = document.getElementById('inputCashInCantidad');

    if (e.value == "Porcentaje"){
        inputCashInCantidad.value = "";
        inputCashInCantidad.setAttribute("oninput", "caracteristicasCampoPorcentual(this);");
        inputCashInCantidad.setAttribute("placeholder", "0.00%");
    }else if (e.value == "Fijo"){
        inputCashInCantidad.value = "";
        inputCashInCantidad.setAttribute("oninput", "caracteristicasCampoFijo(this);");
        inputCashInCantidad.setAttribute("placeholder", "0.00");
    }
};

function caracteristicasCampoPorcentual(e){
    var cadena = String(e.value);
    contienePuntoDecimal = cadena.includes(".");
    var posicionPuntoDecimal = cadena.indexOf(".");
    var cont = 0;


    for (let c = posicionPuntoDecimal+1; c < cadena.length; c++) {
        cont+=1;
    }   
    

    if (contienePuntoDecimal){
        var splitString = cadena.split(".");
        var decimales = splitString[1];
        if (cont >= 2){
            var decimalesModificado = decimales.slice(0,2);
        }else{
            var decimalesModificado = decimales;
        }
        splitString[1] = decimalesModificado;
        var nuevaCadena = splitString.join(".");
        e.value = nuevaCadena;
    }
    else{
        var nuevaCadena = cadena;
    }


    if (e.value > 100){
        e.value = 100;
    } 
    if (e.value < 0){
        e.value = 0;
    }
};

function caracteristicasCampoFijo(e){
    var cadena = String(e.value);
    contienePuntoDecimal = cadena.includes(".");
    var posicionPuntoDecimal = cadena.indexOf(".");
    var cont = 0;


    for (let c = posicionPuntoDecimal+1; c < cadena.length; c++) {
        cont+=1;
    }   
    

    if (contienePuntoDecimal){
        var splitString = cadena.split(".");
        var decimales = splitString[1];
        if (cont >= 2){
            var decimalesModificado = decimales.slice(0,2);
        }else{
            var decimalesModificado = decimales;
        }
        splitString[1] = decimalesModificado;
        var nuevaCadena = splitString.join(".");
        e.value = nuevaCadena;
    }
    else{
        var nuevaCadena = cadena;
    }

    if (e.value < 0){
        e.value = 0;
    } 
};



