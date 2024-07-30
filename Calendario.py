import streamlit as st  # Importa a biblioteca Streamlit para criar a interface web
import calendar  # Importa a biblioteca calendar para manipular calendários
from datetime import date  # Importa a classe date para trabalhar com datas
import json  # Importa a biblioteca json para manipulação de arquivos JSON
from unidecode import unidecode  # Importa a função unidecode para remover acentos de strings

def create_calendar(year, month, dados):
    """Função para criar e exibir um calendário para um mês específico."""
    # Obtém o calendário do mês especificado
    cal = calendar.monthcalendar(year, month)
    # Nomes dos meses em português
    month_names = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    # Exibe o título do calendário
    st.write("<h4 style='text-align: center;'>Agenda - {} de {}</h4>".format(month_names[month-1], year), unsafe_allow_html=True)
    
    # Nomes dos dias da semana em português
    days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    
    # Dicionário de cores para as cidades
    city_colors = {
        "Abaiara": "#690202",  
        "Barro": "#692402",    
        "Brejo Santo": "#694a02",  
        "Mauriti": "#696702",  
        "Milagres": "#406902",  
        "Missão Velha": "#026913",  
        "Penaforte": "#025b69",  
        "Porteitas": "#021f69",  
        "Jati": "#400269",       
        "ADICIONAR NOVA CIDADE": "#4B4B4B"  
    }
    
    # Cria a tabela do calendário
    table = "<table style='width:100%; border-collapse: collapse;'>"
    # Adiciona o cabeçalho com os dias da semana
    table += "<tr>" + "".join(f"<th style='padding: 5px; text-align: center;'>{day}</th>" for day in days_of_week) + "</tr>"
    
    # Preenche a tabela com os dias do mês
    for week in cal:
        table += "<tr>"
        for day in week[1:]:  # Ignora o primeiro elemento (domingo)
            if day == 0:
                # Célula vazia para dias que não pertencem ao mês
                table += "<td style='height: 35mm; width: 100px; padding: 5px; text-align: center;'></td>"
            else:
                # Verifica se há informações para o dia atual
                info_dia = [item for item in dados if item['dia'] == day and item['mes'] == month and item['ano'] == year]
                if info_dia:
                    # Adiciona o dia e as informações correspondentes
                    cell_content = f"<div style='margin: 0; font-weight: bold; text-align: left;'>{day}</div>"
                    for entry in info_dia:
                        cidade = unidecode(entry['cidade'])  # Remove acentos da cidade
                        cliente = unidecode(entry['cliente'])  # Remove acentos do cliente
                        servico = unidecode(entry['servico'])  # Remove acentos do serviço
                        color = city_colors.get(cidade, "#000000")  # Cor padrão se a cidade não estiver no dicionário
                        cell_content += (
                            f"<div style='text-align: left; background-color: {color}; color: white; padding: 2px; border-radius: 4px;'>{cidade} - {cliente}</div>"
                            f"<div style='text-align: left; background-color: {color}; color: white; padding: 2px; border-radius: 4px;'>{servico}</div>"
                        )
                    table += (
                        f"<td style='height: 100px; width: 100px; padding: 5px; text-align: left; vertical-align: top;'>"
                        f"{cell_content}"
                        "</td>"
                    )
                else:
                    # Célula para dias sem informações
                    table += (
                        "<td style='height: 100px; width: 100px; padding: 5px; text-align: left; vertical-align: top;'>"
                        f"<div style='margin: 0;'>{day}</div>"
                        "<div style='text-align: center;'></div>"
                        "</td>"
                    )
        table += "</tr>"
    table += "</table>"
    # Exibe a tabela do calendário na interface
    st.markdown(table, unsafe_allow_html=True)

