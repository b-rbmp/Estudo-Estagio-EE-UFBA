# -*- coding: utf-8 -*-

""" Estudo Estágio Engenharia Elétrica - UFBA

Um estudo realizado para analisar os anuncios de estágio recebidos entre os semestres 2016.1 e 2021.1 
através do Centro de Atendimento à Graduação - CEAG Politecnica e Colegiado de Engenharia Elétrica com 
vagas para Engenharia Elétrica/Eletrônica
Foram considerados apenas os estágios na região próxima de Salvador e desconsiderando vagas para Marketing/Comercial
Periodo Considerado: Data limite para enviar curriculo. Se indisponível, data que a vaga foi postada pela primeira vez
Para requisito e maximo semestre, as vezes é utilizado o periodo pedido em relação a
previsão de formatura. Ex: Disponibilidade para estagiar pelo menos 1 ano: Maximo_semestre = 10 - 2 = 8
Informações conforme informado na divulgação das empresas pelos
Centro de Atendimento à Graduação - CEAG Politecnica e Colegiado de Engenharia Elétrica
Vagas em desenvolvimento de Software são ignoradas (consideradas como Eng Computação/Ciencia
da Computação) a menos que vinculo claro com alguma área de Eng Elétrica/Eletrônica/Hardware
Para grandes empresas, foi feito uma pesquisa no linkedin OU google para observar se as empresas
ofereciam vagas de estágio em áreas relacionadas a engenharia elétrica. (quando não informavam nos sites
de inscrição ou nos flyers) """

from typing import Dict
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS

# Define a configuração do streamlit
st.set_page_config(page_title="Estudo Estágio",
                   page_icon=":clipboard:",
                   layout="centered",
                   initial_sidebar_state="auto")


# Função que adiciona um arquivo .css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Esconde menu e footer
hide_menu_footer = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_menu_footer, unsafe_allow_html=True) 

# Função cacheada que carrega os dados
@st.cache(persist=True)
def load_data():
    data = pd.read_json('estagio_data.json', encoding='UTF-8', dtype='object')
    return data

dados_df = load_data()

# Desativa o modebar
config_plotly = {'displayModeBar': False, 'staticPlot': True}

# SIDEBAR
st.sidebar.title('Índice do Estudo:')
st.sidebar.write('')
st.sidebar.markdown(
    '<a class="toc-header" href="#1-per-odo-vs-quantidade-de-anuncios">1. Período vs Quantidade de anuncios</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<a class="toc-header" href="#2-ofertas-de-est-gio-por-rea-sub-rea">2. Ofertas de estágio por Área/Subárea</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<span>&nbsp;&nbsp;</span><a class="toc-sub-header" href="#2-1-divis-o-de-ofertas-por-rea">2.1. Divisão de ofertas por área</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<span>&nbsp;&nbsp;</span><a class="toc-sub-header" href="#2-2-divis-o-por-sub-rea">2.2. Divisão por Subárea</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<a class="toc-header" href="#3-requisitos-de-semestraliza-o">3. Requisitos de Semestralização</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<span>&nbsp;&nbsp;</span><a class="toc-sub-header" href="#3-1-semestraliza-o-m-nima">3.1. Semestralização Mínima</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<span>&nbsp;&nbsp;</span><a class="toc-sub-header" href="#3-2-semestraliza-o-m-xima">3.2. Semestralização Máxima</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<a class="toc-header" href="#4-pr-requisitos-e-diferenciais">4. Pré-requisitos e diferenciais</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<span>&nbsp;&nbsp;</span><a class="toc-sub-header" href="#4-1-pr-requisitos-mais-comuns">4.1. Pré-requisitos mais comuns</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<span>&nbsp;&nbsp;</span><a class="toc-sub-header" href="#4-2-exist-ncia-de-pr-requisitos">4.2. Existência de Pré-requisitos</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<span>&nbsp;&nbsp;</span><a class="toc-sub-header" href="#4-3-pr-requisitos-filtrados-por-rea-de-atua-o">4.3. Pré-requisitos filtrados por área de atuação</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<span>&nbsp;&nbsp;</span><a class="toc-sub-header" href="#4-4-diferenciais-mais-comuns">4.4. Diferenciais mais comuns</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<a class="toc-header" href="#5-carga-hor-ria-semanal">5. Carga Horária Semanal</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<a class="toc-header" href="#6-ofertas-por-empresa">6. Ofertas por Empresa</a>',
    unsafe_allow_html=True)
