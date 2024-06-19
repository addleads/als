import streamlit as st
import json
import os
import re
from datetime import datetime, timedelta

# Credenciais de usuário para autenticação
CREDENTIALS = {
    "francisco": "francisco",
    "adm": "adm123",
    "wingriddy": "wingriddy"
}

def load_json(file_path):
    if not os.path.exists(file_path):
        st.error(f"Arquivo {file_path} não encontrado.")
        st.stop()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar: {str(e)}")
        st.stop()
    return json_data

def convert_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except ValueError:
        return None

def filter_json(json_data, city, cnae_codes, keyword, porte, data_range):
    filtered_data = []
    data_inicio, data_fim = data_range

    for item in json_data:
        if (not city or item.get('municipio') == city) and (not cnae_codes or any(prim.get('code') in cnae_codes for prim in item.get('atividade_principal', []))):
            if keyword.lower() in json.dumps(item).lower():
                if (not porte or item.get('porte') == porte):
                    data_abertura_str = item.get('abertura', '')
                    data_abertura = convert_date(data_abertura_str)
                    if data_abertura:
                        if data_inicio and data_fim:
                            if data_inicio <= data_abertura <= data_fim:
                                filtered_data.append(item)
                        else:
                            filtered_data.append(item)
    return filtered_data

def create_whatsapp_link(phone_number):
    return f"https://wa.me/55{phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')}"

def authenticate():
    st.sidebar.title("Add Leads")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Login"):
        if username in CREDENTIALS and password == CREDENTIALS[username]:
            st.sidebar.success(f"Login realizado com sucesso como {username.capitalize()}!")
            return True
        else:
            st.sidebar.error("Credenciais incorretas. Tente novamente.")
            return False
    return False

def main():

    # Autenticação no início da execução
    authenticated = False
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        authenticated = authenticate()
        st.session_state.authenticated = authenticated
    else:
        authenticated = True

    if not authenticated:
        return

    file_path = "cli.json"
    json_data = load_json(file_path)

    if not isinstance(json_data, list):
        st.error("O arquivo não está no formato correto. Por favor, verifique se é uma lista.")
        st.stop()

    # Ordenar a lista de empresas pela data de abertura, da mais recente para a mais antiga
    json_data_sorted = sorted(json_data, key=lambda x: datetime.strptime(x.get('abertura', ''), '%d/%m/%Y'), reverse=True)

    cities = [''] + sorted(list(set(item.get('municipio', '') for item in json_data_sorted)))
    
    cnaes_dict = {prim['code']: prim['text'] for item in json_data_sorted for prim in item.get('atividade_principal', [])}
    cnae_codes = [''] + sorted(list(cnaes_dict.keys()))

    portes = [''] + sorted(list(set(item.get('porte', '') for item in json_data_sorted)))

    city = st.sidebar.selectbox('Selecione a cidade', cities)
    selected_cnaes = st.sidebar.multiselect('Selecione o(s) CNAE(s)', cnae_codes, format_func=lambda x: cnaes_dict.get(x, ""))
    porte = st.sidebar.selectbox('Selecione o porte', portes)
    keyword = st.sidebar.text_input('Pesquisar por palavra-chave')

    # Inicialização do intervalo de datas com base nos dados filtrados
    data_range = st.session_state.data_range if "data_range" in st.session_state else (None, None)

    # Encontrar a data mínima e máxima dos dados não filtrados
    if json_data_sorted:
        min_date = datetime.strptime(json_data_sorted[-1]['abertura'], '%d/%m/%Y').date()
        max_date = datetime.strptime(json_data_sorted[0]['abertura'], '%d/%m/%Y').date()
    else:
        min_date = datetime.now().date()
        max_date = datetime.now().date()

    # Slider único para selecionar o intervalo de datas, atualizado conforme os filtros
    st.sidebar.subheader("Intervalo de Data de Abertura")
    selected_start_date, selected_end_date = st.sidebar.slider("Intervalo de Data", min_value=min_date, max_value=max_date, value=(min_date, max_date), format="DD/MM/YYYY", key="date_slider")
    
    # Botão para acionar o filtro com as seleções do usuário
    if st.sidebar.button("Filtrar"):
        # Atualizar o intervalo de datas selecionado
        data_range = (selected_start_date, selected_end_date)
        st.session_state.data_range = data_range
        
        # Filtrar dados com base nas seleções do usuário, incluindo o novo intervalo de datas
        filtered_data = filter_json(json_data_sorted, city, selected_cnaes, keyword, porte, data_range)

        # Exibir os dados filtrados diretamente após alterar o slider, sem precisar pressionar Filtrar
        if filtered_data:
            st.subheader("Empresas Filtradas")
            for item in filtered_data:
                # Encontrar números de telefone que contenham ") 8" ou ") 9"
                telephones = re.findall(r"\(\d+\) \d+-\d+", item.get('telefone', ''))
                telefone_html = ""
                for phone_number in telephones:
                    if ") 8" in phone_number or ") 9" in phone_number:
                        telefone_link = create_whatsapp_link(phone_number)
                        telefone_html += f"<a href='{telefone_link}'>{phone_number}</a><br>"
                    else:
                        telefone_html += f"{phone_number}<br>"
                
                card_content = "<div class='content'>" + \
                    f"<h3>{item.get('nome', '')}</h3></p>" + \
                    f"<h3>{item.get('fantasia', '')}</h3></p>" + \
                    f"<p><strong>CNPJ:</strong> {item.get('cnpj', '')}</p>" + \
                    f"<p><strong>Abertura:</strong> {item.get('abertura', '')}</p>" + \
                    f"<p><strong>E-mail:</strong> {item.get('email', '')}</p>" + \
                    f"<p><strong>Telefone:</strong> {telefone_html}</p>" + \
                    f"<p><strong>Atividade Principal:</strong> {item.get('atividade_principal', [{}])[0].get('text', '')}</p>" + \
                    f"<p><strong>Atividades Secundárias:</strong> {item.get('atividades_secundarias', [{}])[0].get('text', '')}</p>" + \
                    f"<p><strong>Município:</strong> {item.get('municipio', '')}</p>" + \
                    f"<p><strong>Bairro:</strong> {item.get('bairro', '')}</p>" + \
                    f"<p><strong>Rua:</strong> {item.get('logradouro', '')}</p>" + \
                    f"<p><strong>Número:</strong> {item.get('numero', '')}</p>" + \
                    f"<p><strong>Porte:</strong> {item.get('porte', '')}</p>" + \
                    "</div>"

                st.markdown(card_content, unsafe_allow_html=True)
                st.markdown('___________')
                
        else:
            st.subheader("Nenhum resultado encontrado com os filtros selecionados.")

if __name__ == "__main__":
    main()
