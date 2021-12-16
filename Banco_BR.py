
# Função de validar codigo da conta
def valida_codigo():
    while True:
        try:
            entrada = valida_int(
                'Insira o código ou 0 para retornar ao menu: ')
            if entrada <= 0:
                raise
        except:
            print('Entrada inválida. Entre um valor inteiro maior que 0')
        else:
            return entrada


def valida_float(txt):
    while True:
        try:
            entrada = float(input(txt))
        except:
            print('Entrada inválida. Entre um valor de ponto flutuante')
        else:
            return entrada


def valida_int(txt):
    while True:
        try:
            entrada = int(input(txt))
            if entrada <= 0:
                raise
        except:
            print('Entrada inválida. Entre um valor inteiro')
        else:
            return entrada

# Função de incluir nome


def valida_nome():
    nome = input('Insira o nome: ')
    while len(nome.split()) < 2:
        print('Erro, nome inválido. É necessário ter pelo menos dois nomes')
        nome = input('Insira o nome: ')
    return nome


def busca_cod(cod, lista):
    for conta in lista:
        if conta[0] == cod:
            return True
    return False

# Função de Inclusão


def incluir_conta(cc):
    cod = valida_codigo()
    for conta in cc:
        if conta[0] == cod:
            print('Erro, código já existe na base.')
            return
    nome = valida_nome()
    saldo = valida_float('Insira o saldo da conta: ')
    if saldo < 0:
        print('Erro, saldo negativo')
        return
    print('Inserido com sucesso!')
    cc.append([cod, nome, saldo])
    cc.sort()


def alterar_saldo(lista):

    def muda_saldo(codigo, cc, oper):
        for linha in range(len(cc)):
            if cc[linha][0] == codigo:
                if oper == 1:
                    cc[linha][2] += novo_saldo
                else:
                    cc[linha][2] -= novo_saldo
                break

    cod = valida_codigo()

    # Busca pelo codigo na lista de contas
    if not busca_cod(cod, lista):
        print('Código não encontrado')
        return

    novo_saldo = valida_float(
        'Insira o valor a ser alterado na conta(negativo para débito, positivo para crédito): ')

    operacao = valida_int("1 para crédito, 2 para débito")
    while operacao not in [1, 2]:
        operacao = valida_int("1 para crédito, 2 para débito")

    muda_saldo(cod, lista, operacao)


def excluir(lista):

    cod = valida_codigo()

    for linha in range(len(lista)):
        if lista[linha][0] == cod:
            if lista[linha][2] == 0:
                lista.pop(linha)
                return True
            print('O saldo da conta é diferente de 0')
            return False
    print('A conta não foi encontrada.')
    return


def menu():
    print('''MENU
 1 - inclusão de conta
 2 - alteração de saldo
 3 - exclusão de conta
 4 - relatórios gerenciais
 5 - saída do programa''')
    while True:
        try:
            escolha = valida_int("Escolha uma opção do menu: ")
            if escolha < 1 or escolha > 5:
                raise
        except:
            print('Opção inválida')
        else:
            return escolha


def salvar(lista, arquivo):
    with open(arquivo, 'w+') as arq:
        for c in lista:
            for ind in range(len(c)):
                if ind < 2:  # não é o ultimo
                    arq.write(str(c[ind]) + ';')
                else:
                    arq.write(str(c[ind]) + '\n')


def relatorios(lista):

    def menurelatorio():
        print('''MENU
        1 - listar clientes com saldo negativo
        2 - listar os clientes que têm saldo acima de um determinado valor
        3 - listar todas as contas
        4 - Retornar ao menu''')
        opc = valida_int('Escolha uma opção do menu: ')
        while opc < 1 or opc > 4:
            print('Opção inválida. Selecione uma opção do menu')
            opc = valida_int('Escolha uma opção do menu: ')
        return opc

    opcao = menurelatorio()

    while opcao != 4:

        if opcao == 1:
            print('Clientes com saldo negativo: ')
            for conta in lista:
                if conta[2] < 0:
                    print('Nome:', conta[1], 'Saldo:', conta[2])
        elif opcao == 2:
            valor = valida_float('Insira o valor que deseja verificar')
            encontrado = False
            for conta in lista:
                if conta[2] > valor:
                    print('Cliente', conta[1], 'com R$', conta[2])
                    encontrado = True
            if not encontrado:
                print('Nenhum cliente possui saldo acima do valor solicitado')

        elif opcao == 3:
            for conta in lista:
                print(
                    f'Conta {conta[0]}, nome: {conta[1]}, saldo: R${conta[2]}')

        opcao = menurelatorio()

    print('Retornando ao menu')
    return

# Definir contas Correntes


def ler_arquivo(nome):
    with open(nome) as arq:
        linhas = []
        contas = arq.readlines()
        for contas_correntes in contas:
            linhas.append(contas_correntes.strip().split(';'))
        for i in range(len(linhas)):
            linhas[i][0] = int(linhas[i][0])
            linhas[i][2] = float(linhas[i][2])
    return linhas


def main():
    file = 'contas.txt'
    contas_correntes = ler_arquivo(file)
    opc = menu()

    while opc != 5:

        if opc == 1:  # inclusão de conta
            incluir_conta(contas_correntes)
            input('Pressione enter para continuar')

        elif opc == 2:  # alteração de saldo
            if contas_correntes:  # Se há contas correntes na lista
                alterar_saldo(contas_correntes)
            else:
                print('Não há contas na lista')
            input('Pressione enter para continuar')

        elif opc == 3:  # exclusão de conta
            if contas_correntes:
                resultado = excluir(contas_correntes)
                if resultado:
                    print('A conta foi excluida com sucesso!')
                elif not resultado:
                    print('Saldo diferente de zero')
            else:
                print('Não há contas na lista')
            input('Pressione enter para continuar')

        elif opc == 4:  # relatórios gerenciais
            relatorios(contas_correntes)
            input('Pressione enter para continuar')

        else:  # Caso nenhuma opção válida seja selecionada
            print('Opção inválida, retornando ao menu')
        opc = menu()

    print('Encerrando o programa')
    salvar(contas_correntes, file)


if __name__ == "__main__":
    main()
