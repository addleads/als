import streamlit as st
import calendar
from datetime import date
import json
from unidecode import unidecode

def create_calendar(year, month, dados):
    cal = calendar.monthcalendar(year, month)
    month_names = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    st.write("<h4 style='text-align: center;'>Agenda - {} de {}</h4>".format(month_names[month-1], year), unsafe_allow_html=True)
    days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]

    table = "<table style='width:100%; border-collapse: collapse;'>"
    table += "<tr>" + "".join(f"<th style='padding: 5px;'>{day}</th>" for day in days_of_week) + "</tr>"

    for week in cal:
        table += "<tr>" + "".join(
            f"<td style='height: 35mm; padding: 5px; position: relative;'>"
            f"{day if day != 0 else ''}</td>" for day in week
        ) + "</tr>"
    
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Calendário", layout="wide")
    
    with st.sidebar:
        selected_date = st.date_input("Adicionar agenda", value=date.today())
        year, month = selected_date.year, selected_date.month

        with open('agenda.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)

        cidade = st.selectbox("Cidade", ['Abaiara', 'Barro', 'Brejo Santo', 'Mauriti', 'Milagres', 'Missão Velha', 'Penaforte', 'Porteitas', 'Jati'])
        cliente = st.text_input("Cliente")
        servico = st.text_input("Serviço")

        if st.button("Adicionar"):
            new_item = {"dia": selected_date.day, "mes": month, "ano": year, "cidade": cidade, "cliente": cliente, "servico": servico}
            if new_item not in dados:
                dados.append(new_item)
                with open('agenda.json', 'w', encoding='utf-8') as file:
                    json.dump(dados, file, ensure_ascii=False, indent=4)
                st.success("Informação adicionada à agenda com sucesso!")
            else:
                st.error("Esta informação já existe na agenda.")

        delete_date = st.date_input("Excluir agenda", value=date.today(), key="delete_date")

        if st.button("Excluir"):
            for item in dados:
                if item['dia'] == delete_date.day and item['mes'] == delete_date.month and item['ano'] == delete_date.year:
                    dados.remove(item)
                    with open('agenda.json', 'w', encoding='utf-8') as file:
                        json.dump(dados, file, ensure_ascii=False, indent=4)
                    st.success("Item excluído com sucesso!")
                    break
            else:
                st.error("Nenhum item encontrado com a data informada.")

    create_calendar(year, month, dados)

if __name__ == "__main__":
    main()
