import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Painel de Vendas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Painel Analítico de Vendas")

df = pd.read_csv("dados_atividade_13_vendas - dados_atividade_13_vendas.csv")

# Conversão segura da coluna Faturamento
# Se já estiver numérica, mantém como número.
# Se estiver como texto com R$, vírgula ou ponto, faz a conversão.
if df["Faturamento"].dtype == "object":
    df["Faturamento"] = (
        df["Faturamento"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

df["Faturamento"] = pd.to_numeric(df["Faturamento"], errors="coerce")

df = df.dropna(subset=["Faturamento"])

with st.sidebar:
    st.header("Filtros")

    lista_cidades = sorted(df["Cidade"].unique())

    cidades_selecionadas = st.multiselect(
        "Selecione as Filiais",
        lista_cidades,
        default=lista_cidades
    )

df_filtrado = df[df["Cidade"].isin(cidades_selecionadas)]

faturamento = df_filtrado["Faturamento"].sum()
quantidade_vendas = len(df_filtrado)
ticket_medio = faturamento / quantidade_vendas if quantidade_vendas > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Faturamento Total", f"R$ {faturamento:,.2f}")
col2.metric("Quantidade de Vendas", quantidade_vendas)
col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.divider()

faturamento_categoria = df_filtrado.groupby(
    "Categoria_Produto", as_index=False
)["Faturamento"].sum()

grafico = px.bar(
    faturamento_categoria,
    x="Categoria_Produto",
    y="Faturamento",
    title="Faturamento por Categoria de Produto",
    text="Faturamento"
)

grafico.update_traces(
    texttemplate="R$ %{text:,.2f}",
    textposition="outside"
)

grafico.update_layout(
    xaxis_title="Categoria do Produto",
    yaxis_title="Faturamento",
    uniformtext_minsize=8,
    uniformtext_mode="hide"
)

st.plotly_chart(grafico, use_container_width=True)

st.subheader("Base de dados filtrada")
st.dataframe(df_filtrado)