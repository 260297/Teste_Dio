import textwrap

def menu():
    menu_text = """
    ================ MENU ================
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q]  Sair
    => """
    return input(textwrap.dedent(menu_text))

def depositar(saldo, valor):
    if valor > 0:
        saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return saldo, f"Depósito:\tR$ {valor:.2f}\n"
    print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, ""

def sacar(saldo, valor, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, "", numero_saques

    if valor > saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        return saldo, "", numero_saques

    if valor > limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        return saldo, "", numero_saques

    if numero_saques >= limite_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        return saldo, "", numero_saques

    saldo -= valor
    numero_saques += 1
    print("\n=== Saque realizado com sucesso! ===")
    return saldo, f"Saque:\t\tR$ {valor:.2f}\n", numero_saques

def exibir_extrato(saldo, extrato):
    header = "\n================ EXTRATO ================"
    footer = "\n=========================================="
    print(header)
    if extrato:
        print(extrato)
    else:
        print("Não foram realizadas movimentações.")
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print(footer)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_usuario = {"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco": endereco}
    usuarios.append(novo_usuario)
    print("=== Usuário criado com sucesso! ===")

def criar_conta(agencia, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)

    if not usuario:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return None

    numero_conta = len(contas) + 1
    nova_conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    contas.append(nova_conta)
    print("\n=== Conta criada com sucesso! ===")
    return nova_conta

def listar_contas(contas):
    print("=" * 100)
    for conta in contas:
        print(f"Agência:\t{conta['agencia']}\nC/C:\t\t{conta['numero_conta']}\nTitular:\t{conta['usuario']['nome']}\n")
    print("=" * 100)

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, nova_transacao = depositar(saldo, valor)
            extrato += nova_transacao
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, nova_transacao, numero_saques = sacar(saldo, valor, limite, numero_saques, LIMITE_SAQUES)
            extrato += nova_transacao
        elif opcao == "e":
            exibir_extrato(saldo, extrato)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            criar_conta(AGENCIA, usuarios, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("Saindo do sistema...")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
