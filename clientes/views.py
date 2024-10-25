from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente
import re
from django.core import serializers
import json
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def pagina_inicial(request):
    return render(request, 'login.html')  


def adicionar_cliente(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        cep = request.POST.get('cep')
        endereco = request.POST.get('endereco')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')

        if Cliente.objects.filter(cpf=cpf).exists():
            messages.error(request, 'Um cliente com este CPF já está cadastrado.')
            return render(request, 'clientes/adicionar_cliente.html', {
                'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cep': cep,
                'endereco': endereco, 'bairro': bairro, 'cidade': cidade
            })

        cliente = Cliente(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            cpf=cpf,
            cep=cep,
            endereco=endereco,
            bairro=bairro,
            cidade=cidade
        )
        cliente.save()
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('gerenciar_clientes')  # ou outra URL conforme necessário

    return render(request, 'clientes/cliente.html')


@login_required
def consultar_cliente(request):
    query = request.GET.get('query', '')  # Obtém o termo de pesquisa do parâmetro de consulta na URL
    clientes_list = []

    # Verifica se o termo de busca é um CPF válido (somente dígitos e 11 caracteres)
    if query.isdigit() and len(query) == 11:
        clientes_list = Cliente.objects.filter(cpf=query)  # Filtra clientes pelo CPF exato

        if not clientes_list.exists():  # Se não encontrar nenhum cliente
            messages.error(request, 'Nenhum cliente encontrado com este CPF.')

    elif query:
        messages.error(request, 'Por favor, insira um CPF válido com 11 dígitos.')

    # Exibe a página de consulta de clientes com a lista filtrada
    return render(request, 'clientes/consultar_cliente.html', {'clientes': clientes_list, 'query': query})




# Função auxiliar para validar o email
def is_valid_email(email):
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return re.fullmatch(email_regex, email) is not None

def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    
    elif request.method == "POST":
        # Extrair os campos do POST
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        cep = request.POST.get('cep')
        endereco = request.POST.get('endereco')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')

        # Verificar se o CPF já está cadastrado
        cliente_existente = Cliente.objects.filter(cpf=cpf).exists()
        if cliente_existente:
            messages.error(request, 'Um cliente com este CPF já está cadastrado.')
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})
        
        # Verificar se o email é válido
        if not is_valid_email(email):
            messages.error(request, 'O email fornecido é inválido.')
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf})

        # Criar um novo cliente
        cliente = Cliente(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            cpf=cpf
        


        )

        # Salvar o cliente no banco de dados
        cliente.save()

        # Mensagem de sucesso com o nome do cliente cadastrado
        messages.success(request, f'Cadastro realizado com sucesso para {nome} {sobrenome}!')
        return redirect('clientes')  # Redireciona para a lista de clientes
       


def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']
    data = {'cliente': cliente_json, 'cliente_id': cliente_id}
    return JsonResponse(data)


def update_cliente(request, id):
    body = json.loads(request.body)

    nome = body['nome']
    sobrenome = body['sobrenome']
    email = body['email']
    cpf = body['cpf']

    cliente = get_object_or_404(Cliente, id=id)
    try:
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()
        return JsonResponse({'status': '200', 'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})
    except:
        return JsonResponse({'status': '500'})

