
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Painel Ecossistêmico",
    page_icon="🌐",
    layout="wide"
)

dados = pd.DataFrame({
    "Cidade": ["RMBH", "Poços de Caldas", "Uberlândia"],
    "Conhecimento": [85, 70, 75],
    "Inovação": [80, 65, 60],
    "Negócios": [75, 55, 45],
    "Empreendedorismo": [70, 50, 40],
    "Governança": [65, 60, 35]
})

dimensoes = [
    "Conhecimento",
    "Inovação",
    "Negócios",
    "Empreendedorismo",
    "Governança"
]

dados["Score Geral"] = dados[dimensoes].mean(axis=1)

def classificar(score):
    if score < 20:
        return "Inicial"
    elif score < 40:
        return "Emergente"
    elif score < 60:
        return "Estruturado"
    elif score < 80:
        return "Integrado"
    else:
        return "Inteligente"

dados["Nível de Maturidade"] = dados["Score Geral"].apply(classificar)

st.sidebar.title("🌐 Painel Ecossistêmico")

cidade = st.sidebar.selectbox(
    "Selecione a cidade:",
    dados["Cidade"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dimensões avaliadas:**")
st.sidebar.markdown("""
- Conhecimento
- Inovação
- Negócios
- Empreendedorismo
- Governança
""")

st.title("Painel de Diagnóstico Ecossistêmico das Cidades")

st.markdown("""
Protótipo computacional de apoio à decisão para avaliação dos ecossistemas
direcionados à mobilidade inteligente.

Os dados utilizados nesta versão são simulados e possuem finalidade demonstrativa.
""")

linha = dados[dados["Cidade"] == cidade].iloc[0]

st.subheader(f"Diagnóstico: {cidade}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Score Geral", f"{linha['Score Geral']:.1f}")
col2.metric("Nível de Maturidade", linha["Nível de Maturidade"])
col3.metric("Maior Fragilidade", linha[dimensoes].idxmin())
col4.metric("Maior Potencial", linha[dimensoes].idxmax())

st.subheader("Interpretação automática")

st.write(
    f"""
    A cidade de **{cidade}** apresentou score geral de **{linha['Score Geral']:.1f}**,
    sendo classificada no nível **{linha['Nível de Maturidade']}** de maturidade ecossistêmica.
    A dimensão com maior desempenho foi **{linha[dimensoes].idxmax()}** e a principal
    fragilidade identificada foi **{linha[dimensoes].idxmin()}**.
    """
)

radar = pd.DataFrame({
    "Dimensão": dimensoes,
    "Score": [linha[d] for d in dimensoes]
})

fig_radar = px.line_polar(
    radar,
    r="Score",
    theta="Dimensão",
    line_close=True,
    title=f"Radar Ecossistêmico - {cidade}"
)

fig_radar.update_traces(fill="toself")

fig_radar.update_polars(
    radialaxis=dict(
        visible=True,
        range=[0, 100]
    )
)

st.plotly_chart(fig_radar, use_container_width=True)

st.subheader("Ranking de Maturidade Ecossistêmica")

ranking = dados.sort_values("Score Geral", ascending=False)

fig_ranking = px.bar(
    ranking,
    x="Cidade",
    y="Score Geral",
    text=ranking["Score Geral"].round(1),
    title="Comparação entre Cidades"
)

fig_ranking.update_layout(yaxis_range=[0, 100])

st.plotly_chart(fig_ranking, use_container_width=True)

st.subheader("Base de Diagnóstico")

st.dataframe(dados, use_container_width=True)

st.subheader("Recomendações Estratégicas")

fragilidade = linha[dimensoes].idxmin()

recomendacoes = {
    "Conhecimento": "Fortalecer a integração entre universidades, governo e empresas; ampliar o compartilhamento de dados e criar laboratórios urbanos.",
    "Inovação": "Estimular projetos colaborativos, testes-piloto, uso de IoT, inteligência artificial e integração tecnológica aplicada à mobilidade.",
    "Negócios": "Ampliar parcerias público-privadas, modelos de financiamento e estratégias de sustentabilidade econômica dos serviços.",
    "Empreendedorismo": "Incentivar incubadoras, startups, hubs de inovação e programas de aceleração voltados à mobilidade inteligente.",
    "Governança": "Melhorar a coordenação institucional, a continuidade política, a participação cidadã e a integração entre os atores."
}

st.info(recomendacoes[fragilidade])

st.subheader("Exportação dos dados")

csv = dados.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Baixar base simulada em CSV",
    data=csv,
    file_name="diagnostico_ecossistemico.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption(
    "Protótipo desenvolvido em Python com Streamlit, Pandas e Plotly. "
    "Dados simulados para fins demonstrativos e metodológicos."
)
