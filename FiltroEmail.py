import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import dns.resolver
import os
import logging

# Configurar logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Variável global para armazenar o DataFrame dos emails inválidos
df_invalidos = None

# Lista de nomes/dominios inválidos
nomes_invalidos_default = [
    'grupoab', 'sememail', 'naotem', 'yahoo.com.br', 'bol.com.br', 'ymail', 'terra.com.br',
    'gmail.com.br', 'hotmail.com.br', 'nt@gmail', 'nt@hotmail', 'nao@tem', 'naopossui',
    'uol.com.br', 'ig.com.br', 'naoinformado', 'padrao', 'nao', 'sem', 'gnail', 'naosei',
    'coim', 'lymail', 'me.com', 'montadoras', 'bool', 'yhaoo', 'lwmail', 'gamil'
]

# Variável para armazenar nomes/dominios inválidos customizados
nomes_invalidos = nomes_invalidos_default.copy()

# Função para selecionar arquivo
def selecionar_arquivo():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        logging.info(f"Arquivo selecionado: {filepath}")
        processar_arquivo(filepath)
    else:
        logging.info("Nenhum arquivo selecionado")

# Função para selecionar arquivo de parâmetros de exclusão
def selecionar_parametros():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        logging.info(f"Parâmetros de exclusão selecionados: {filepath}")
        carregar_parametros(filepath)
    else:
        logging.info("Nenhum arquivo de parâmetros selecionado")

# Função para carregar parâmetros de exclusão de um arquivo
def carregar_parametros(filepath):
    global nomes_invalidos
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            nomes_invalidos = [line.strip() for line in file if line.strip()]
        logging.info("Parâmetros de exclusão carregados com sucesso")
        messagebox.showinfo("Concluído", "Parâmetros de exclusão carregados com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao carregar parâmetros: {e}")
        messagebox.showerror("Erro", f"Erro ao carregar parâmetros: {e}")

# Função de validação de email
def validar_email(email):
    # Verificar estrutura básica do email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        return False
    
    # Verificar se o domínio é comum
    dominios_comuns = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']
    dominio = email.split('@')[1]
    if dominio not in dominios_comuns:
        return False

    # Verificar DNS para MX records
    try:
        dns.resolver.resolve(dominio, 'MX')
        return True
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.NXDOMAIN:
        return False
    except dns.exception.Timeout:
        return False
    except dns.resolver.NoNameservers:
        return False

# Função para verificar nomes inválidos
def verificar_nomes_invalidos(email):
    for nome in nomes_invalidos:
        if nome in email.lower():
            return False
    return True

# Função para processar o arquivo
def processar_arquivo(filepath):
    global df_invalidos
    encodings = ['utf-8', 'latin1']
    separators = [';', ',', '\t']

    for encoding in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(filepath, sep=sep, encoding=encoding)
                logging.info(f"Arquivo carregado com sucesso usando encoding '{encoding}' e separador '{sep}'")
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        else:
            continue
        break
    else:
        logging.error("Erro ao carregar o arquivo com os encodings e separadores tentados.")
        messagebox.showerror("Erro", "Erro ao carregar o arquivo. Verifique o formato do arquivo.")
        return
    
    # Verificar se a coluna 'Email' existe
    if 'Email' not in df.columns:
        logging.warning("A coluna 'Email' não foi encontrada na planilha.")
        messagebox.showwarning("Aviso", "A coluna 'Email' não foi encontrada na planilha.")
        return
    
    # Remover linhas com valores vazios na coluna 'Email'
    df.dropna(subset=['Email'], inplace=True)

    # Iniciar a barra de progresso
    progress_bar['maximum'] = len(df)
    progress_bar['value'] = 0

    # Aplicar a função de validação aos emails
    df['valido'] = df['Email'].apply(lambda x: validar_email(x) and verificar_nomes_invalidos(x))

    # Atualizar a barra de progresso
    for i, row in df.iterrows():
        progress_bar['value'] = i + 1
        root.update_idletasks()

    # Filtrar emails válidos e inválidos
    df_validos = df[df['valido'] == True].drop(columns=['valido'])
    df_invalidos = df[df['valido'] == False].drop(columns=['valido'])

    # Gerar o nome do arquivo de saída
    dir_name, base_name = os.path.split(filepath)
    file_name, file_ext = os.path.splitext(base_name)
    output_filepath = os.path.join(dir_name, f"{file_name}_Atualizado{file_ext}")

    # Salvar resultados em um novo CSV
    df_validos.to_csv(output_filepath, sep=';', index=False)
    logging.info(f"Resultados salvos em {output_filepath}")
    messagebox.showinfo("Concluído", f"Resultados salvos em {output_filepath}")

# Função para salvar emails inválidos
def salvar_invalidos():
    global df_invalidos
    if df_invalidos is not None:
        # Gerar o nome do arquivo de saída
        output_filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile='Retorno_Inválidos.csv')
        if output_filepath:
            df_invalidos.to_csv(output_filepath, sep=';', index=False)
            logging.info(f"Emails inválidos salvos em {output_filepath}")
            messagebox.showinfo("Concluído", f"Emails inválidos salvos em {output_filepath}")
    else:
        logging.warning("Nenhum dado de email inválido encontrado. Por favor, processe um arquivo primeiro.")
        messagebox.showwarning("Aviso", "Nenhum dado de email inválido encontrado. Por favor, processe um arquivo primeiro.")

# Criar interface gráfica
root = tk.Tk()
root.title("Validador de Emails")

# Configurar o tamanho da janela
root.geometry("400x350")

# Definir cor de fundo
root.configure(bg='#f0f0f0')

# Adicionar título ao topo
title_label = tk.Label(root, text="Validador de Emails", font=("Helvetica", 18, "bold"), bg='#f0f0f0')
title_label.pack(pady=20)

# Centralizar botões em um frame
frame = tk.Frame(root, bg='#f0f0f0')
frame.pack(expand=True)

btn_selecionar = tk.Button(frame, text="Selecionar Planilha CSV", command=selecionar_arquivo, font=("Helvetica", 12))
btn_selecionar.pack(pady=10)

btn_parametros = tk.Button(frame, text="Selecionar Parâmetros de Exclusão", command=selecionar_parametros, font=("Helvetica", 12))
btn_parametros.pack(pady=10)

btn_lista_retorno = tk.Button(frame, text="Lista de Retorno", command=salvar_invalidos, font=("Helvetica", 12))
btn_lista_retorno.pack(pady=10)

# Adicionar barra de progresso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

root.mainloop()
