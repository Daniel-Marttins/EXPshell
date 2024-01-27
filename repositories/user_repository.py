from tqdm import tqdm
import time
from datetime import datetime
import os
import random
import string
import calendar
from controllers import user_controller as controller

#padrão de dados fixos
root_dir = os.getcwd()
database_dir = root_dir + '/db'
interations = 10
current_date = datetime.now().strftime("%d/%m/%Y")
current_year = datetime.now().year
current_time = datetime.now().strftime("%H:%M:%S")


def insert_new_expense(name, value, validity, repeat, quantity_repeat, number, notification, observations, userdb, userdata):
    expanse_db = userdb + '/expenses' + '/' + str(current_year)
    
    #convertendo data de vencimento da despesa
    date_object = datetime.strptime(validity, '%d/%m/%Y')
    
    #pegando numero e nome do mes
    month = date_object.month
    month_name = date_object.strftime("%B")
    
    #buscando a pasta relacionada ao mes de lançamento da despesa
    create_month_name = os.path.join(expanse_db, f"{month:02d}_{month_name}")
    
    #resgatar arquivo do usuário
    user_file_name = userdb + '/' + userdata['NOME'] + '.txt'
    
    user_data = {}
    expense_value = float(value)
    
    #Atualizar os dados do saldo disponivel do usuário para despesas
    with open(user_file_name, 'r') as arq:
        lines = arq.readlines()
        
        #carrega os dados do usuário e adiciona a lista de dados acima
        for line in (lines):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                user_data[key] = value
                
    user_wallet = float(user_data['SALDO DISPONIVEL R$'])
    
    
    #verificar se o usuário tem saldo para lançar uma nova despesa
    if user_wallet < expense_value:
        print(f"\nVocê não tem saldo suficiente para efetuar um lançamento de uma nova despesa, seu valor R$: {user_wallet}\n")
        return
    
    #verifica o ano no qua esta sendo realizado o lançamento da despesa para criar ou inserir dados nos meses do ano em questão
    if os.path.exists(expanse_db):
        #caso a despesa estiver marcada para se repetir ele gera varias copias da despesas para cada mes a partir do vencimento da mesma para os outros meses        
        if repeat == "S":
            for i in range(int(quantity_repeat)):
                interator_month_name = calendar.month_name[month+i]
                interator_month_number = os.path.join(expanse_db, f"{month+i:02d}_{interator_month_name}")
                
                existing_files = [file for file in os.listdir(interator_month_number) if file.endswith(".txt")]
                next_file_number = 0
                
                if not existing_files:
                    next_file_number = 0
                else:
                    # Encontrar o último número utilizado nos arquivos
                    last_numbers = [int(file.split('.')[0]) for file in existing_files]
                    next_file_number = max(last_numbers) + 1
                    
                # Criar o nome do próximo arquivo
                file_expense_name = f"{next_file_number:03d}.txt"

                # Caminho completo para o novo arquivo
                root_file_expense = os.path.join(interator_month_number, file_expense_name)
                
                for i in tqdm(range(interations), desc="Lançando nova despesa...", unit="it"):
                    time.sleep(0.1)
        
                with open(root_file_expense, 'a') as new_expense:
                    new_expense.write(f"----DESPESA {name} DE {current_date} : {current_time}------------------\n")
                    new_expense.write("------------------------------------------------------------------------\n")
                    new_expense.write("\n")
                    new_expense.write(f"NOME: {name}\n")
                    new_expense.write(f"VALOR R$: {expense_value}\n")
                    new_expense.write(f"VENCIMENTO: {validity}\n")
                    new_expense.write(f"PARA REPETIR: {repeat}\n")
                    new_expense.write(f"STATUS: PENDENTE\n")
                    new_expense.write(f"MESES A SE REPETIR: {quantity_repeat}\n")
                    new_expense.write(f"NOTIFICAR SOBRE: {notification}\n")
                    new_expense.write(f"OBSERVACOES: {observations}\n")
                    
                
                    
            print(f"\nNova despesa lançanda em {current_date} as {current_time}...\n")
        else:
            existing_files = [file for file in os.listdir(create_month_name) if file.endswith(".txt")]
            next_file_number = 0
                
            if not existing_files:
                next_file_number = 0
            else:
                # Encontrar o último número utilizado nos arquivos
                last_numbers = [int(file.split('.')[0]) for file in existing_files]
                next_file_number = max(last_numbers) + 1
                
            # Criar o nome do próximo arquivo
            file_expense_name = f"{next_file_number:03d}.txt"
            
            # Caminho completo para o novo arquivo
            root_file_expense = os.path.join(create_month_name, file_expense_name)
            
            for i in tqdm(range(interations), desc="Lançando nova despesa...", unit="it"):
                # Execute alguma tarefa
                time.sleep(0.1)
        
            with open(root_file_expense, 'a') as new_expense:
                new_expense.write(f"----DESPESA {name} DE {current_date} : {current_time}------------------\n")
                new_expense.write("------------------------------------------------------------------------\n")
                new_expense.write("\n")
                new_expense.write(f"NOME: {name}\n")
                new_expense.write(f"VALOR R$: {expense_value}\n")
                new_expense.write(f"VENCIMENTO: {validity}\n")
                new_expense.write(f"PARA REPETIR: {repeat}\n")
                new_expense.write(f"STATUS: PENDENTE\n")
                new_expense.write(f"MESES A SE REPETIR: {quantity_repeat}\n")
                new_expense.write(f"NOTIFICAR SOBRE: {notification}\n")
                new_expense.write(f"OBSERVACOES: {observations}\n")
                
            update_user_after_expense(user_file_name, name, expense_value, current_date, current_time)
            print(f"\nNova despesa lançanda em {current_date} as {current_time}...\n")
            controller.user_operations(userdb, user_file_name, userdata)
    else:
        os.makedirs(expanse_db) 

