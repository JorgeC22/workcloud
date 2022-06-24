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
        inputCashOutCantidad.value = 0.00;
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
        inputCashInCantidad.value = 0.00;
    }
};

function caracteristicasCampoPorcentual(e){
    var t = e.value;
    var n = (t.indexOf(".") >= 0) ? (t.substr(0, t.indexOf(".")) + t.substr(t.indexOf("."), 3)) : t;
    e.value = n;
    if (e.value > 100){
        e.value = 100;
    } else if (e.value < 0){
        e.value = 0;
    }
};

function caracteristicasCampoFijo(e){
    var t = e.value;
    var n = (t.indexOf(".") >= 0) ? (t.substr(0, t.indexOf(".")) + t.substr(t.indexOf("."), 3)) : t;
    e.value = n;
    if (e.value < 0){
        e.value = 0;
    } 
};



