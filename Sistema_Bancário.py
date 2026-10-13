import os
import subprocess

saldo = 0
historico = ""
numero_saques = 0
LIMITE_SAQUES = 3

menu = "menu\n [1] Depositar\n [2] Sacar\n [3] Extrato\n [4] Sair"


def depositar(valor):
    global saldo, historico
    if valor >= 0:
        saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        historico += f"Depósito: R$ {valor:.2f}\n\n"
    
    else:
        print("Valor de depósito inválido.")    

def sacar(valor):
    
    global saldo, numero_saques, historico
    
    if valor < saldo:
        saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        historico += f"Saque: R$ {valor:.2f}\n\n"
        numero_saques += 1
    
    elif numero_saques >= LIMITE_SAQUES:
        print("Limite de saques diários atingido.")
    
    else:
        print("Saldo insuficiente para saque.")

def extrato():
    global saldo, historico
    
    if not historico:
        print("Não foram realizadas movimentações.")
    else:
        print(historico, end="")
        
    print(f"\nSaldo atual: R$ {saldo:.2f}")



while True:
    input("Pressione Enter para continuar...")
    
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
        print("Saindo do sistema bancário.")
        break
    else:
        print("Opção inválida. Tente novamente.")