st.sidebar.markdown(
    '<a class="toc-header" href="#7-navega-o-pelos-dados">7. Navegação pelos dados</a>',
    unsafe_allow_html=True)

# Conteúdo Principal
st.title('Estudo Anuncios de Estágio EE - UFBA')
st.markdown("""---""")
st.write(
    'Um estudo realizado para analisar os anuncios de estágio recebidos entre os semestres 2016.1 e 2021.1 através do Centro de Atendimento à Graduação - CEAG Politecnica e Colegiado de Engenharia Elétrica com vagas para Engenharia Elétrica/Eletrônica'
)
st.write(
    'Foram apenas considerados estágios para a região próxima de Salvador (Camaçari, Feira de Santana, Simões Filho, dentre outros)'
)
st.write(
    'As informações utilizadas são aquelas tiradas dos anuncios/flyers/sites de processo seletivo, sendo que para grandes empresas foi feito uma pesquisa no linkedin OU google para observar se as empresas ofereciam vagas de estágio em áreas relacionadas a engenharia elétrica'
)
st.write(
    'Considerou-se também o período (semestre) com a data limite para envio do currículo/inscrição no Processo Seletivo, e para os requisito ou máximo semestre matriculado, as vezes é utilizado o periodo pedido em relação a previsão de formatura'
)
st.markdown('Link para o repositório GitHub: [Clique Aqui](https://github.com/b-rbmp/Estudo-Estagio-EE-UFBA "Repositório GitHub")')

st.header('1. Período vs Quantidade de anuncios')
st.write(
    'Observando a quantidade de anuncios de estágio em cada semestre, verificou-se um aumento progressivo com os anos, interrompido durante o período de adaptação para o COVID-19 (2020.1 e 2020.2)'
)

# Conta quantos anuncios por semestre
ofertas_por_semestre = dados_df['periodo'].value_counts()

# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_ofertas_semestre = go.Figure(
    data=[go.Bar(x=ofertas_por_semestre.index, y=ofertas_por_semestre)])
fig_ofertas_semestre.update_traces(text=ofertas_por_semestre,
                                   textposition="outside",
                                   hovertemplate='N° de anuncios: %{y}' +
                                   '<br>Semestre: %{x}<br><extra></extra>')
fig_ofertas_semestre.update_xaxes(type='category',
                                  categoryorder='category ascending')
fig_ofertas_semestre.update_layout(margin=dict(l=20, r=20, b=20, t=20, pad=5),
                                   height=400,
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_ofertas_semestre,
                use_container_width=True,
                **{'config': config_plotly})

st.header('2. Ofertas de estágio por Área/Subárea')

st.subheader('2.1. Divisão de ofertas por área')
st.write(
    'Observa-se uma predominância de ofertas de estágio sem especificação da vaga (Geral), com quase metade dos anuncios nesta categoria. Não é uma surpresa, pois a maioria das grandes empresas abrem um processo seletivo genérico, abrindo para todas engenharias e outros cursos'
)
st.write(
    'Por outro lado, das empresas que selecionam estagiários para vagas específicas, a área de potência é a mais requisitada, com mais de 1/4 dos anuncios para esta área, seguido de controle, eletrônica e computação'
)

# Conta o número de ofertas por área
ofertas_por_area = dados_df['area'].value_counts()

# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_ofertas_por_area = go.Figure(data=[
    go.Pie(labels=ofertas_por_area.index,
           values=ofertas_por_area,
           textinfo='label+percent',
           insidetextorientation='radial')
])
fig_ofertas_por_area.update_traces(hovertemplate='Área: %{label}' +
                                   '<br>Contagem: %{value}' +
                                   '<br>%{percent}<extra></extra>',
                                   textposition='outside')
fig_ofertas_por_area.update_layout(margin=dict(l=20, r=20, b=20, t=20, pad=0),
                                   height=400,
                                   paper_bgcolor='rgba(0,0,0,0)',
                                   plot_bgcolor='rgba(0,0,0,0)',
                                   uniformtext_minsize=12,
                                   uniformtext_mode='hide',
                                   showlegend=False)
st.plotly_chart(fig_ofertas_por_area,
                use_container_width=True,
                **{'config': config_plotly})

st.subheader('2.2. Divisão por Subárea')
st.write(
    'Observa-se também a divisão dos anuncios de estágio por Subárea dentro de cada área, como visto a seguir:'
)

# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_subarea = px.sunburst(dados_df, path=["area", "subarea"])
fig_subarea.update_traces(hovertemplate='Área/Subárea: %{id}' +
                          '<br>Contagem: %{value}',
                          leaf=dict(opacity=0.92))
fig_subarea.update_layout(margin=dict(l=20, r=20, b=20, t=20, pad=0),
                          height=400,
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_subarea,
                use_container_width=True,
                **{'config': config_plotly})

st.header('3. Requisitos de Semestralização')
st.write(
    'Nesta seção, foram considerados equivalentes os requisitos de previsão de formatura e semestralização. Quando informado a previsão de formatura desejada pela empresa, este foi convertido em semestralização considerando o semestre em que o anuncio foi feito'
)
st.write(
    'Semestre 0 significa que não há requisito mínimo de semestre e semestre 10 significa que não há limite de semestralização máximo. Lembrando que são considerados os dados informados pelas empresas, desconsiderando as limitações semestrais impostas pela UFBA'
)

# Manipulação de dados contando o numero de anuncios por semestre e preenchendo os semestres sem anuncios com zeros
index_semestres = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
requisito_semestre = dados_df['requisito_semestre'].value_counts(
    normalize=True).reindex(index_semestres, fill_value=0)
maximo_semestre = dados_df['maximo_semestre'].value_counts(
    normalize=True).reindex(index_semestres, fill_value=0)

st.subheader('3.1. Semestralização Mínima')
st.write(
    'Em relação a semestralização mínima, pouco mais de 1/3 das ofertas de estágio não demandam um semestre mínimo, permitindo a inscrição de estudantes em início do curso'
)
st.write(
    'Por outro lado, observou-se que 1/4 das empresas requerem semestralização minima do quinto semestre e outros 1/4 no sexto semestre, excluindo dos processos seletivos os estudantes matriculados nos semestres iniciais'
)

# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_requisito_semestre = go.Figure()
fig_requisito_semestre.add_trace(
    go.Bar(
        x=index_semestres,
        y=requisito_semestre,
        name='Requisito Semestre',
    ))
fig_requisito_semestre.update_traces(
    text=requisito_semestre,
    texttemplate='%{text:.3p}',
    textposition="outside",
    hovertemplate='Porcentagem de anuncios: %{y:.3p}' +
    '<br>Semestre: %{x}<br><extra></extra>')
fig_requisito_semestre.update_layout(margin=dict(l=20, r=20, b=20, t=20,
                                                 pad=5),
                                     height=400,
                                     paper_bgcolor='rgba(0,0,0,0)',
                                     plot_bgcolor='rgba(0,0,0,0)')
fig_requisito_semestre.update_yaxes(tickformat='%{text:.3p}')
fig_requisito_semestre.update_xaxes(dtick=1,
                                    showticksuffix='all',
                                    ticksuffix="°")

st.plotly_chart(fig_requisito_semestre,
                use_container_width=True,
                **{'config': config_plotly})

st.subheader('3.2. Semestralização Máxima')
st.write(
    'Pelo lado da semestralização limite, quase 3/4 das ofertas de estágio não impôem limite de semestralização. O restante das ofertas de estágio possuem um limite máximo de semestralização do sexto ao nono semestre'
)

# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_maximo_semestre = go.Figure()
fig_maximo_semestre.add_trace(
    go.Bar(
        x=index_semestres,
        y=maximo_semestre,
        name='Requisito Semestre',
    ))
fig_maximo_semestre.update_traces(
    text=maximo_semestre,
    texttemplate='%{text:.3p}',
    textposition="outside",
    hovertemplate='Porcentagem de anuncios: %{y:.3p}' +
    '<br>Semestre: %{x}<br><extra></extra>')
fig_maximo_semestre.update_layout(margin=dict(l=20, r=20, b=20, t=20, pad=5),
                                  height=400,
                                  paper_bgcolor='rgba(0,0,0,0)',
                                  plot_bgcolor='rgba(0,0,0,0)')
fig_maximo_semestre.update_yaxes(tickformat='%{text:.3p}')
fig_maximo_semestre.update_xaxes(dtick=1, showticksuffix='all', ticksuffix="°")

st.plotly_chart(fig_maximo_semestre,
                use_container_width=True,
                **{'config': config_plotly})

st.header('4. Pré-requisitos e diferenciais')

st.subheader('4.1. Pré-requisitos mais comuns')
st.write(
    'A seguir, observou-se os pré-requisitos mais comuns pedidos pelas empresas:'
)

