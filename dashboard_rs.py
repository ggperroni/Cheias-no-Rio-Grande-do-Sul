import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide")

state = json.load(open("geojson/state_of_rs.geojson", 'r', encoding="utf8"))

state_id_map = {}
for feature in state["features"]:
    feature["id"] = feature["properties"]["id"]
    state_id_map[feature["properties"]["name"]] = feature["id"]

df_data = pd.read_csv("datasets/analise_ada_rhguaiba_municipios_10052024.csv", index_col=False, sep=",")
df = df_data.rename(columns={"CD_MUN": "codigo_ibge"})
df_cities = pd.read_csv("datasets/municipios.csv", index_col=False, sep=",")

df_rs = df.merge(df_cities, how="left", on="codigo_ibge")
df_rs["id"] = df_rs["NM_MUN"].apply(lambda x: state_id_map[x])

st.write("# Cheias no Rio Grande do Sul")
st.write("## Base de dados e informações geográficas na Região Hidrográfica do Lago Guaíba em 2024")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

fig_map_people = px.choropleth_mapbox(df_rs, 
                               locations="codigo_ibge",
                               geojson=state,
                               color="Pessoas_afetadas",
                               hover_name="NM_MUN",
                               mapbox_style="open-street-map",
                               center={"lat": -29.9845, "lon": -52.3711},
                               zoom=5.8,
                               opacity=0.5,
                               color_continuous_scale=[(0, "grey"), (0.7, "yellow"), (1, "red")],
                               title="Pessoas afetadas pelas cheias em maio de 2024")
col1.plotly_chart(fig_map_people, use_container_width=True)

fig_per_people = px.pie(df_rs, values=df_rs["Pessoas_afetadas"].head(10), names=df_rs["NM_MUN"].head(10), title="Pessoas afetadas por município (%)")
col2.plotly_chart(fig_per_people, use_container_width=True)

fig_map_places = px.choropleth_mapbox(df_rs, 
                               locations="codigo_ibge",
                               geojson=state,
                               color="Vias_Diretamente_Afetadas_km",
                               hover_name="NM_MUN",
                               mapbox_style="open-street-map",
                               center={"lat": -29.9845, "lon": -52.3711},
                               zoom=5.8,
                               opacity=0.5,
                               color_continuous_scale=[(0, "grey"), (0.7, "yellow"), (1, "red")],
                               title="Vias diretamente obstruídas pelas cheias em maio de 2024")
col3.plotly_chart(fig_map_places, use_container_width=True)

fig_per_places = px.pie(df_rs, values=df_rs["Vias_Diretamente_Afetadas_km"].head(10), names=df_rs["NM_MUN"].head(10), title="Vias obstruídas por município (%)")
col4.plotly_chart(fig_per_places, use_container_width=True)

fig_map_area = px.choropleth_mapbox(df_rs, 
                               locations="codigo_ibge",
                               geojson=state,
                               color="Area_Diretamente_Afetada_Municipio_%",
                               hover_name="NM_MUN",
                               mapbox_style="open-street-map",
                               center={"lat": -29.9845, "lon": -52.3711},
                               zoom=7.5,
                               opacity=0.5,
                               color_continuous_scale=[(0, "grey"), (0.7, "yellow"), (1, "red")],
                               title="Área afetada por município (%)")
st.plotly_chart(fig_map_area, use_container_width=True)

st.write("Desenvolvido por [Guilherme Perroni](https://guilhermeperroni.com)")