#Metodo para atualizar os dados do usuário depois do lançamento da despesa
def update_user_after_expense(userfilename, name, value, current_date, current_time):    
    
    user_data = {}
    expense_value = float(value)
       
    #Atualizar os dados do saldo disponivel do usuário para despesas
    with open(userfilename, 'r') as arq:
        lines = arq.readlines()
        
        #carrega os dados do usuário e adiciona a lista de dados acima
        for line in (lines):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                user_data[key] = value
        
    user_balance = float(user_data['SALDO DISPONIVEL R$']) - expense_value

    for i, line in enumerate(lines):
        if "SALDO DISPONIVEL R$:" in line:
            lines[i] = f"SALDO DISPONIVEL R$: {user_balance:.2f}\n"
             
    with open(userfilename, 'w') as f:
        f.writelines(lines)
            
    with open(userfilename, 'a') as f:
        f.writelines('\n')
        f.writelines(f"-- DESPESA >>> [{current_date}:{current_time}] - {name} <R$: {expense_value}>") 

def insert_new_revenue(name, value, validity, repeat, quantity_repeat, number, notification, observations, userdb, userdata):
    revenue_db = userdb + '/revenues' + '/' + str(current_year)
    
    #convertendo data de vencimento da despesa
    date_object = datetime.strptime(validity, '%d/%m/%Y')
    
    #pegando numero e nome do mes
    month = date_object.month
    month_name = date_object.strftime("%B")
    
    #buscando a pasta relacionada ao mes de lançamento da despesa
    create_month_name = os.path.join(revenue_db, f"{month:02d}_{month_name}")
    
    #resgatar arquivo do usuário
    user_file_name = userdb + '/' + userdata['NOME'] + '.txt'
    
    user_data = {}
    revenue_value = float(value)
    
    #Atualizar os dados do saldo disponivel do usuário para despesas
    with open(user_file_name, 'r') as arq:
        lines = arq.readlines()
        
        #carrega os dados do usuário e adiciona a lista de dados acima
        for line in (lines):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                user_data[key] = value
                
    user_wallet = float(user_data['SALDO DA CARTEIRA R$'])
    user_wallet_avaliable = float(user_data['SALDO DISPONIVEL R$'])
    
    
    #verificar se o usuário tem saldo para lançar uma nova despesa
    if user_wallet < (revenue_value + user_wallet_avaliable):
        print(f"\nSeu saldo da carteira é menor do que o seu disponivel atual tente atualizar seu saldo primeiro, seu valor R$: {user_wallet}\n")
        return
    
    #verifica o ano no qua esta sendo realizado o lançamento da despesa para criar ou inserir dados nos meses do ano em questão
    if os.path.exists(revenue_db):
        #caso a despesa estiver marcada para se repetir ele gera varias copias da despesas para cada mes a partir do vencimento da mesma para os outros meses        
        if repeat == "S":
            for i in range(int(quantity_repeat)):
                interator_month_name = calendar.month_name[month+i]
                interator_month_number = os.path.join(revenue_db, f"{month+i:02d}_{interator_month_name}")
                
                existing_files = [file for file in os.listdir(interator_month_number) if file.endswith(".txt")]
                next_file_number = 0
                
                if not existing_files:
                    next_file_number = 0
                else:
                    # Encontrar o último número utilizado nos arquivos
                    last_numbers = [int(file.split('.')[0]) for file in existing_files]
                    next_file_number = max(last_numbers) + 1
                    
                # Criar o nome do próximo arquivo
                file_revenue_name = f"{next_file_number:03d}.txt"

                # Caminho completo para o novo arquivo
                root_file_revenue = os.path.join(interator_month_number, file_revenue_name)
                
                for i in tqdm(range(interations), desc="Lançando nova receita...", unit="it"):
                    time.sleep(0.1)
        
                with open(root_file_revenue, 'a') as new_revenue:
                    new_revenue.write(f"----RECEITA {name} DE {current_date} : {current_time}------------------\n")
                    new_revenue.write("------------------------------------------------------------------------\n")
                    new_revenue.write("\n")
                    new_revenue.write(f"NOME: {name}\n")
                    new_revenue.write(f"VALOR R$: {revenue_value}\n")
                    new_revenue.write(f"VENCIMENTO: {validity}\n")
                    new_revenue.write(f"PARA REPETIR: {repeat}\n")
                    new_revenue.write(f"STATUS: PENDENTE\n")
                    new_revenue.write(f"MESES A SE REPETIR: {quantity_repeat}\n")
                    new_revenue.write(f"NOTIFICAR SOBRE: {notification}\n")
                    new_revenue.write(f"OBSERVACOES: {observations}\n")          
                    
            print(f"\nNova despesa lançanda em {current_date} as {current_time}...\n")
        else:
            existing_files = [file for file in os.listdir(create_month_name) if file.endswith(".txt")]
            next_file_number = 0
                
            if not existing_files:
                next_file_number = 0
            else:
                # Encontrar o último número utilizado nos arquivos
                last_numbers = [int(file.split('.')[0]) for file in existing_files]
                next_file_number = max(last_numbers) + 1
                
            # Criar o nome do próximo arquivo
            file_expense_name = f"{next_file_number:03d}.txt"
            
            # Caminho completo para o novo arquivo
            root_file_expense = os.path.join(create_month_name, file_expense_name)
            
            for i in tqdm(range(interations), desc="Lançando nova receita...", unit="it"):
                # Execute alguma tarefa
                time.sleep(0.1)
        
            with open(root_file_expense, 'a') as new_revenue:
                new_revenue.write(f"----DESPESA {name} DE {current_date} : {current_time}------------------\n")
                new_revenue.write("------------------------------------------------------------------------\n")
                new_revenue.write("\n")
                new_revenue.write(f"NOME: {name}\n")
                new_revenue.write(f"VALOR R$: {revenue_value}\n")
                new_revenue.write(f"VENCIMENTO: {validity}\n")
                new_revenue.write(f"PARA REPETIR: {repeat}\n")
                new_revenue.write(f"STATUS: PENDENTE\n")
                new_revenue.write(f"MESES A SE REPETIR: {quantity_repeat}\n")
                new_revenue.write(f"NOTIFICAR SOBRE: {notification}\n")
                new_revenue.write(f"OBSERVACOES: {observations}\n")
                
            update_user_after_revenue(user_file_name, name, revenue_value, current_date, current_time)
            print(f"\nNova despesa lançanda em {current_date} as {current_time}...\n")
            controller.user_operations(userdb, user_file_name, userdata)
    else:
        os.makedirs(revenue_db) 
        

