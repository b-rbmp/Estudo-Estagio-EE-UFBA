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
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

dados_df = pd.read_json('estagio_data.json', encoding='UTF-8')

# APP

'''
# Estudo Estágio Engenharia Elétrica UFBA ![alt text](https://github.com/b-rbmp/Estudo-Estagio-EE-UFBA/blob/main/assets/images/brasao_ufba.png "Universidade Federal Da Bahia")
'''

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

st.subheader('Período vs Quantidade de Ofertas')
st.write('Verificamos a quantidade de ofertas de estágio em cada semestre. ')
ofertas_por_semestre = dados_df['periodo'].value_counts()

fig_ofertas_semestre = go.Figure(data=[
    go.Bar(x=ofertas_por_semestre.index,
           y=ofertas_por_semestre)
])
# Customize aspect
fig_ofertas_semestre.update_traces(textposition='outside')
fig_ofertas_semestre.update_layout(uniformtext_minsize=8,
                                   uniformtext_mode='hide')

st.bar_chart(data=ofertas_por_semestre,
             width=0,
             height=0,
             use_container_width=True)
#st.plotly_chart(fig_ofertas_semestre, use_container_width=True)

st.subheader('Ofertas de estágio por Área')
st.write('**@TODO: Piechart mostrando as ofertas por área**')
st.write('**@TODO: Piechart comparando GERAL vs Especifico**')
st.write('**@TODO: Tabela mostrando as ofertas por área/subarea**')

st.subheader('Requisitos de Semestralização')
st.write('**@TODO: Barplot vertical mostrando semestre mínimo e máximo**')

st.subheader('Requisitos mais comuns')
st.write('**@TODO: Barplot horizontal mostrando requisitos mais comuns**')
st.write('**@TODO: Tabela filtrando requisitos mais comuns por ÁREA**')

st.subheader('Diferenciais mais comuns')
st.write('**@TODO: Barplot horizontal mostrando diferenciais mais comuns**')

st.subheader('Carga Horária')
st.write('**@TODO: Barplot vertical mostrando cargas horárias**')

st.subheader('Ofertas por Empresa')
st.write(
    '**@TODO: Barplot horizontal ou lista com empresas com mais ofertas de estágio**'
)
st.write(
    '**@TODO: Pesquise abaixo o nome da empresa para ver todos os seus anuncios de estágio**'
)

st.subheader(
    '@TODO: Pegar se empresa fazia processo seletivo global ou anuncio apenas para elétrica'
)
st.write('**@TODO: Piechart mostrando a problematica acima**')
