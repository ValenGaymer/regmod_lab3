import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import numpy as np

data = {
    'Variable1': np.random.randn(100),
    'Variable2': np.random.randn(100),
    'Variable3': np.random.randn(100),
    'Variable4': np.random.randn(100),
    'Variable5': np.random.randn(100),
    'Variable6': np.random.randn(100)
}

df = pd.DataFrame(data)
fig_hist_variable1 = px.histogram(df, x="Variable1", marginal="box", nbins=30, title="Histograma Variable1", height=500, width=600)
fig_hist_variable2 = px.histogram(df, x="Variable2", marginal="box", nbins=30, title="Histograma Variable2", height=500, width=600)
fig_hist_variable3 = px.histogram(df, x="Variable3", marginal="box", nbins=30, title="Histograma Variable3", height=500, width=600)
fig_hist_variable4 = px.histogram(df, x="Variable1", marginal="box", nbins=30, title="Histograma Variable4", height=500, width=600)
fig_hist_variable5 = px.histogram(df, x="Variable2", marginal="box", nbins=30, title="Histograma Variable5", height=500, width=600)
fig_hist_variable6 = px.histogram(df, x="Variable3", marginal="box", nbins=30, title="Histograma Variable6", height=500, width=600)

correlation_matrix = df.corr()
fig_corr = px.imshow(correlation_matrix.values,
                     labels=dict(color="Correlación"),
                     x=df.columns,
                     y=df.columns,
                     title="Diagrama de Correlación Múltiple", height=500, width=1000)

fig = sp.make_subplots(rows=2, cols=3, subplot_titles=["Histograma Variable1", "Histograma Variable2", "Histograma Variable3", "Histograma Variable4", "Histograma Variable5", "Histograma Variable6"])

fig.add_trace(fig_hist_variable1['data'][0], row=1, col=1)
fig.add_trace(fig_hist_variable2['data'][0], row=1, col=2)
fig.add_trace(fig_hist_variable3['data'][0], row=1, col=3)
fig.add_trace(fig_hist_variable4['data'][0], row=2, col=1)
fig.add_trace(fig_hist_variable5['data'][0], row=2, col=2)
fig.add_trace(fig_hist_variable6['data'][0], row=2, col=3)

fig.update_layout(height=400, width=1200, showlegend=False)
fig.write_html('histogramas.html', auto_open=True)

with open('histogramas.html', 'a', encoding='utf-8') as f:
    f.write('<head><meta charset="UTF-8"><style>.custom-paragraph { text-align: center; font-size: 18px; color: #333; padding: 10px; background-color: #f0f0f0; border-radius: 10px; font-family: Arial, sans-serif; }</style></head>')
    f.write('<body>')
    f.write('<h1 style="text-align: center; font-family: Arial, sans-serif;">Modelo de regresión lineal y resumen estadístico</h1>')
    f.write(fig_corr.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write('<p class="custom-paragraph">Parrafitoomggg\n\n holaaaa \n jerhjkejkr Valen.</p>')
    f.write('</body>')