#Metodo para atualizar os dados do usuário depois do lançamento da receita
def update_user_after_revenue(userfilename, name, value, current_date, current_time):    
    
    user_data = {}
    revenue_value = float(value)
       
    #Atualizar os dados do saldo disponivel do usuário para receitas
    with open(userfilename, 'r') as arq:
        lines = arq.readlines()
        
        #carrega os dados do usuário e adiciona a lista de dados acima
        for line in (lines):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                user_data[key] = value
        
    user_balance = float(user_data['SALDO DISPONIVEL R$']) + revenue_value

    for i, line in enumerate(lines):
        if "SALDO DISPONIVEL R$:" in line:
            lines[i] = f"SALDO DISPONIVEL R$: {user_balance:.2f}\n"
             
    with open(userfilename, 'w') as f:
        f.writelines(lines)
            
    with open(userfilename, 'a') as f:
        f.writelines('\n')
        f.writelines(f"++ RECEITA >>> [{current_date}:{current_time}] - {name} <R$: {revenue_value}>")
          

#metodo para inserir
def insert(username, email, password):
    #montando nome do banco com base no email do usuário
    new_user = database_dir + '/' + email
    
    #verificando se o usuário existe ou não
    if not os.path.exists(new_user):
        for i in tqdm(range(interations), desc="Criando usuário", unit="it"):
            # Execute alguma tarefa
            time.sleep(0.1) 
        
        #cria a pasta para o usuário    
        os.makedirs(new_user)
        
        #gera o nome dos arquivos e pastas necessarios para cada usuário
        file_name = new_user + '/' + username + '.txt'
        expenses_dir = new_user + '/expenses'
        expanses_year_dir = expenses_dir + '/' + str(current_year)
        revenues_dir = new_user + '/revenues'
        revenues_year_dir = revenues_dir + '/' + str(current_year)

        # Se o arquivo não existir, ele será criado
        with open(file_name, 'a') as arq:
            arq.write(f"NOME: {username}\n")
            arq.write(f"EMAIL: {email}\n")
            arq.write(f"SENHA: {password}\n")
            arq.write("-----------------------------\n")
            arq.write("SALDO DA CARTEIRA R$: 0.00\n")
            arq.write("SALDO DISPONIVEL R$: 0.00\n")
            arq.write("-----------------------------\n")
            arq.write("-----------------------------\n")
            arq.write(f"CADASTRADO EM: {current_date} AS {current_time} \n")
            arq.write("----------------------------------------------------------------\n")
            arq.write("------HISTORICO DE MOVIMENTACOES--------------------------------\n")
            arq.write("\n")
                     
            
        #criar pasta para as receitas e despesas
        os.makedirs(expenses_dir)
        os.makedirs(revenues_dir)
        
        #criar subpastas para o ano das despesas e receitas
        os.makedirs(expanses_year_dir)
        os.makedirs(revenues_year_dir)
        
        #criar subpastas para cada mês das receitas e despesas
        for month in range(1, 13):
            month_name = datetime(current_year, month, 1).strftime("%B")  # Obtém o nome do mês
            month_folder = os.path.join(expanses_year_dir, f"{month:02d}_{month_name}")
            os.makedirs(month_folder, exist_ok=True)
            
        for month in range(1, 13):
            month_name = datetime(current_year, month, 1).strftime("%B")  # Obtém o nome do mês
            month_folder = os.path.join(revenues_year_dir, f"{month:02d}_{month_name}")
            os.makedirs(month_folder, exist_ok=True)
        
        print(f"\nUsuário [{email}] criado com sucesso em {current_date} as {current_time}!\n")
    else:
        print(f"\nEste usuário [{email}] já existe, faça o login!")


