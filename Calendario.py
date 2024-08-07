import streamlit as st  # Importa a biblioteca Streamlit para criar a interface web
import calendar  # Importa a biblioteca calendar para manipular calendários
from datetime import date  # Importa a classe date para trabalhar com datas
import json  # Importa a biblioteca json para manipulação de arquivos JSON
from unidecode import unidecode  # Importa a função unidecode para remover acentos de strings
import time  # Importa a biblioteca time para trabalhar com tempo

# Dicionário para cores das cidades
city_colors = {
    "Abaiara": "#690202",  
    "Barro": "#692402",    
    "B.Santo": "#694a02",  
    "Mauriti": "#696702",  
    "Milagres": "#406902",  
    "M.Velha": "#026913",  
    "Penaforte": "#025b69",  
    "Porteitas": "#021f69",  
    "Jati": "#400269",       
    "ADICIONAR NOVA CIDADE": "#4B4B4B"  
}

def create_calendar(year, month, dados):
    """Função para criar e exibir um calendário para um mês específico, sem a coluna de domingo."""
    cal = calendar.monthcalendar(year, month)
    month_names = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    st.write("<h4 style='text-align: center;'>Agenda - {} de {}</h4>".format(month_names[month-1], year), unsafe_allow_html=True)
    days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    
    table = "<table style='width:100%; border-collapse: collapse;'>"
    table += "<tr>" + "".join(f"<th style='padding: 5px; text-align: center;'>{day}</th>" for day in days_of_week) + "</tr>"
    
    for week in cal:
        table += "<tr>"
        for day in week[0:6]:  # Itera sobre os primeiros 6 dias da semana (segunda a sábado)
            if day == 0:
                table += "<td style='height: 3cm; width: 3cm; padding: 5px; text-align: center;'></td>"
            else:
                info_dia = [item for item in dados if item['dia'] == day and item['mes'] == month and item['ano'] == year]
                if info_dia:
                    cell_content = f"<div style='margin: 0; font-weight: bold; text-align: left;'>{day}</div>"
                    for entry in info_dia:
                        cidade = unidecode(entry['cidade'])
                        cliente = unidecode(entry['cliente'])
                        servico = unidecode(entry['servico'])
                        color = city_colors.get(cidade, "#000000")
                        cell_content += (
                            f"<div style='text-align: left; background-color: {color}; color: white; padding: 2px; border-radius: 4px;'>{cidade} - {cliente}</div>"
                            f"<div style='text-align: left; background-color: {color}; color: white; padding: 2px; border-radius: 4px;'>{servico}</div>"
                        )
                    table += (
                        f"<td style='height: 3cm; width: 3cm; padding: 5px; text-align: left; vertical-align: top;'>"
                        f"{cell_content}"
                        "</td>"
                    )
                else:
                    table += (
                        "<td style='height: 3cm; width: 3cm; padding: 5px; text-align: left; vertical-align: top;'>"
                        f"<div style='margin: 0;'>{day}</div>"
                        "<div style='text-align: center;'></div>"
                        "</td>"
                    )
        table += "</tr>"
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

def create_next_month_calendar(year, month, dados):
    """Função para criar e exibir o calendário do mês seguinte."""
    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year += 1
    
    cal = calendar.monthcalendar(next_year, next_month)
    month_names = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    st.write("<h4 style='text-align: center;'>Agenda - {} de {}</h4>".format(month_names[next_month-1], next_year), unsafe_allow_html=True)
    days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    
    table = "<table style='width:100%; border-collapse: collapse;'>"
    table += "<tr>" + "".join(f"<th style='padding: 5px; text-align: center;'>{day}</th>" for day in days_of_week) + "</tr>"
    
    for week in cal:
        table += "<tr>"
        for day in week[0:6]:  # Itera sobre os primeiros 6 dias da semana (segunda a sábado)
            if day == 0:
                table += "<td style='height: 3cm; width: 3cm; padding: 5px; text-align: center;'></td>"
            else:
                info_dia = [item for item in dados if item['dia'] == day and item['mes'] == next_month and item['ano'] == next_year]
                if info_dia:
                    cell_content = f"<div style='margin: 0; font-weight: bold; text-align: left;'>{day}</div>"
                    for entry in info_dia:
                        cidade = unidecode(entry['cidade'])
                        cliente = unidecode(entry['cliente'])
                        servico = unidecode(entry['servico'])
                        color = city_colors.get(cidade, "#000000")
                        cell_content += (
                            f"<div style='text-align: left; background-color: {color}; color: white; padding: 2px; border-radius: 4px;'>{cidade} - {cliente}</div>"
                            f"<div style='text-align: left; background-color: {color}; color: white; padding: 2px; border-radius: 4px;'>{servico}</div>"
                        )
                    table += (
                        f"<td style='height: 3cm; width: 3cm; padding: 5px; text-align: left; vertical-align: top;'>"
                        f"{cell_content}"
                        "</td>"
                    )
                else:
                    table += (
                        "<td style='height: 3cm; width: 3cm; padding: 5px; text-align: left; vertical-align: top;'>"
                        f"<div style='margin: 0;'>{day}</div>"
                        "<div style='text-align: center;'></div>"
                        "</td>"
                    )
        table += "</tr>"
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

