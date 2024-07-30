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
    # ... (código existente para criar o calendário)

def create_next_month_calendar(year, month, dados):
    """Função para criar e exibir o calendário do mês seguinte."""
    # ... (código existente para criar o calendário do próximo mês)

def load_data():
    """Carrega dados do arquivo JSON."""
    # ... (código existente para carregar os dados do arquivo JSON)

def main():
    """Função principal que configura a interface e gerencia a lógica do aplicativo."""
    st.set_page_config(page_title="Calendário", layout="wide")   
    today = date.today()
    year = today.year
    month = today.month

    # Armazena os dados no estado da sessão
    if 'dados' not in st.session_state:
        st.session_state.dados = load_data()

    # Cria um espaço reservado para o calendário atual
    current_calendar_placeholder = st.empty()

    # Cria um espaço reservado para o calendário do próximo mês
    next_calendar_placeholder = st.empty()

    # Cria um espaço reservado para o sidebar
    sidebar_placeholder = st.sidebar.empty()

    # Atualiza os calendários a cada 2 segundos
    while True:
        with current_calendar_placeholder.container():
            st.session_state.dados = load_data()  # Recarrega os dados do arquivo JSON
            create_calendar(year, month, st.session_state.dados)  # Atualiza o calendário atual
        
        with next_calendar_placeholder.container():
            create_next_month_calendar(year, month, st.session_state.dados)  # Atualiza o calendário do próximo mês
        
        with sidebar_placeholder:
            selected_option = st.radio("Opções", ["Adicionar", "Editar", "Excluir"])
            
            if selected_option == "Adicionar":
                st.subheader("Adicionar Agenda")
                selected_date = st.date_input("Data", value=today)
                year, month = selected_date.year, selected_date.month
                
                cidades = ['Abaiara', 'Barro', 'B.Santo', 'Mauriti', 'Milagres', 'M.Velha', 'Penaforte', 'Porteitas', 'Jati', "ADICIONAR NOVA CIDADE"]
                cidade = st.selectbox("Cidade", cidades)
                
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
                    st.session_state.dados.append(new_item)
                    with open('agenda.json', 'w', encoding='utf-8') as file:
                        json.dump(st.session_state.dados, file, ensure_ascii=False, indent=4)
                    st.success("Item adicionado com sucesso!")
            
            elif selected_option == "Editar":
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
            
            else:
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
        
        time.sleep(2)  # Aguarda 2 segundos antes de atualizar novamente

if __name__ == "__main__":
    main()
