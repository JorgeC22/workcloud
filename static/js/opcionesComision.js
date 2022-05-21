var inputCashOutCantidad = document.getElementById('inputCashOutCantidad');
inputCashOutCantidad.setAttribute("oninput", "caracteristicasCampoPorcentual(this);");
inputCashOutCantidad.setAttribute("placeholder", "%");
var inputCashInCantidad = document.getElementById('inputCashInCantidad');
inputCashInCantidad.setAttribute("oninput", "caracteristicasCampoPorcentual(this);");
inputCashInCantidad.setAttribute("placeholder", "%");

function getValorSelectOut(e){
    var inputCashOutCantidad = document.getElementById('inputCashOutCantidad');

    if (e.value == "Porcentaje"){
        inputCashOutCantidad.value = "";
        inputCashOutCantidad.setAttribute("oninput", "caracteristicasCampoPorcentual(this);");
        inputCashOutCantidad.setAttribute("placeholder", "%");
    }else if (e.value == "Fijo"){
        inputCashOutCantidad.value = "";
        inputCashOutCantidad.setAttribute("oninput", "caracteristicasCampoFijo(this);");
        inputCashOutCantidad.value = 0;
    }
};

function getValorSelectIn(e){
    var inputCashInCantidad = document.getElementById('inputCashInCantidad');

    if (e.value == "Porcentaje"){
        inputCashInCantidad.value = "";
        inputCashInCantidad.setAttribute("oninput", "caracteristicasCampoPorcentual(this);");
        inputCashInCantidad.setAttribute("placeholder", "%");
    }else if (e.value == "Fijo"){
        inputCashInCantidad.value = "";
        inputCashInCantidad.setAttribute("oninput", "caracteristicasCampoFijo(this);");
        inputCashInCantidad.value = 0;
    }
};

function caracteristicasCampoPorcentual(e){
    var cambio = parseInt(e.value);
    e.value = cambio;
    if (e.value > 100){
        e.value = 100;
    } else if (e.value < 0){
        e.value = 0;
    }
};

function caracteristicasCampoFijo(e){
    e.value = Math.abs(e.value)
};



