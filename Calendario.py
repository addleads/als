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

    # Dicionário de cores escuras para as cidades
    city_colors = {
        "Abaiara": "#4CAF50",  # Verde escuro
        "Barro": "#2196F3",    # Azul escuro
        "Brejo Santo": "#F44336",  # Vermelho escuro
        "Mauriti": "#FF5722",  # Laranja escuro
        "Milagres": "#FFC107",  # Amarelo escuro
        "Missão Velha": "#9C27B0",  # Roxo escuro
        "Penaforte": "#607D8B",  # Cinza escuro
        "Porteitas": "#3F51B5",  # Azul marinho
        "Jati": "#795548"        # Marrom escuro
    }

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
                info_dia = [item for item in dados if item['dia'] == day and item['mes'] == month and item['ano'] == year]
                if info_dia:
                    # Adicionar as informações em linhas separadas
                    cell_content = f"<div style='margin: 0; font-weight: bold; text-align: center;'>{day}</div>"
                    for entry in info_dia:
                        cidade = unidecode(entry['cidade'])
                        cliente = unidecode(entry['cliente'])
                        servico = unidecode(entry['servico'])
                        color = city_colors.get(cidade, "white")  # Cor padrão se a cidade não estiver no dicionário
                        cell_content += (
                            f"<div style='text-align: center; background-color: {color}; color: white; padding: 2px; border-radius: 4px;'>{cidade} - {cliente}</div>"
                            f"<div style='text-align: center;'>{servico}</div>"
                        )
                    table += (
                        f"<td style='height: 35mm; width: 100px; padding: 5px; text-align: center; vertical-align: top;'>"
                        f"{cell_content}"
                        "</td>"
                    )
                else:
                    table += (
                        "<td style='height: 35mm; width: 100px; padding: 5px; text-align: center; vertical-align: top;'>"
                        f"<div style='margin: 0;'>{day}</div>"
                        "<div style='text-align: center;'></div>"
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
        try:
            with open('agenda.json', 'r', encoding='utf-8') as file:
                dados = json.load(file)
        except FileNotFoundError:
            dados = []  # Inicializa dados como uma lista vazia se o arquivo não existir

        # Campo para o cliente
        cliente = st.text_input("Cliente")
        
        # Lista de cidades com uma opção para adicionar nova cidade
        cidades = ['Abaiara', 'Barro', 'Brejo Santo', 'Mauriti', 'Milagres', 'Missão Velha', 'Penaforte', 'Porteitas', 'Jati', "ADICIONAR NOVA CIDADE"]
        
        cidade = st.selectbox("Cidade", cidades)

        # Campo para adicionar nova cidade se a opção for selecionada
        if cidade == "ADICIONAR NOVA CIDADE":
            cidade = st.text_input("Digite o nome da nova cidade:", "")

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
            # Adicionar nova informação à agenda
            dados.append(new_item)

            # Salvar os dados atualizados no arquivo JSON
            with open('agenda.json', 'w', encoding='utf-8') as file:
                json.dump(dados, file, ensure_ascii=False, indent=4)
            st.success("Informação adicionada à agenda com sucesso!")

        # Seção para editar informações
        st.subheader("Editar Informações")
        edit_date = st.date_input("Selecionar data para editar", value=date.today())
        edit_year, edit_month = edit_date.year, edit_date.month

        # Coletar informações para a data selecionada
        edit_info = [item for item in dados if item['dia'] == edit_date.day and item['mes'] == edit_month and item['ano'] == edit_year]

        if edit_info:
            st.write(f"Inserções para {edit_date}:")
            for idx, entry in enumerate(edit_info):
                st.write(f"Entrada {idx + 1}:")
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
                    # Salvar os dados atualizados no arquivo JSON
                    with open('agenda.json', 'w', encoding='utf-8') as file:
                        json.dump(dados, file, ensure_ascii=False, indent=4)
                    st.success("Alterações salvas com sucesso!")

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
