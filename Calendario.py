import streamlit as st
import calendar
from datetime import datetime, date
import json
from unidecode import unidecode
import os

def create_calendar(year, month, dados):
    # Código para criar o calendário...
    pass

def main():
    st.set_page_config(page_title="Calendário", layout="wide")

    # Adicionar filtro de data na sidebar
    with st.sidebar:
        selected_date = st.date_input("Adicionar agenda", value=date.today())
        year, month, day = selected_date.year, selected_date.month, selected_date.day

        # Carregar dados do arquivo JSON
        if os.path.exists('agenda.json'):
            with open('agenda.json', 'r', encoding='utf-8') as file:
                dados = json.load(file)
        else:
            dados = []

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
                st.experimental_rerun()  # Recarregar a página

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
                    st.experimental_rerun()  # Recarregar a página
                    break
            else:
                st.error("Nenhum item encontrado com a data informada.")

    create_calendar(year, month, dados)

if __name__ == "__main__":
    main()