def main():
    """Função principal que configura a interface e gerencia a lógica do aplicativo."""
    st.set_page_config(page_title="Calendário", layout="wide")   
    # Usa a data atual para definir o mês e o ano
    today = date.today()
    year = today.year
    month = today.month
    
    # Carrega dados do arquivo JSON
    try:
        with open('agenda.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)  # Carrega os dados existentes
    except FileNotFoundError:
        dados = []  # Inicializa dados como uma lista vazia se o arquivo não existir

    with st.sidebar:
        # Campo para selecionar uma data para adicionar uma nova agenda
        selected_date = st.date_input("Adicionar agenda", value=today)
        year, month = selected_date.year, selected_date.month
        
        # Lista de cidades com uma opção para adicionar nova cidade
        cidades = ['Abaiara', 'Barro', 'Brejo Santo', 'Mauriti', 'Milagres', 'Missão Velha', 'Penaforte', 'Porteitas', 'Jati', "ADICIONAR NOVA CIDADE"]
        cidade = st.selectbox("Cidade", cidades)
        
        # Campo para adicionar nova cidade se a opção for selecionada
        if cidade == "ADICIONAR NOVA CIDADE":
            cidade = st.text_input("Digite o nome da nova cidade:", "")
        
        # Campo para o cliente (agora abaixo da cidade)
        cliente = st.text_input("Cliente") 
        
        servico = st.text_input("Serviço")
        
        # Botão para adicionar uma nova entrada à agenda
        if st.button("Adicionar"):
            new_item = {
                "dia": selected_date.day,
                "mes": month,
                "ano": year,
                "cidade": cidade,
                "cliente": cliente,
                "servico": servico
            }
            # Adiciona nova informação à agenda
            dados.append(new_item)
            # Salva os dados atualizados no arquivo JSON
            with open('agenda.json', 'w', encoding='utf-8') as file:
                json.dump(dados, file, ensure_ascii=False, indent=4)
            st.success("Item adicionado com sucesso!")

        # Seção para editar informações
        st.subheader("Editar Informações")
        edit_date = st.date_input("Selecionar data para editar", value=date.today())
        edit_year, edit_month = edit_date.year, edit_date.month
        # Coleta informações para a data selecionada
        edit_info = [item for item in dados if item['dia'] == edit_date.day and item['mes'] == edit_month and item['ano'] == edit_year]
        if edit_info:
            st.write(f"Inserções para {edit_date}:")
            for idx, entry in enumerate(edit_info):
                st.write(f"Entrada {idx + 1}:")
                # Campos para editar as informações
                new_cidade = st.text_input("Cidade", value=entry['cidade'], key=f"cidade_{idx}")
                new_cliente = st.text_input("Cliente", value=entry['cliente'], key=f"cliente_{idx}")
                new_servico = st.text_input("Serviço", value=entry['servico'], key=f"servico_{idx}")
                if st.button(f"Salvar Alterações {idx + 1}", key=f"save_{idx}"):
                    # Atualiza a entrada correspondente
                    dados[dados.index(entry)] = {
                        "dia": entry['dia'],
                        "mes": entry['mes'],
                        "ano": entry['ano'],
                        "cidade": new_cidade,
                        "cliente": new_cliente,
                        "servico": new_servico
                    }
                    # Salva os dados atualizados no arquivo JSON
                    with open('agenda.json', 'w', encoding='utf-8') as file:
                        json.dump(dados, file, ensure_ascii=False, indent=4)
                    st.success("Alterações salvas com sucesso!")

        # Seção para excluir informações
        st.subheader("Excluir Informações")
        delete_date = st.date_input("Excluir agenda", value=date.today(), key="delete_date")
        if st.button("Excluir"):
            # Exclui informação da agenda
            for item in dados:
                if item['dia'] == delete_date.day and item['mes'] == delete_date.month and item['ano'] == delete_date.year:
                    dados.remove(item)  # Remove o item correspondente
                    # Salva os dados atualizados no arquivo JSON
                    with open('agenda.json', 'w', encoding='utf-8') as file:
                        json.dump(dados, file, ensure_ascii=False, indent=4)
                    st.success("Item excluído com sucesso!")
                    break
            else:
                st.error("Nenhum item encontrado com a data informada.")

    # Exibe o calendário do mês atual
    create_calendar(year, month, dados)

    # Calcula o próximo mês e ano
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # Exibe o calendário do próximo mês
    st.markdown("<hr>", unsafe_allow_html=True)  # Adiciona uma linha horizontal para separação
    create_calendar(next_year, next_month, dados)  # Chama a função para o próximo mês

if __name__ == "__main__":
    main()  # Executa a função principal ao rodar o script
