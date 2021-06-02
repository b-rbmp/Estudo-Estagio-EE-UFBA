import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot

dados_df = pd.read_json('estagio_data.json', encoding='UTF-8')

dados_por_empresa = dados_df['empresa'].value_counts()
#plot(fig)