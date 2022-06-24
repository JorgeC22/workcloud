function evaluarArchivo(e){
    var archivo = e.files[0];

    if (archivo.type!="application/pdf"){
        e.value = "";
        var parrafoInfoSeccion = document.querySelector("p[id='"+e.name+"']");
        parrafoInfoSeccion.innerHTML = "Solo se permiten archivos de tipo PDF.";
    }else{
        if (archivo.size > 41943040){
            e.value = "";
            var parrafoInfoSeccion = document.querySelector("p[id='"+e.name+"']");
            parrafoInfoSeccion.innerHTML = "Solo se permiten archivos no mayor a 20Gb.";
        }else{
            var parrafoInfoSeccion = document.querySelector("p[id='"+e.name+"']");
            parrafoInfoSeccion.innerHTML = "";
        }
    }
};