# Pega os requisitos em cada anuncio, pegando cada subitem da lista de requisitos e os conta
requisitos = pd.Series([
    item for sublist in dados_df.requisitos for item in sublist
]).value_counts()

# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_requisitos = go.Figure(
    data=[go.Bar(y=requisitos.index, x=requisitos, orientation='h')])
fig_requisitos.update_traces(text=requisitos,
                             textposition="inside",
                             hovertemplate='N° de anuncios: %{x}' +
                             '<br>Pré-requisito: %{y}<br><extra></extra>')
fig_requisitos.update_yaxes(autorange="reversed")
fig_requisitos.update_layout(margin=dict(l=0, r=0, b=20, t=20, pad=5),
                             height=800,
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)')

st.plotly_chart(fig_requisitos,
                use_container_width=True,
                **{'config': config_plotly})

st.subheader('4.2. Existência de Pré-requisitos')
st.write(
    'Verificou-se também a proporção entre empresas que pedem pré-requisitos nos anuncios de estágio e aquelas que não o fazem. Neste caso, mais da metade das empresas não demandam nenhum pré-requisito'
)

# Contagem da quantidade de empresas que pedem pré-requisitos vs Empresas que não o fazem
presenca_requisito_dict = {'Sem pré-requisitos': 0, 'Com pré-requisitos': 0}
for requisito in dados_df['requisitos']:
    if len(requisito):
        presenca_requisito_dict['Com pré-requisitos'] += 1
    else:
        presenca_requisito_dict['Sem pré-requisitos'] += 1
df_presenca_requisito = pd.DataFrame.from_dict(presenca_requisito_dict,
                                               orient='index',
                                               columns=['contagem'])
                                               
# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_presenca_requisito = go.Figure(data=[
    go.Pie(labels=df_presenca_requisito.index,
           values=df_presenca_requisito['contagem'],
           textinfo='label+percent',
           insidetextorientation='radial',
           marker_colors=['#EF553B', '#636EFA'])
])
fig_presenca_requisito.update_traces(hovertemplate='%{label}' +
                                     '<br>Contagem: %{value}' +
                                     '<br>%{percent}<extra></extra>',
                                     textposition='inside')
fig_presenca_requisito.update_layout(margin=dict(l=20, r=20, b=20, t=20,
                                                 pad=0),
                                     height=400,
                                     paper_bgcolor='rgba(0,0,0,0)',
                                     plot_bgcolor='rgba(0,0,0,0)',
                                     uniformtext_minsize=12,
                                     uniformtext_mode='hide',
                                     showlegend=False)
st.plotly_chart(fig_presenca_requisito,
                use_container_width=True,
                **{'config': config_plotly})

st.subheader('4.3. Pré-requisitos filtrados por área de atuação')
st.write('A seguir, podem ser filtrados os requisitos mais comuns por área:')

# Pega os requisitos filtrados por área usando um selectbox para seleção
filtro_area = st.selectbox('Escolha a área:', options=dados_df.area.unique())
requisitos_filtrado = pd.Series([
    item
    for sublist in dados_df[dados_df['area'] == filtro_area.upper()].requisitos
    for item in sublist
]).value_counts()

# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_requisitos_filtrado = go.Figure(data=[
    go.Bar(y=requisitos_filtrado.index, x=requisitos_filtrado, orientation='h')
])
fig_requisitos_filtrado.update_traces(
    text=requisitos_filtrado,
    textposition="inside",
    hovertemplate='N° de anuncios: %{x}' +
    '<br>Pré-requisito: %{y}<br><extra></extra>')
fig_requisitos_filtrado.update_yaxes(autorange="reversed")
fig_requisitos_filtrado.update_layout(margin=dict(l=0, r=0, b=20, t=20, pad=5),
                                      height=500,
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      plot_bgcolor='rgba(0,0,0,0)')

st.plotly_chart(fig_requisitos_filtrado,
                use_container_width=True,
                **{'config': config_plotly})

st.subheader('4.4. Diferenciais mais comuns')
st.write(
    'Abaixo estão relacionados os diferenciais mais comuns, habilidades opcionais que concedem ao candidato uma vantagem em relação aos seus pares'
)

# Pega os diferenciais dos anuncios separadamente pegando cada subitem da lista de diferenciais e os conta
diferenciais = pd.Series([
    item for sublist in dados_df.diferenciais for item in sublist
]).value_counts()

# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_diferenciais = go.Figure(
    data=[go.Bar(y=diferenciais.index, x=diferenciais, orientation='h')])
