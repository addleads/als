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

    # Criar a tabela do calendário
    table = "<table style='width:100%; border-collapse: collapse;'>"
    table += "<tr>" + "".join(f"<th style='padding: 5px; text-align: center;'>{day}</th>" for day in days_of_week) + "</tr>"

    for week in cal:
        table += "<tr>"
        for day in week[1:]:  # Ignora o primeiro elemento (domingo)
            if day == 0:
                table += "<td style='height: 35mm; width: 100px; padding: 5px; text-align: center;'></td>"  # Célula vazia
            else:
                # Verificar se há informações para o dia atual
                info_dia = next((item for item in dados if item['dia'] == day and item['mes'] == month and item['ano'] == year), None)
                if info_dia:
                    table += (
                        "<td style='height: 35mm; width: 100px; padding: 5px; text-align: center; vertical-align: top;'>"
                        f"<div style='margin: 0; font-weight: bold; text-align: center;'>{day}</div>"
                        f"<div style='text-align: center;'>{unidecode(info_dia['cidade'])}</div>"
                        f"<div style='text-align: center;'>{unidecode(info_dia['cliente'])}</div>"
                        f"<div style='text-align: center;'>{unidecode(info_dia['servico'])}</div>"
                        "</td>"
                    )
                else:
                    table += (
                        "<td style='height: 35mm; width: 100px; padding: 5px; text-align: center; vertical-align: top;'>"
                        f"<div style='margin: 0;'>{day}</div>"
                        "</td>"
                    )
        table += "</tr>"

    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Calendário", layout="wide")
    
    with st.sidebar:
        selected_date = st.date_input("Adicionar agenda", value=date.today())
        year, month = selected_date.year, selected_date.month

        # Carregar dados do arquivo JSON
        with open('agenda.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)

        # Lista de cidades com uma opção para adicionar nova cidade
        cidades = ['Abaiara', 'Barro', 'Brejo Santo', 'Mauriti', 'Milagres', 'Missão Velha', 'Penaforte', 'Porteitas', 'Jati', "ADICIONAR NOVA CIDADE"]
        
        cidade = st.selectbox("Cidade", cidades)

        # Campo para adicionar nova cidade se a opção for selecionada
        if cidade == "ADICIONAR NOVA CIDADE":
            cidade = st.text_input("Digite o nome da nova cidade:", "")

        cliente = st.text_input("Cliente")
        servico = st.text_input("Serviço")

        if st.button("Adicionar"):
            new_item = {
                "dia": selected_date.day,
                "mes": month,
                "ano": year,
                "cidade": cidade,
                "cliente": cliente,
                "servico": servico
            }
            # Verificar se a mesma informação já existe na agenda
            existing_item = next((item for item in dados if item['dia'] == new_item['dia'] and item['mes'] == new_item['mes'] and item['ano'] == new_item['ano'] and item['cidade'] == cidade and item['cliente'] == cliente and item['servico'] == servico), None)
            if existing_item:
                st.error("Esta informação já existe na agenda.")
            else:
                # Adicionar nova informação à agenda
                dados.append(new_item)

                # Salvar os dados atualizados no arquivo JSON
                with open('agenda.json', 'w', encoding='utf-8') as file:
                    json.dump(dados, file, ensure_ascii=False, indent=4)
                st.success("Informação adicionada à agenda com sucesso!")

        delete_date = st.date_input("Excluir agenda", value=date.today(), key="delete_date")

        if st.button("Excluir"):
            # Excluir informação da agenda
            for item in dados:
                if item['dia'] == delete_date.day and item['mes'] == delete_date.month and item['ano'] == delete_date.year:
                    dados.remove(item)
                    # Salvar os dados atualizados no arquivo JSON
                    with open('agenda.json', 'w', encoding='utf-8') as file:
                        json.dump(dados, file, ensure_ascii=False, indent=4)
                    st.success("Item excluído com sucesso!")
                    break
            else:
                st.error("Nenhum item encontrado com a data informada.")

    create_calendar(year, month, dados)

if __name__ == "__main__":
    main()
