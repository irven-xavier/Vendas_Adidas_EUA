import pandas as pd  
import plotly.express as px  
import streamlit as st  
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(page_title="Vendas da Adidas - USA", layout="wide")

logo_image = 'Imagem1.png'

st.image(logo_image)
st.title('Vendas da Adidas - EUA', logo_image)
st.markdown("##")

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel('Adidas US Sales Datasets.xlsx', skiprows=4)
    return df

df = get_data_from_excel()

df.rename(columns={"Sales_Method": "Tipo"}, inplace=True)
df.rename(columns={"Invoice Date": "Date"}, inplace=True)

colunas_to_drop = [0]
df = df.drop(df.columns[colunas_to_drop], axis=1)

df["Nº Mês"] = df["Date"].apply(lambda x: (x.month))
df["Year"] = df["Date"].apply(lambda x: str(x.year))
df["Day"] = df["Date"].apply(lambda x: str(x.day))
df["Mês"] = df["Date"].map(lambda x: x.month_name()).to_list()

#st.sidebar.image(logo_image)
st.sidebar.header("**Filtros**")
retailer = st.sidebar.radio(
    "Selecione a Loja:",
    options=df["Retailer"].unique()
)
sales_method = st.sidebar.radio(
    "Selecione o tipo de venda:",
    options=df["Tipo"].unique()
)
ano = st.sidebar.radio(
    "Selecione o ano:",
    options=df["Year"].unique()
)

df = df.query(
    "Year == @ano & Retailer == @retailer & Tipo == @sales_method"
)

#st.dataframe(df, hide_index=True)

Vendas_Totais = int(df["Total Sales"].sum())
QTD = int(df["Units Sold"].sum())
Vendas_efetuadas = int(df["Product"].count())

def compact_number(number):
    if abs(number) >= 1e9:
        return f'{number / 1e9:.0f} B'
    elif abs(number) >= 1e6:
        return f'{number / 1e6:.0f} M'
    elif abs(number) >= 1e3:
        return f'{number / 1e3:.0f} K'
    else:
        return str(number)

col1, col2, col3 = st.columns(3)

Vendas_Totais_format = compact_number(Vendas_Totais)
qtd_format = compact_number(QTD)
Vendas_efetuadas_format = compact_number(Vendas_efetuadas)

estilo = style_metric_cards(
    background_color = "#FAFAFA",
    border_size_px = 1,
    border_color = "#CCC",
    border_radius_px = 5,
    border_left_color = "#000000",
    box_shadow = True)

with col1:
    st.metric(label="Vendas Totais:", value=f"US$ {Vendas_Totais_format}")
    #style_metric_cards(estilo)
            #border_left_color='#000000', border_color='#000000', box_shadow=True)

with col2:
    st.metric(label="Quantidade Vendida:", value=f"{qtd_format}")
    #style_metric_cards()
            #border_left_color='#000000', box_shadow=True)

with col3:
    st.metric(label="Vendas Efetuadas:", value=f"{Vendas_efetuadas_format}")
    #style_metric_cards()
            #border_left_color='#000000', box_shadow=True)

st.markdown("""---""")

vendas_produto = df.groupby(by=["Product"])[["Total Sales"]].sum().sort_values(by="Total Sales", ascending=False)

Margem = df.groupby(by=["Product"])[["Operating Margin"]].mean().sort_values(by="Operating Margin", ascending=False)
Margem["Operating Margin"] = Margem["Operating Margin"].apply(lambda x: "{:.2%}".format(x))


qtd_produto = df.groupby(by=["Product"])[["Units Sold"]].sum().sort_values(by="Units Sold", ascending=False)

#unique_countries = df['Month'].unique()
#sel_country = st.selectbox('**Selecione o mês**', unique_countries)
#fil_df = df[df.Month == sel_country]  # filter

st.header('Produtos')
#st.markdown("<h2 style='text-align: center; color: black;'>Produtos</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
st.markdown("""---""")
st.header('Faturamento')
col4, col5 = st.columns(2)

with col1:
    st.markdown("##### Receita")
    st.write(vendas_produto)

with col2:
    st.markdown("##### Unidades Vendidas")
    st.write(qtd_produto)

with col3:
    st.markdown("##### Margem Operacional (Média)")
    st.write(Margem)

fig_date = px.bar(df, x="Nº Mês", y="Total Sales")
fig_data1 = df.groupby(by=["Nº Mês", "Mês"])[["Total Sales"]].sum().sort_values(by="Nº Mês", ascending=False)

with col4:
    st.markdown("##### Por Mês")
    tab1, tab2 = st.tabs(["📈 Gráfico", "🗃 Tabela"])
    tab1.plotly_chart(fig_date, use_container_width=True)
    tab2.write(fig_data1)

city_total = df.groupby("Region")[["Total Sales"]].sum().reset_index()
fig_city = px.bar(city_total, x="Region", y="Total Sales")

with col5:
    st.markdown("##### Por Região")
    tab1, tab2 = st.tabs(["📈 Gráfico", "🗃 Tabela"])
    tab1.plotly_chart(fig_city, use_container_width=True)
    tab2.dataframe(city_total, hide_index=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)