fig_diferenciais.update_traces(text=diferenciais,
                               textposition="inside",
                               hovertemplate='N° de anuncios: %{x}' +
                               '<br>Diferencial: %{y}<br><extra></extra>')
fig_diferenciais.update_yaxes(autorange="reversed")
fig_diferenciais.update_layout(margin=dict(l=0, r=0, b=20, t=20, pad=5),
                               height=1200,
                               paper_bgcolor='rgba(0,0,0,0)',
                               plot_bgcolor='rgba(0,0,0,0)')

st.plotly_chart(fig_diferenciais,
                use_container_width=True,
                **{'config': config_plotly})

st.header('5. Carga Horária Semanal')
st.write(
    'Em relação a carga horária dos estágios ofertados, a maioria dos anuncios de estágio não informam a carga horária requisitada ou possuem carga horária fléxivel'
)
st.write(
    'Mais de 1/4 dos anuncios possuem a carga horária de 30 horas semanais, seguida das 20 horas semanais'
)

# Pega as cargas horárias e os formata para melhor visualização
dados_carga = dados_df['carga_horaria'].value_counts()
dados_carga = dados_carga.add_suffix('h')
dados_carga.rename(index={'0h': 'N/A'}, inplace=True)

# Configura o plot pelo plotly e o carrega usando a função correspondente do streamlit
fig_cargah = go.Figure(data=[
    go.Pie(labels=dados_carga.index,
           values=dados_carga,
           textinfo='label+percent',
           insidetextorientation='radial')
])
fig_cargah.update_traces(hovertemplate='Carga Horária: %{label}' +
                         '<br>Contagem: %{value}' +
                         '<br>%{percent}<extra></extra>',
                         textposition='outside')
fig_cargah.update_layout(margin=dict(l=20, r=20, b=20, t=20, pad=0),
                         height=400,
                         paper_bgcolor='rgba(0,0,0,0)',
                         plot_bgcolor='rgba(0,0,0,0)',
                         uniformtext_minsize=12,
                         uniformtext_mode='hide',
                         showlegend=False)
st.plotly_chart(fig_cargah,
                use_container_width=True,
                **{'config': config_plotly})

st.header('6. Ofertas por Empresa')
st.write(
    'Podemos verificar na nuvem de palavras a seguir o nome de todas as empresas que já realizaram anuncios através do Centro de Atendimento à Graduação - CEAG Politecnica e Colegiado de Engenharia Elétrica com vagas para Engenharia Elétrica/Eletrônica'
)
st.write(
    'Observa-se que as empresas maiores na nuvem são as que possuem maior número de anuncios realizados no período estudado, demonstrando maior regularidade nas seleções de estágio'
)

# Conta a quantidade de anuncios por empresa e cria uma nuvem de palavras baseado na frequência destas
dados_por_empresa = dados_df['empresa'].value_counts()
wordcloud_empresa = WordCloud(
    stopwords=STOPWORDS,
    background_color='rgb(14, 17, 23)',
    height=800,
    width=800,
    random_state=2,
    colormap='rainbow',
    collocations=False,
).generate_from_frequencies(dados_por_empresa)
st.image(wordcloud_empresa.to_array(), use_column_width='always')
st.write('No total, são **' + str(len(dados_df['empresa'].unique())) + '** empresas que realizaram **' + str(len(dados_df['empresa'])) + '** anuncios de estágio pelos canais de comunicação estudados')
st.write('')

st.header('7. Navegação pelos dados')
st.write(
    'Pesquise abaixo o nome da empresa para ver todos os seus anuncios de estágio'
)

# Realiza a filtragem dos dados baseado no nome da empresa digitado e dos dados a mostrar selecionados
empresa_search = st.text_input(label="Digite o nome da empresa e dê enter:")
columns = st.multiselect(label='Selecione os dados a mostrar:',
                         options=dados_df.columns.to_list(),
                         default=['empresa', 'periodo'])
dados_df_filtrado = dados_df
if empresa_search != '':
    dados_df_filtrado = dados_df[dados_df['empresa'] == empresa_search.upper(
    )]  
    dados_df_filtrado = dados_df_filtrado[columns]
else:
    dados_df_filtrado = dados_df
    dados_df_filtrado = dados_df_filtrado[columns]

# Mostra o dataframe filtrado
st.dataframe(dados_df_filtrado, height=400) 

# Custom Footer
st.markdown("""---""")
st.markdown("""Feito com Streamlit, por [b-rbmp](https://github.com/b-rbmp/ "Perfil GitHub")""")
