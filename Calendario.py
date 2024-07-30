import streamlit as st
import calendar
from datetime import date
import json
from unidecode import unidecode
import time

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
    days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    
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
        for idx, day in enumerate(week):
            if idx == 0:  # Ignora o primeiro elemento (domingo)
                continue
            if day == 0:
                # Célula vazia para dias que não pertencem ao mês
                table += "<td style='height: 60px; width: 60px; padding: 5px; text-align: center;'></td>"  # Altura e largura padronizadas
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
                        f"<td style='height: 60px; width: 60px; padding: 5px; text-align: left; vertical-align: top;'>"
                        f"{cell_content}"
                        "</td>"
                    )
                else:
                    # Célula para dias sem informações
                    table += (
                        "<td style='height: 60px; width: 60px; padding: 5px; text-align: left; vertical-align: top;'>"
                        f"<div style='margin: 0;'>{day}</div>"
                        "<div style='text-align: center;'></div>"
                        "</td>"
                    )
        table += "</tr>"
    table += "</table>"
    # Exibe a tabela do calendário na interface
    st.markdown(table, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Calendário", layout="wide")   
    today = date.today()
    year = today.year
    month = today.month
    
    try:
        with open('agenda.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)
    except FileNotFoundError:
        dados = []
    
    while True:
        # Exibe o calendário do mês atual
        st.write(f"Mês atual: {month}")
        create_calendar(year, month, dados)

        # Calcula o próximo mês e ano
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        # Exibe o calendário do próximo mês
        st.markdown("<hr>", unsafe_allow_html=True)
        st.write(f"Próximo mês: {next_month}")
        create_calendar(next_year, next_month, dados)

        # Aguarda 1 segundo antes de atualizar
        st.write("Aguardando 1 segundo antes da próxima atualização...")
        time.sleep(1)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
