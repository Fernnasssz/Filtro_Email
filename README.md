# Validador de Emails

## Descrição
Este projeto consiste em uma aplicação de validação de emails desenvolvida em Python com interface gráfica usando Tkinter. A aplicação permite carregar um arquivo CSV contendo uma lista de emails, validar cada um deles com base em critérios específicos (estrutura do email, domínios comuns e registros MX DNS) e filtrar os emails inválidos.

## Funcionalidades
- **Selecionar Planilha CSV:** Permite ao usuário selecionar um arquivo CSV para processamento.
- **Selecionar Parâmetros de Exclusão:** Permite importar parâmetros de exclusão adicionais para filtragem de emails inválidos.
- **Lista de Retorno:** Salva em um novo arquivo CSV os emails que foram considerados inválidos após o processamento.
- **Barra de Progresso:** Mostra o progresso do processamento dos emails na interface gráfica.

## Metodologia
O projeto utiliza uma abordagem de interface gráfica para facilitar a interação do usuário com a aplicação. A validação de emails é realizada com base em regex para a estrutura básica do email, verificação de domínios comuns e consulta aos registros MX DNS dos domínios. A aplicação utiliza as bibliotecas pandas para manipulação de dados CSV e tkinter para construção da interface gráfica.

## Regras de Negócio
- **Validação de Estrutura de Email:** Utiliza expressões regulares para validar a estrutura básica do email.
- **Verificação de Domínios Comuns:** Verifica se o domínio do email pertence a uma lista predefinida de domínios comuns.
- **Consulta a Registros MX DNS:** Realiza consulta aos registros MX DNS para verificar a existência de servidores de email válidos para o domínio.

## Tecnologias Utilizadas
- Python
- Tkinter (para GUI)
- pandas (para manipulação de dados)
- dns.resolver (para consulta DNS)

## Como Usar
1. Clone o repositório:

    git clone https://github.com/seu-usuario/nome-do-repositorio.git

2. Instale as dependências necessárias:

    pip install -r requirements.txt

3. Execute o arquivo principal da aplicação:

    python FiltroEmail.py

4. Selecione um arquivo CSV para processar e utilize as funcionalidades disponíveis na interface gráfica.

## Contribuições
Contribuições são bem-vindas! Para sugestões, melhorias ou correções, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Todos os direiros reservados - Desenvolvedor: Daniel Fernandes


