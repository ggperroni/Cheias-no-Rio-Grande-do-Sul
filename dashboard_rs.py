import streamlit as st
import pandas as pd
import plotly.express as px

df_data = pd.read_csv("analise_ada_rhguaiba_municipios_10052024.csv", index_col=False, sep=",")
df_data