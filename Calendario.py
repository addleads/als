import streamlit as st
import calendar
from datetime import datetime, date
import json
from unidecode import unidecode
import time

def create_calendar(year, month, dados):
    # Criar o calendário para o mês e ano selecionados
    cal = calendar.monthcalendar(year, month)

    # Criar o cabeçalho com os dias da semana
    month_names = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    st.write("<h4 style='text-align: center;'>Agenda ADD Soluções - {} de {}</h4>".format(month_names[month-1], year), unsafe_allow_html=True)
    days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]

    # Criar a tabela do calendário
    table = "<table style='width:100%; border-collapse: collapse;'>"
    table += "<colgroup>"
    table += "<col style='width: 150px;'>"
    table += "<col style='width: 150px;'>"
    table += "<col style='width: 150px;'>"
    table += "<col style='width: 150px;'>"
    table += "<col style='width: 150px;'>"
    table += "<col style='width: 150px;'>"
    table += "</colgroup>"
    table += "<tr>"
    for day in days_of_week:
        table += "<th style='padding: 5px;'>{}</th>".format(day)
    table += "</tr>"

    for week in cal:
        table += "<tr>"
        for day in week[:-1]:
            if day == 0:
                table += "<td style='height: 35mm; padding: 5px; position: relative;'></td>"
            else:
                # Verificar se há informações para o dia atual
                info_dia = next((item for item in dados if item['dia'] == day and item['mes'] == month and item['ano'] == year), None)
                if info_dia:
                    table += "<td style='height: 35mm; padding: 5px; position: relative;'><div style='position: absolute; top: 0; left: 5px;'>{} - {}</div><div style='margin-top: 5px;'>{}</div><div style='margin-top: 5px;'>{}</div></td>".format(day, unidecode(info_dia['cidade']), unidecode(info_dia['cliente']), unidecode(info_dia['servico']))
                else:
                    table += "<td style='height: 35mm; padding: 5px; position: relative;'><div style='position: absolute; top: 0; left: 5px;'>{}</div></td>".format(day)
        table += "</tr>"

    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Calendário", layout="wide")

    # Adicionar filtro de data na sidebar
    with st.sidebar:
        selected_date = st.date_input("Adicionar agenda", value=date.today())
        year, month, day = selected_date.year, selected_date.month, selected_date.day

        # Carregar dados do arquivo JSON
        with open('agenda.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)

        cidades = ['Abaiara', 'Barro', 'Brejo Santo', 'Mauriti', 'Milagres', 'Missão Velha', 'Penaforte', 'Porteitas', 'Jati']
        cidade = st.selectbox("Cidade", cidades, key="cidade_add")
        cliente = st.text_input("Cliente", key="cliente_add")
        servico = st.text_input("Serviço", key="servico_add")

        if st.button("Adicionar"):
            # Verificar se a mesma informação já existe na agenda
            existing_item = next((item for item in dados if item['dia'] == day and item['mes'] == month and item['ano'] == year and item['cidade'] == cidade and item['cliente'] == cliente and item['servico'] == servico), None)
            if existing_item:
                st.error("Esta informação já existe na agenda.")
            else:
                # Adicionar nova informação à agenda
                new_item = {
                    "dia": day,
                    "mes": month,
                    "ano": year,
                    "cidade": cidade,
                    "cliente": cliente,
                    "servico": servico
                }
                dados.append(new_item)

                # Salvar os dados atualizados no arquivo JSON
                with open('agenda.json', 'w', encoding='utf-8') as file:
                    json.dump(dados, file, ensure_ascii=False, indent=4)
                st.success("Informação adicionada à agenda com sucesso!")

    # Atualizar a página a cada 5 segundos
    while True:
        create_calendar(year, month, dados)
        time.sleep(5)
        st.experimental_rerun()

    # Seção de exclusão
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

    # Botão para exportar agenda.json
    if st.sidebar.button("Exportar"):
        st.download_button(
            label="Baixar agenda.json",
            data=json.dumps(dados, ensure_ascii=False, indent=4),
            file_name="agenda.json",
            mime="application/json",
        )
        st.success("Agenda exportada com sucesso!")

if __name__ == "__main__":
    main()
