import plotly.express as px
import plotly.subplots as sp
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import webbrowser

data = {
    'Variable1': np.random.randn(100),
    'Variable2': np.random.randn(100),
    'Variable3': np.random.randn(100),
    'Variable4': np.random.randn(100),
    'Variable5': np.random.randn(100),
    'Variable6': np.random.randn(100)
}

df = pd.DataFrame(data)


color_palette = ["#de6e4b", "#7fd1b9", "#7fd1b9", "#7a6563", "#E56399"]
correlation_matrix = df.corr()
fig_corr = px.imshow(correlation_matrix.values,
                     labels=dict(color="Correlación"),
                     x=df.columns,
                     y=df.columns,
                     title="Diagrama de Correlación Múltiple", height=500, width=1000,
                     color_continuous_scale = ["#7FD1B9", "#de6e4b"])

with open('histogramas.html', 'w', encoding='utf-8') as f:
    f.write('<html>')
    f.write('<head><meta charset="UTF-8"><style>')
    f.write('.toc-container { position: fixed; top: 0px; right: 0; padding: 10px; background-color: #fff; border; font-family: Arial, sans-serif; }')
    f.write('.toc-title { font-size: 18px; color: rgb(229, 99, 153); margin-bottom: 10px; }')
    f.write('.toc-list { list-style-type: none; padding: 0; margin: 0; }')
    f.write('.toc-item { margin-bottom: 5px; }')
    f.write('.toc-link { text-decoration: none; color: #333; font-weight: bold; }')
    f.write('.toc-link:hover { color: rgb(229, 99, 153); }')
    f.write('</style></head>')
    f.write('<body style="background-color: #ffffff;">')

    f.write('<h1 style="text-align: left; font-family: Arial, sans-serif; padding: 30px; color: white; background-color: rgb(127, 209, 185);">RESUMEN ESTADÍSTICO</h1>')

    f.write('<h2 id = "histogramas" style="text-align: left; font-family: Arial, sans-serif; padding: 20px; color: rgb(229, 99, 153);">Histogramas</h2>')
    for i, variable in enumerate(df.columns, start=1):
        fig_hist_variable = px.histogram(df, x=variable, marginal="box", nbins=30, title=f"Histograma de {variable}", height=500, width=600, color_discrete_sequence=[color_palette[i % len(color_palette)]])
        f.write(fig_hist_variable.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write('<h2 id = "correlacion" style="text-align: left; font-family: Arial, sans-serif; padding: 20px; color: rgb(222, 110, 75);">Correlación</h2>') 
    f.write(fig_corr.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write('<h2 id = "modelo" style="text-align: left; font-family: Arial, sans-serif; padding: 20px; color: rgb(127, 209, 185);">Modelo de regresión lineal</h2>') 
    f.write('<h2 id = "analisis" style="text-align: left; font-family: Arial, sans-serif; padding: 20px; color: rgb(127, 209, 185);">Análisis</h2>') 
    f.write('<p style = "text-align: center; font-size: 18px; color: #333; padding: 20px; background-color: #f0f0f0; border-radius: 10px; font-family: Arial, sans-serif;">Parrafitoomggg\n\n holaaaa \n jerhjkejkr Valen.</p>')


    f.write('<div class="toc-container">')
    f.write('<h2 class="toc-title">Tabla de Contenidos</h2>')
    f.write('<ul class="toc-list">')
    f.write('<li class="toc-item"><a class="toc-link" href="#histogramas">Histogramas</a></li>')
    f.write('<li class="toc-item"><a class="toc-link" href="#correlacion">Correlación</a></li>')
    f.write('<li class="toc-item"><a class="toc-link" href="#modelo">Modelo de regresión lineal</a></li>')
    f.write('<li class="toc-item"><a class="toc-link" href="#analisis">Análisis</a></li>')
    f.write('</ul>')
    f.write('</div>')

    f.write('</body>')
    f.write('</html>')

webbrowser.open('histogramas.html', new=2)

