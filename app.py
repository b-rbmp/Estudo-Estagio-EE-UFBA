# -*- coding: utf-8 -*-

# APENAS ESTÁGIOS NA REGIÃO PROXIMA DE SALVADOR! E TIRANDO MARKETING/COMERCIAL
# Periodo: Data limite para enviar curriculo.
# Se indisponível, data que a vaga foi postada pela primeira vez
# Para requisito e maximo semestre, as vezes é utilizado o periodo pedido em relação a
# previsão de formatura. Ex: Disponibilidade para estagiar pelo menos 1 ano: Maximo_semestre = 10 - 2 = 8
# Informações conforme informado na divulgação das empresas pelos
# Centro de Atendimento à Graduação - CEAG Politecnica e Colegiado de Engenharia Elétrica
# Vagas em desenvolvimento de Software são ignoradas (consideradas como Eng Computação/Ciencia
# da Computação) a menos que vinculo claro com alguma área de Eng Elétrica/Eletrônica/Hardware
# Para grandes empresas, foi feito uma pesquisa no linkedin OU google para observar se as empresas
# ofereciam vagas de estágio em áreas relacionadas a engenharia elétrica. (quando não informavam nos sites
# de inscrição ou nos flyers)
from typing import Dict
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

dados_df = pd.read_json('estagio_data.json', encoding='UTF-8')

config_plotly = {'displayModeBar': False}

# APP

st.title('Estudo Estágio Engenharia Elétrica UFBA')
st.write('')
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
    'Considerou-se também o período (semestre) com a data limite para envio do currículo/inscrição no Processo Seletivo, e para os requisito ou máximo semestre matriculado, as vezes é utilizado o periodo pedido em relação a previsão de formatura.'
)

st.header('1. Período vs Quantidade de anuncios')
st.write(
    'Observando a quantidade de anuncios de estágio em cada semestre, verificou-se um aumento progressivo com os anos, interrompido durante o período de adaptação para o COVID-19 (2020.1 e 2020.2)'
)
# Conta quantos anuncios por semestre
ofertas_por_semestre = dados_df['periodo'].value_counts()
# Configura o plot pelo plotly
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
    'Observa-se uma predominância de ofertas de estágio sem especificação da vaga (Geral), com quase metade dos anuncios nesta categoria. Não é uma surpresa, pois a maioria das grandes empresas abrem um processo seletivo genérico, abrindo para todas engenharias e outros cursos.'
)
st.write(
    'Por outro lado, das empresas que selecionam estagiários para vagas específicas, a área de potência é a mais requisitada, com mais de 1/4 dos anuncios para esta área, seguido de controle, eletrônica e computação.'
)
ofertas_por_area = dados_df['area'].value_counts()
# Configura o plot pelo plotly
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

st.header('3. Requisitos de Semestralização/Previsão de Formatura')
st.write(
    'Nesta seção, foram considerados equivalentes os requisitos de previsão de formatura e semestralização. Quando informado a previsão de formatura desejada pela empresa, este foi convertido em semestralização considerando o semestre em que o anuncio foi feito.'
)
st.write(
    'Semestre 0 significa que não há requisito mínimo de semestre e semestre 10 significa que não há limite de semestralização máximo.'
)
# Manipulação de dados
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
    'Por outro lado, observou-se 1/4 das empresas requerem semestralização minima do quinto semestre e outros 1/4 no sexto semestre, excluindo dos processos seletivos os estudantes matriculados nos semestres iniciais'
)

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
requisitos = pd.Series([
    item for sublist in dados_df.requisitos for item in sublist
]).value_counts()

fig_requisitos = go.Figure(
    data=[go.Bar(y=requisitos.index, x=requisitos, orientation='h')])
fig_requisitos.update_traces(text=requisitos,
                             textposition="outside",
                             hovertemplate='N° de anuncios: %{x}' +
                             '<br>Pré-requisito: %{y}<br><extra></extra>')
fig_requisitos.update_yaxes(autorange="reversed")
fig_requisitos.update_layout(margin=dict(l=0, r=0, b=20, t=20, pad=5),
                             height=500,
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)')

st.plotly_chart(fig_requisitos,
                use_container_width=True,
                **{'config': config_plotly})

st.write(
    'Verificou-se também a proporção entre empresas que pedem pré-requisitos nos anuncios de estágio e aquelas que não o fazem. Neste caso, mais da metade das empresas não demandam nenhum pré-requisito.'
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

fig_presenca_requisito = go.Figure(data=[
    go.Pie(labels=df_presenca_requisito.index,
           values=df_presenca_requisito['contagem'],
           textinfo='label+percent',
           insidetextorientation='radial',
           marker_colors=['#EF553B', '#636EFA'])
])
fig_presenca_requisito.update_traces(hovertemplate='Área: %{label}' +
                                     '<br>Contagem: %{value}' +
                                     '<br>%{percent}<extra></extra>',
                                     textposition='outside')
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

st.write('**@TODO: Tabela filtrando requisitos mais comuns por ÁREA**')

st.subheader('4.2. Diferenciais mais comuns')
st.write(
    'Abaixo estão relacionados os diferenciais mais comuns, habilidades opcionais que concedem ao candidato uma vantagem em relação aos seus pares'
)
diferenciais = pd.Series([
    item for sublist in dados_df.diferenciais for item in sublist
]).value_counts()

fig_diferenciais = go.Figure(
    data=[go.Bar(y=diferenciais.index, x=diferenciais, orientation='h')])
fig_diferenciais.update_traces(text=diferenciais,
                               textposition="outside",
                               hovertemplate='N° de anuncios: %{x}' +
                               '<br>Diferencial: %{y}<br><extra></extra>')
fig_diferenciais.update_yaxes(autorange="reversed")
fig_diferenciais.update_layout(margin=dict(l=0, r=0, b=20, t=20, pad=5),
                               height=800,
                               paper_bgcolor='rgba(0,0,0,0)',
                               plot_bgcolor='rgba(0,0,0,0)')

st.plotly_chart(fig_diferenciais,
                use_container_width=True,
                **{'config': config_plotly})

st.header('Carga Horária Semanal')
st.write(
    'Em relação a carga horária dos estágios ofertados, a maioria dos anuncios de estágio não informam a carga horária requisitada ou possuem carga horária fléxivel.'
)
st.write(
    'Mais de 1/4 dos anuncios possuem a carga horária de 30 horas semanais, seguida das 20 horas semanais.'
)
dados_carga = dados_df['carga_horaria'].value_counts()
dados_carga = dados_carga.add_suffix('h')
dados_carga.rename(index={'0h': 'N/A'}, inplace=True)
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

st.header('5. Ofertas por Empresa')
st.write(
    '**@TODO: Barplot horizontal ou lista com empresas com mais ofertas de estágio**'
)
st.write(
    'Pesquise abaixo o nome da empresa para ver todos os seus anuncios de estágio'
)

st.header(
    '@TODO: Pegar se empresa fazia processo seletivo global ou anuncio apenas para elétrica'
)
st.write('**@TODO: Piechart mostrando a problematica acima**')
