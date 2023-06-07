import streamlit as st
import plotly.express as px
import topologicpy
from topologicpy.CellComplex import CellComplex
from topologicpy.Plotly import Plotly

def main():
    #Title
    st.markdown("<h1 style='font-size:24px;'>Topologic Viewer</h1>", unsafe_allow_html=True)

    # Add a slider from 0 to 1 with customized color
    slider_vSides_value = st.slider("V Sides", 1, 5, 1, step=1, key="slider_vSides", format="%.2i")
    slider_uSides_value = st.slider("U Sides", 1, 5, 1, step=1, key="slider_uSides", format="%.2i")
    slider_wSides_value = st.slider("W Sides", 1, 5, 1, step=1, key="slider_wSides", format="%.2i")

    #CellComplex
    tp_CellComplex = CellComplex.Prism(vSides=slider_vSides_value,uSides=slider_uSides_value,wSides=slider_wSides_value)

    # Create a sample plot using Plotly
    dataList = []
    data = Plotly.DataByTopology(tp_CellComplex,faceOpacity=0.2)
    dataList += data
    fig = Plotly.FigureByData(data)
    fig.update_layout(width=700)
    Plotly.SetCamera(fig,camera=[1.5,1.5,1.5],target=[0,0,0],up=[0,0,1])
    st.plotly_chart(fig)

if __name__ == '__main__':
    main()
