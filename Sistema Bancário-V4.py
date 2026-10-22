import os
import subprocess
from datetime import tzinfo, datetime

saldo = 0
historico = ""
numero_saques = 0
numero_transacoes = 0
LIMITE_SAQUES = 3
LIMITE_TRANSACOES = 10

contas = []
clientes = []

menu = "menu\n [1] Depositar\n [2] Sacar\n [3] Extrato\n [4] Novo usuário\n [5] Listar usuários\n [6] Nova conta\n [7] Listar contas\n [8] Sair"

def log_transacoes(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {func.__name__.upper()}")
        return resultado
    return envelope

@log_transacoes
def depositar(valor, saldo, historico, numero_transacoes):
   
    if numero_transacoes >= LIMITE_TRANSACOES:
        print("Limite de transações diárias atingido.")
    
    elif valor >= 0:
        saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        historico += f"\nDepósito: R$ {valor:.2f}\n  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        numero_transacoes += 1
        
    
    else:
        print("Valor de depósito inválido.")   

    return saldo, historico, numero_transacoes

@log_transacoes
def sacar(valor , saldo = saldo, numero_saques = numero_saques, historico = historico, numero_transacoes = numero_transacoes):
    
    if numero_saques >= LIMITE_SAQUES:
        print("Limite de saques diários atingido.")

    elif numero_transacoes >= LIMITE_TRANSACOES:
        print("Limite de transações diárias atingido.")
    
    elif valor < saldo:
        saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        historico += f"\nSaque: R$ {valor:.2f}\n  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        numero_saques += 1
        numero_transacoes += 1
    
    else:
        print("Saldo insuficiente para saque.")
    
    return saldo, numero_saques, historico, numero_transacoes

@log_transacoes
def extrato(saldo, historico):
    
    
    if not historico:
        print("Não foram realizadas movimentações.")
    else:
        print(historico, end="")
        
    print(f"\nSaldo atual: R$ {saldo:.2f}")

@log_transacoes
def novo_usuario(clientes): 
    
    cpf = input('Digite o número do seu CPF: ')
    
    if cpf in [cliente[0] for cliente in clientes]:
        print("CPF já vinculado a um usuário.")

    else:
        nome = input("Digite o seu nome: ")
        nascimento = input("Digite a sua data de nascimento (dd/mm/aaaa): ").strip()
        nascimento = f"{nascimento[:2]}/{nascimento[2:4]}/{nascimento[4:]}"
        logradouro = input("Digite o logradouro: ").strip()
        numero = input("Digite o número: ").strip()
        bairro = input("Digite o bairro: ").strip()
        cidade = input("Digite a cidade: ").strip()
        uf = input("Digite a UF: ").strip()
        endereço = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf}"
        clientes.append((cpf, nome, nascimento, endereço))
        print("\n======== Usuário criado com sucesso! ========\n") 

    return clientes

@log_transacoes
def nova_conta(contas, clientes):
    
    cpf = input('Digite o número do seu CPF: ')

    cliente = next((cliente for cliente in clientes if cliente[0] == cpf), None)
    
    if cliente is None:
        print("CPF não encontrado. Por favor, crie um usuário primeiro.")
    
    elif cpf in [conta["titular"] for conta in contas]:
        print("CPF já vinculado a uma conta.\nDeseja criar uma nova conta para o mesmo CPF? (S/N)")
        resposta = input().strip().upper()
        
        if resposta == "N":
            print("======== Operação cancelada. ========")
            return contas
    
    
    contas.append({
        "agencia": "0001",
        "numero": len(contas) + 1,
        "titular": cpf
        })
    print("======== Conta criada com sucesso. ========")
    
    return contas

@log_transacoes
def listar_contas(clientes, contas):
    for conta in (contas):
        cliente = next((cliente for cliente in clientes if cliente[0] == conta["titular"]), None)
        print(f"Cliente: {cliente[1]} - Conta: {conta['numero']}")   

@log_transacoes
def listar_clientes(clientes):
    for cliente in clientes:
        print(f"Nome: {cliente[1]} - CPF: {cliente[0]} - Data de Nascimento: {cliente[2]} - Endereço: {cliente[3]}")


while True:
    
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    
    print(menu)
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        valor = float(input("Digite o valor a depositar: "))
        depositar(valor)
    elif opcao == "2":
        valor = float(input("Digite o valor a sacar: "))
        sacar(valor)
    elif opcao == "3":
        extrato()
    elif opcao == "4":
        novo_usuario(clientes)
    elif opcao == "5":
        listar_clientes(clientes)
    elif opcao == "6":
        nova_conta(contas, clientes)
    elif opcao == "7":
        listar_contas(clientes, contas)
    elif opcao == "8":  
        print("Saindo do sistema bancário.")
        break
    else:
        print("Opção inválida. Tente novamente.")
   
    input("Pressione Enter para continuar...")
