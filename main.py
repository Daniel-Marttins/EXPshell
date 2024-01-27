from tqdm import tqdm
import time
from controllers import user_controller as controller

def main_program():
    while(True):
        print('''
\n
------------------------ EXPshell ------------------------
----------------------------------------------------------

| [1] - Novo usuário
| [2] - Acessar
| [3] - Sair
            
\n
        ''')
        
        input_option = input('Selecione uma opção acima: ')
        if input_option.isdigit():
            if input_option == "1":
                controller.insert_new_user()
            elif input_option == "2":
                controller.user_login()
        else:
            print("Por favor, informe apenas números!")
            
# Defina o número total de iterações
interations = 10

# Use o tqdm para criar a barra de progresso
for i in tqdm(range(interations), desc="Inciando...", unit="it"):
    # Execute alguma tarefa
    time.sleep(0.1)  # Simulando algum trabalho
        
main_program()