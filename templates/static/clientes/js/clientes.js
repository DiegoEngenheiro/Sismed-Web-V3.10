
html = "<br>  <div class='row'> <div class='col-md'> <input type='text' placeholder='carro' class='form-control' name='carro' > </div> <div class='col-md'><input type='text' placeholder='Placa' class='form-control' name='placa' ></div> <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='ano'> </div> </div>"

    container.innerHTML += html

function exibir_form(tipo){

    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')

    if(tipo == "1"){
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"

    }else if(tipo == "2"){
        add_cliente.style.display = "none";
        att_cliente.style.display = "block"
    }

}


function dados_cliente(){
    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value

    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/",{
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data

    }).then(function(result){
        return result.json()
    }).then(function(data){
        document.getElementById('form-att-cliente').style.display = 'block'
        
        id = document.getElementById('id')
        id.value = data['cliente_id']

        nome = document.getElementById('nome')
        nome.value = data['cliente']['nome']

        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data['cliente']['sobrenome']

        cpf = document.getElementById('cpf')
        cpf.value = data['cliente']['cpf']

        email = document.getElementById('email')
        email.value = data['cliente']['email']

        cep = document.getElementById('cep')
        cep.value = data['cliente']['cep']

        endereco = document.getElementById('endereco')
        endereco.value = data['cliente']['endereco']

        bairro = document.getElementById('bairro')
        bairro.value = data['cliente']['bairro']

        cidade = document.getElementById('cidade')
        cidade.value = data['cliente']['cidade']
        
    })
}


function update_cliente(){
    cep = document.getElementById('cep').value
    endereco = document.getElementById('endereco').value
    bairro = document.getElementById('bairro').value
    cidade = document.getElementById('cidade').value
    sobrenome = document.getElementById('sobrenome').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value
    id = document.getElementById('id').value
    nome = document.getElementById('nome').value



    fetch('/clientes/update_cliente/' + id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf,
            cep: cep,
            endereco: endereco,
            bairro: bairro,
            cidade: cidade,
        })

    }).then(function(result){
        return result.json()
    }).then(function(data){

        if(data['status'] == '200'){
            nome = data['nome']
            sobrenome = data['sobrenome']
            email = data['email']
            cpf = data['cpf']
            cep = data['cep']
            endereco = data['endereco']
            bairro = data['bairro']
            cidade = data['cidade']
            console.log('Dados alterado com sucesso')
        }else{
            console.log('Ocorreu algum erro')
        }

    })

}
