import getpass
from repositories import user_repository as repository

def user_operations(userdb, userfile, userdata):
    user_data = repository.get_user_after_login(userfile)
    
    while(True):
        print(f'''
\n
---------------------Menu Principal---------------------
--------------------------------------------------------

    Seja bem vindo(a) de volta {user_data['NOME']}
    
    Seu Saldo Total R$: {user_data['SALDO DA CARTEIRA R$']}
    Seu Saldo Disponivel R$: {user_data['SALDO DISPONIVEL R$']}

| [1] - Nova Receita
| [2] - Nova Despesa
| [3] - Minha Carteira
| [4] - Minhas Informações
| [5] - Voltar 

\n
        ''')
        
        user_options = input('Selecione a opção: ')
        if user_options.isdigit():
            if user_options == "1":
                add_new_revenue(userdb, userdata)
                break
            elif user_options == "2":
                add_new_expanse(userdb, userdata)
                break
            elif user_options == "3":
                my_wallet(userdb, userfile, userdata)
                break
            elif user_options == "4":
                show_infos(userdb, userfile, userdata)
                break
        else:
            print("\nPor favor, informe apenas números!\n")

def my_wallet(userdb, userfile, userdata):
    user_data = repository.get_user_after_login(userfile)

    while(True):
        print(f'''
\n

---------------------Minha Carteira---------------------
--------------------------------------------------------
               
    Saldo Total R$: {user_data['SALDO DA CARTEIRA R$']}
    Saldo Disponivel R$: {user_data['SALDO DISPONIVEL R$']}
              
| [1] - Atualizar Renda
| [2] - Voltar
              
\n

        ''')

        user_options = input('Selecione a opção: ')
        if user_options.isdigit():
            if user_options == "1":
                expense_value = input('\nInforme o valor dos Fundos R$: ')
                repository.add_value_user_wallet(userfile, expense_value)
                break
            elif user_options == "2":
                user_operations(userdb, userfile, userdata)
                break
            else:
                print("\nPor favor, informe apenas números!\n")

def show_infos(userdb, userfile, userdata):
    while(True):
        print('\n---------------Minhas Informações---------------\n')
        print('| [1] - Voltar\n')

        repository.show_user_infos(userdb, userfile, userdata)
        print('\n\n')

        user_options = input('Selecione a opção: ')
        if user_options.isdigit():
            if user_options == "1":
                user_operations(userdb, userfile, userdata)
                break
            else:
                print('\nOpção Inválida\n')
        else:
                print("\nPor favor, informe apenas números!\n")
            
def add_new_expanse(userdb, userdata):
    while(True):
        print('\n---------------Lançar Nova Movimentação de Despesa---------------\n')
    
        expense_name = input('Informe o nome da despesa: ')
        expense_value = input('Informe o valor da despesa R$: ')
        expense_validity = input('Data de vencimento(dia/mês/ano): ')
        expense_repeat = input('Deseja replicar para os outros mesês?(S/N): ')
        expense_quantity_repeat = 0
        expense_number = None
        
        if not expense_repeat.isdigit():
            if expense_repeat == "S":
                expense_month_repeat = input('Quantidade de mesês para replicar: ')
                if expense_month_repeat.isdigit():
                    expense_quantity_repeat = int(expense_month_repeat)
                else:
                    print('\nInforme apenas numeros!\n')         
        else:
            print('\nDigite apenas(S ou N)!\n')
            
        expense_notification = input('Deseja receber notificações desta despesa?(S/N): ')
        if not expense_notification.isdigit():
            if expense_notification == "S":
                expense_number = input('Informe o numero para notificar: ')
        else:
            print('\nDigite apenas(S ou N)!\n')
            
        expense_observations = input('Observações: ')
        
        repository.insert_new_expense(
            expense_name,
            expense_value, 
            expense_validity,
            expense_repeat,
            expense_quantity_repeat, 
            expense_number, 
            expense_notification,
            expense_observations,
            userdb,
            userdata
        )
        break

def add_new_revenue(userdb, userdata):
    while(True):
        print('\n---------------Lançar Nova Movimentação de Despesa---------------\n')
    
        revenue_name = input('Informe o nome da receita: ')
        revenue_value = input('Informe o valor da receita R$: ')
        revenue_validity = input('Data de recebimento(dia/mês/ano): ')
        revenue_repeat = input('Deseja replicar para os outros mesês?(S/N): ')
        revenue_quantity_repeat = 0
        revenue_number = None
        
        if not revenue_repeat.isdigit():
            if revenue_repeat == "S":
                revenue_month_repeat = input('Quantidade de mesês para replicar: ')
                if revenue_month_repeat.isdigit():
                    revenue_quantity_repeat = int(revenue_month_repeat)
                else:
                    print('\nInforme apenas numeros!\n')         
        else:
            print('\nDigite apenas(S ou N)!\n')
            
        revenue_notification = input('Deseja receber notificações desta despesa?(S/N): ')
        if not revenue_notification.isdigit():
            if revenue_notification == "S":
                revenue_number = input('Informe o numero para notificar: ')
        else:
            print('\nDigite apenas(S ou N)!\n')
            
        revenue_observations = input('Observações: ')
        
        repository.insert_new_revenue(
            revenue_name,
            revenue_value, 
            revenue_validity,
            revenue_repeat,
            revenue_quantity_repeat, 
            revenue_number, 
            revenue_notification,
            revenue_observations,
            userdb,
            userdata
        )
        break

        
def insert_new_user():
    print('\n---------------Adicionar Novo Usuário---------------\n')
    
    username = input('Informe seu nome: ')
    email = input('Escolha seu melhor email: ')
    password =  getpass.getpass("Digite uma senha: ")
    print('\n\n')
    
    repository.insert(username, email, password)
    
def user_login():
    print('\n---------------Acessar Minha Conta---------------\n')
    
    username = input('Informe seu nome: ')
    email = input('Seu email: ')
    password =  getpass.getpass("Sua senha: ")
    print('\n\n')
    
    repository.search_user_by_login(username, email, password)