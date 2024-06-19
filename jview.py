import streamlit as st
import json
import os
import re
from datetime import datetime

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

def filter_json(json_data, city, cnae_codes, keyword, situacao, porte, data_inicio, data_fim):
    filtered_data = []
    for item in json_data:
        if (not city or item.get('municipio') == city) and (not cnae_codes or any(prim.get('code') in cnae_codes for prim in item.get('atividade_principal', []))):
            if keyword.lower() in json.dumps(item).lower():
                if (not situacao or item.get('situacao') == situacao) and (not porte or item.get('porte') == porte):
                    data_abertura_str = item.get('abertura', '')
                    data_abertura = convert_date(data_abertura_str)
                    if data_abertura:
                        if data_inicio and data_fim:
                            data_inicio_conv = convert_date(data_inicio)
                            data_fim_conv = convert_date(data_fim)
                            if data_inicio_conv and data_fim_conv:
                                if data_inicio_conv <= data_abertura <= data_fim_conv:
                                    filtered_data.append(item)
                        else:
                            filtered_data.append(item)
    return filtered_data

def create_whatsapp_link(phone_number):
    return f"https://wa.me/55{phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')}"

def main():
    st.title('Empresas')

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

    situacoes = [''] + sorted(list(set(item.get('situacao', '') for item in json_data_sorted)))
    portes = [''] + sorted(list(set(item.get('porte', '') for item in json_data_sorted)))

    city = st.sidebar.selectbox('Selecione a cidade', cities)
    selected_cnaes = st.sidebar.multiselect('Selecione o(s) CNAE(s)', cnae_codes, format_func=lambda x: cnaes_dict.get(x, ""))
    situacao = st.sidebar.selectbox('Selecione a situação', situacoes)
    porte = st.sidebar.selectbox('Selecione o porte', portes)
    keyword = st.sidebar.text_input('Pesquisar por palavra-chave')

    data_inicio = st.sidebar.date_input("Data de Início", min_value=None, max_value=None, key='inicio')
    data_fim = st.sidebar.date_input("Data Final", min_value=None, max_value=None, key='fim')

    if st.sidebar.button('Filtrar'):
        try:
            filtered_data = filter_json(json_data_sorted, city, selected_cnaes, keyword, situacao, porte, data_inicio.strftime('%d/%m/%Y') if data_inicio else None, data_fim.strftime('%d/%m/%Y') if data_fim else None)
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
                    f"<p><strong>CNPJ:</strong> {item.get('cnpj', '')}</p>" + \
                    f"<p><strong>Nome:</strong> {item.get('nome', '')}</p>" + \
                    f"<p><strong>Fantasia:</strong> {item.get('fantasia', '')}</p>" + \
                    f"<p><strong>Abertura:</strong> {item.get('abertura', '')}</p>" + \
                    f"<p><strong>E-mail:</strong> {item.get('email', '')}</p>" + \
                    f"<p><strong>Telefone:</strong> {telefone_html}</p>" + \
                    f"<p><strong>Atividade Principal:</strong> {item.get('atividade_principal', [{}])[0].get('text', '')}</p>" + \
                    f"<p><strong>Atividades Secundárias:</strong> {item.get('atividades_secundarias', [{}])[0].get('text', '')}</p>" + \
                    f"<p><strong>Município:</strong> {item.get('municipio', '')}</p>" + \
                    f"<p><strong>Bairro:</strong> {item.get('bairro', '')}</p>" + \
                    f"<p><strong>Rua:</strong> {item.get('logradouro', '')}</p>" + \
                    f"<p><strong>Número:</strong> {item.get('numero', '')}</p>" + \
                    f"<p><strong>Situação:</strong> {item.get('situacao', '')}</p>" + \
                    f"<p><strong>Porte:</strong> {item.get('porte', '')}</p>" + \
                    "</div>"
                st.markdown(card_content, unsafe_allow_html=True)
                st.markdown('___________')
        except ValueError:
            st.error("Formato de data inválido. Utilize o formato dd/mm/aaaa para as datas.")

if __name__ == "__main__":
    main()