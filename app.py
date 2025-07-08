import pandas as pd
import dash
from dash import dcc,html,Input,Output
import plotly.express as px

#Cargar los datos excel
Dataf = pd.read_excel('notas_estudiantes_limpio.xlsx')
print(Dataf)

#Inicializar la app
app = dash.Dash(__name__)
app.title = 'Estadistica notas'
server = app.server

#Crear el layout
app.layout = html.Div([
    #Crear el titulo del tablero
    html.H1("Tablero de notas de estudiantes",style={"textAlign":"center",
                                                     "color":"#ee0eab",
                                                     "padding":"20px",
                                                     "fontFamily":"Arrial",
                                                     "BackgroundColor":"#7a2cc7"}),

#Crear la barra de seleccion de materias
    html.Label("Selccionar una materia: ",style={"margin":"10px"}),
    dcc.Dropdown(id="filtro_materia",
                 options=[{"label":carrera,"value":carrera} for carrera in sorted(Dataf["Carrera"].unique())],
                 value=Dataf["Carrera"].unique()[0],
                 style={"width":"50%","margin":"auto"}
                ),
    html.Br(),
#Crear los tabs
    dcc.Tabs([
        dcc.Tab(label='Grafico de promedios',children=dcc.Graph(id='histograma')
    ),
    dcc.Tab(label="Edad vs Promedio",children=[dcc.Graph(id='dispersion')
    ]),
    dcc.Tab(label="Desempeño",children=[dcc.Graph(id='pie')
    ]),
    dcc.Tab(label="Promedio notas x carrera ",children=[dcc.Graph(id='barras')
    ]),
 ], style={"fontWeight":"bold","color":"#05294d"})

    ])
#actualizar el grafico
@app.callback(
        #Se llama los outputs creados en el layout
        Output("histograma","figure"),
        Output("dispersion","figure"),
        Output("pie","figure"),
        Output("barras","figure"),
        Input("filtro_materia", 'value')
)
#Funcion para actualizar el grafico
def actualizar(filtro_materia):
    filtro= Dataf[Dataf["Carrera"]==filtro_materia]

    #Crear los graficos
    #Grafico tipo histograma
    histo = px.histogram(filtro, x="Promedio",nbins=10,title=f"Distribucion de promedios - {filtro_materia}",
                         color_discrete_sequence=["#07cf22"]).update_layout(template="plotly_white",yaxis_title="Cantidad de estudiantes")

#Grafico de dispersion
    disper = px.scatter(filtro,x="Edad",y="Promedio",color="Desempeño",title=f"Edad vs Promedio - {filtro_materia}",
                     color_discrete_sequence=px.colors.qualitative.Set2).update_layout(template="presentation")
#grafico de pie
    pi = px.pie(filtro,names="Desempeño",values="Promedio",title=f"Desempeño - {filtro_materia}",
                color_discrete_sequence=px.colors.qualitative.Pastel).update_layout(template="plotly_dark")
#grafico de barras
    promedios = filtro.groupby("Carrera")["Promedio"].mean().reset_index()
    barr = px.bar(promedios,x="Carrera",y="Promedio",title="Promedio de notas por carrera",
                   color="Carrera",color_discrete_sequence=px.colors.qualitative.Prism).update_layout(template="ggplot2")
    return histo,disper,pi,barr
#Es una prueba
#Ejecutar la aplicacion
if __name__ == '__main__':
    app.run(debug=True)
    