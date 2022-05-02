let btnMas = document.getElementById('idMas');

btnMas.addEventListener('click', () => {
    var form_envio_variables = document.getElementById('form_envio_variables');
    let btnEnviar = document.getElementById('btnEnviar');

    var labelTel = document.createElement('label');
    var textoLabel = document.createTextNode("Telefono");
    labelTel.appendChild(textoLabel);

    var inputTel = document.createElement('input');
    inputTel.setAttribute('type', 'text')
    inputTel.setAttribute('id', 'inputTelefono');
    inputTel.setAttribute('name', 'telefono');

    form_envio_variables.insertBefore(labelTel,btnEnviar)
    form_envio_variables.insertBefore(inputTel,btnEnviar)
})