def load_data():
    """Carrega dados do arquivo JSON."""
    try:
        with open('agenda.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def main():
    """Função principal que configura a interface e gerencia a lógica do aplicativo."""
    st.set_page_config(page_title="Calendário", layout="wide")   
    today = date.today()
    year = today.year
    month = today.month

    # Armazena os dados no estado da sessão
    if 'dados' not in st.session_state:
        st.session_state.dados = load_data()

    with st.sidebar:
        selected_date = st.date_input("Adicionar agenda", value=today)
        year, month = selected_date.year, selected_date.month
        
        cidades = ['Abaiara', 'Barro', 'B.Santo', 'Mauriti', 'Milagres', 'M.Velha', 'Penaforte', 'Porteitas', 'Jati', "ADICIONAR NOVA CIDADE"]
        cidade = st.selectbox("Cidade", cidades)
        
        if cidade == "ADICIONAR NOVA CIDADE":
            cidade = st.text_input("Digite o nome da nova cidade:", "")
        
        cliente = st.text_input("Cliente") 
        servico = st.text_input("Serviço")
        
        # Adicionar nova entrada
        if st.button("Adicionar"):
            new_item = {
                "dia": selected_date.day,
                "mes": month,
                "ano": year,
                "cidade": cidade,
                "cliente": cliente,
                "servico": servico
            }
            st.session_state.dados.append(new_item)
            with open('agenda.json', 'w', encoding='utf-8') as file:
                json.dump(st.session_state.dados, file, ensure_ascii=False, indent=4)
            st.success("Item adicionado com sucesso!")

        st.subheader("Editar Informações")
        edit_date = st.date_input("Selecionar data para editar", value=date.today())
        edit_year, edit_month = edit_date.year, edit_date.month
        edit_info = [item for item in st.session_state.dados if item['dia'] == edit_date.day and item['mes'] == edit_month and item['ano'] == edit_year]
        if edit_info:
            st.write(f"Inserções para {edit_date}:")
            for idx, entry in enumerate(edit_info):
                st.write(f"Entrada {idx + 1}:")
                new_cidade = st.text_input("Cidade", value=entry['cidade'], key=f"cidade_{idx}")
                new_cliente = st.text_input("Cliente", value=entry['cliente'], key=f"cliente_{idx}")
                new_servico = st.text_input("Serviço", value=entry['servico'], key=f"servico_{idx}")
                if st.button(f"Salvar Alterações {idx + 1}", key=f"save_{idx}"):
                    st.session_state.dados[st.session_state.dados.index(entry)] = {
                        "dia": entry['dia'],
                        "mes": entry['mes'],
                        "ano": entry['ano'],
                        "cidade": new_cidade,
                        "cliente": new_cliente,
                        "servico": new_servico
                    }
                    with open('agenda.json', 'w', encoding='utf-8') as file:
                        json.dump(st.session_state.dados, file, ensure_ascii=False, indent=4)
                    st.success("Alterações salvas com sucesso!")

        st.subheader("Excluir Informações")
        delete_date = st.date_input("Excluir agenda", value=date.today(), key="delete_date")
        if st.button("Excluir"):
            for item in st.session_state.dados:
                if item['dia'] == delete_date.day and item['mes'] == delete_date.month and item['ano'] == delete_date.year:
                    st.session_state.dados.remove(item)
                    with open('agenda.json', 'w', encoding='utf-8') as file:
                        json.dump(st.session_state.dados, file, ensure_ascii=False, indent=4)
                    st.success("Item excluído com sucesso!")
                    break
            else:
                st.error("Nenhum item encontrado com a data informada.")

    # Cria um espaço reservado para o calendário atual
    current_calendar_placeholder = st.empty()

    # Cria um espaço reservado para o calendário do próximo mês
    next_calendar_placeholder = st.empty()

    # Atualiza os calendários a cada 2 segundos
    while True:
        with current_calendar_placeholder.container():
            st.session_state.dados = load_data()  # Recarrega os dados do arquivo JSON
            create_calendar(year, month, st.session_state.dados)  # Atualiza o calendário atual
        
        with next_calendar_placeholder.container():
            create_next_month_calendar(year, month, st.session_state.dados)  # Atualiza o calendário do próximo mês
        
        time.sleep(2)  # Aguarda 2 segundos antes de atualizar novamente

if __name__ == "__main__":
    main()