def generate_random_string(length):
    randomcharacters = string.ascii_letters + string.digits  # letras maiúsculas, minúsculas e dígitos
    return ''.join(random.choice(randomcharacters) for _ in range(length))   


def get_user_after_login(userfile):
    user_data = {}
        
    with open(userfile, 'r') as arq:
        # Lê todas as linhas do arquivo do usuário
        lines = arq.readlines()
            
        #carrega os dados do usuário e adiciona a lista de dados acima
        for line in (lines):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                user_data[key] = value

    return user_data
 
    
#metodo para buscar e validar o login
def search_user_by_login(username, email, password):
    #montando caminho do banco com base no email do usuário
    user_db_name = database_dir + '/' + email
    
    #nome do arquivo de informações do usuário
    file_name = user_db_name + '/' + username + '.txt'

    #verifica se o usuário existe
    if os.path.exists(user_db_name) and os.path.isdir(user_db_name):
        #lista de informações do usuário
        user_data = {}
        
        with open(file_name, 'r') as arq:
            # Lê todas as linhas do arquivo do usuário
            lines = arq.readlines()
            
            #carrega os dados do usuário e adiciona a lista de dados acima
            for line in (lines):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    user_data[key] = value
                
            if username == user_data['NOME'] and password == user_data["SENHA"]:
                for i in tqdm(range(interations), desc="Entrando...", unit="it"):
                    time.sleep(0.1)

                controller.user_operations(user_db_name, file_name, user_data)
            else:
                print('\nUsuário ou senha estão incorretos, tente novamente!\n')
            
    else:
        print(f"\nO usuário '{email}' não existe, faça o cadastro ou tente outro login!\n")


def add_value_user_wallet(userfile, value):
    user_data = get_user_after_login(userfile)

    add_value_total = float(user_data['SALDO DA CARTEIRA R$']) + float(value)
    add_value_avaliable = float(user_data['SALDO DISPONIVEL R$']) + float(value)

    with open(userfile, 'r') as arq:
        lines = arq.readlines()

        for i, line in enumerate(lines):
            if "SALDO DA CARTEIRA R$:" in line:
                lines[i] = f"SALDO DA CARTEIRA R$: {add_value_total:.2f}\n"
            elif "SALDO DISPONIVEL R$:" in line:
                lines[i] = f"SALDO DISPONIVEL R$: {add_value_avaliable:.2f}\n"
                
        with open(userfile, 'w') as f:
            f.writelines(lines)
                
        with open(userfile, 'a') as f:
            f.writelines('\n')
            f.writelines(f"++ ATUALIZAR RENDA >>> [{current_date}:{current_time}] - <R$: {value}>") 

    for i in tqdm(range(interations), desc="Adicionando Fundos...", unit="it"):
            # Execute alguma tarefa
            time.sleep(0.1) 

    print(f'\nFundos adicionados com sucesso co valor de R$ {value}\n')
    controller.my_wallet(userfile)

def show_user_infos(userdb, userfile, userdata):
    user_data = get_user_after_login(userfile)

    for key, value in user_data.items():
        print(f'{key}: {value}')