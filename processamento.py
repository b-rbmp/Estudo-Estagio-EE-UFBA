import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot

dados_df = pd.read_json('estagio_data.json', encoding='UTF-8', dtype='object')

index_semestres = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
requisito_semestre = dados_df['requisito_semestre'].value_counts(
    normalize=True).reindex(index_semestres, fill_value=0)
maximo_semestre = dados_df['maximo_semestre'].value_counts(
    normalize=True).reindex(index_semestres, fill_value=0)
requisito_semestre.rename(index={0: 'N/A'}, inplace=True)
#plot(fig)