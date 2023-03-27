import streamlit as st
import pandas as pd

# read data, 讀取資料

df=pd.read_csv("data/TWSE_TW-1.csv")
df.fillna('', inplace=True)

# set up Streamlit app, 建立應用程式
st.title("TWSE Stock Search, 台灣股票代號查詢")

# add search box and dropdown, 增加搜尋選擇欄位
search_term = st.text_input("Enter search term, 輸入查詢資料:")
search_by = st.selectbox("Search by column:", options=['Symbol 公司代碼', 'Name 公司名稱'])

# search for matching rows, 搜尋並列印結果
if search_term:
    if search_by == 'Symbol 公司代碼':
        result = df[df['Symbol'].str.contains(search_term)]
    elif search_by == 'Name 公司名稱':
        result = df[df['Name'].str.contains(search_term)]
    else:
        result = pd.DataFrame()
    st.write('Search ',search_term,' by ', search_by )   
    st.write(result)
    
import pandas as pd
import streamlit as st

import requests
import geoip2.database

# path to GeoLite2-Country.mmdb file
reader = geoip2.database.Reader('data/GeoLite2-Country.mmdb')

# translations
translations = {
    'en': {'title': 'Taiwan Stock Exchange - Search',
           'search_option': 'Search by',
           'symbol_option': 'Symbol',
           'name_option': 'Name',
           'search_term': 'Enter search term',
           'no_results': 'No results found',
           'language': 'Language',
           'search': 'Search'},
    'zh': {'title': '台灣證券交易所 - 搜尋',
           'search_option': '搜尋方式',
           'symbol_option': '代號',
           'name_option': '名稱',
           'search_term': '輸入搜尋關鍵字',
           'no_results': '查無結果',
           'language': '語言',
           'search': '搜尋'}
}

# read data
df1=pd.read_csv("data/TWSE_TW-1.csv")
df1.fillna('', inplace=True)
# set up state
state = st.session_state

# detect where client comes from
def is_client_from_taiwan(ip_address):
    try:
        response = reader.country(ip_address)
        if response.country.iso_code == 'TW':
            return True
    except:
        pass
    return False


def get_client_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        return ip
    except Exception as e:
        print(str(e))
        return None

def locate():
    ip_address = get_client_ip()
    if is_client_from_taiwan(ip_address):
       return 'zh'
    else:
       return 'en'   

state.lang=locate()

if 'lang' not in state:
    state.lang = 'en'
    state.search_by = translations[state.lang]['symbol_option']
    state.search_term = ''
else:    
    state.search_by = translations[state.lang]['symbol_option']
    state.search_term = ''

#st.write(state.lang,translations[state.lang]['search_option'])

# main page
st.sidebar.title(translations[state.lang]['language'])
if state.lang=='en':
    state.lang = st.sidebar.radio('', ['en', 'zh'])
else:
    state.lang = st.sidebar.radio('', ['en', 'zh'],index=1)

st.sidebar.title(translations[state.lang]['search_option'])
state.search_by = st.sidebar.radio('', [translations[state.lang]['symbol_option'],
                                        translations[state.lang]['name_option']])
state.search_term = st.sidebar.text_input(translations[state.lang]['search_term'], state.search_term)

# set up main page
st.title(translations[state.lang]['title'])
search_by = state.search_by
search_term = state.search_term

# search data
if st.button(translations[state.lang]['search']):
    if search_by == translations[state.lang]['symbol_option']:
        result = df1[df1['Symbol'].str.contains(search_term.upper())]
    elif search_by == translations[state.lang]['name_option']:
        result = df1[df1['Name'].str.contains(search_term, case=False)]
    else:
        result = df1

    # display search results
    if len(result) > 0:
        st.write(result)
    else:
        st.write(translations[state.lang]['no_results'])

st.session_state['state'] = state
