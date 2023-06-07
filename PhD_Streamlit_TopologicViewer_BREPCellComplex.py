import streamlit as st
import plotly.express as px

from topologicpy.CellComplex import CellComplex
from topologicpy.Plotly import Plotly
from topologicpy.Dictionary import Dictionary
from topologicpy.Topology import Topology
from topologicpy.Color import Color
from topologicpy.Cell import Cell
from topologicpy.Graph import Graph
from topologicpy.Aperture import Aperture

import plotly.graph_objs as go

import os

# Set filepath
current_dir = str(os.getcwd())
base_dir = '\JSON'
filename = "\CellComplex_Sample1.json"
relative_path = "https://github.com/angelomassafra/PhD/blob/main"+base_dir+filename

# Functions
def create_legend_trace(color, label):
    return go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=10, color=color), name=label, showlegend=True)

def Visualize_Cells_ByStringProp(tp_CellComplex,propName,faceOpacity):
     
    dataList = []
    data = Plotly.DataByTopology(tp_CellComplex, faceOpacity=faceOpacity, showVertexLegend=False, showEdgeLegend=False)
    dataList += data

    values = [Dictionary.ValueAtKey(Topology.Dictionary(tp_Cell), propName) for tp_Cell in CellComplex.Cells(tp_CellComplex)]
    values = sorted(list(set(values)))
    maxValue = len(values)
    values_numbers = [i for i in range(maxValue)]
        
    color_labels = []   

    for tp_Cell in CellComplex.Cells(tp_CellComplex):
        value = Dictionary.ValueAtKey(Topology.Dictionary(tp_Cell), propName)
        valueNum = values_numbers[values.index(value)]
        color = Color.ByValueInRange(value=valueNum, minValue=0, maxValue=maxValue, colorScale="turbo")
        colorStr = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        color_labels.append((colorStr, value))
        
        tp_Faces_bottomHorizontal = Cell.Decompose(tp_Cell)['bottomHorizontalFaces']
        for f in tp_Faces_bottomHorizontal:
            data = Plotly.DataByTopology(f, faceOpacity=1, faceColor=colorStr)
            dataList += data
    
    color_labels = sorted(list(set(color_labels)),key=lambda x: x[1])
    
    legend_traces = [create_legend_trace(color, label) for color, label in color_labels]
    legend_traces.insert(0, go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=0.1), name="<b>"+ propName[4:]+"</b>", showlegend=True))
    dataList.extend(legend_traces)
    
    fig = Plotly.FigureByData(dataList)
    st.plotly_chart(fig)

def Visualize_Cells_ByNumberProp(tp_CellComplex,propName,colorScale,faceOpacity):
    dataList = []
    data = Plotly.DataByTopology(tp_CellComplex, faceOpacity=faceOpacity, showVertexLegend=False, showEdgeLegend=False)
    dataList += data



    values = []
    for tp_Cell in CellComplex.Cells(tp_CellComplex):
        value = Dictionary.ValueAtKey(Topology.Dictionary(tp_Cell), propName)
        values.append(value)
        
    maxValue = max(values)

    for tp_Cell in CellComplex.Cells(tp_CellComplex):
        value = Dictionary.ValueAtKey(Topology.Dictionary(tp_Cell), propName)
        color = Color.ByValueInRange(value=value, minValue=0, maxValue=maxValue, colorScale=colorScale)
        colorStr = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        faces = Cell.Decompose(tp_Cell)['bottomHorizontalFaces']
        for f in faces:
            data = Plotly.DataByTopology(f, faceOpacity=1, faceColor=colorStr)
            dataList += data
            
    fig = Plotly.FigureByData(dataList)
    colorBar = Plotly.AddColorBar(figure=fig,values=values,colorScale=colorScale,title=propName[4:],nTicks=11,width=20)
    st.plotly_chart(fig)

def Visualize_Face_ByStrProp(tp_CellComplex,tp_Faces,tp_Face_PropName):
    dataList = []
    data = Plotly.DataByTopology(tp_CellComplex, faceOpacity=0.2, showVertexLegend=False, showEdgeLegend=False)
    dataList += data

    tp_Face_BetweenInformedSpace_Props = []

    for tp_Face in tp_Faces:
        tp_Face_Dictionary = Topology.Dictionary(tp_Face)
        tp_Face_BetweenInformedSpace_Prop = Dictionary.ValueAtKey(tp_Face_Dictionary, tp_Face_PropName)
        if tp_Face_BetweenInformedSpace_Prop is None:
            tp_Face_BetweenInformedSpace_Prop = 'Unknown'
        tp_Face_BetweenInformedSpace_Props.append(tp_Face_BetweenInformedSpace_Prop)
    tp_Face_BetweenInformedSpace_Props = sorted(list(set(tp_Face_BetweenInformedSpace_Props)))
    tp_Face_BetweenInformedSpace_Props_Number = [i for i in range(len(tp_Face_BetweenInformedSpace_Props))]

    color_labels = []
    for i, tp_Face_BetweenInformedSpace_Prop in enumerate(tp_Face_BetweenInformedSpace_Props):
        value = tp_Face_BetweenInformedSpace_Props_Number[i]
        color = Color.ByValueInRange(value=value, minValue=0, maxValue=len(tp_Face_BetweenInformedSpace_Props), colorScale="rainbow")
        colorStr = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        color_labels.append((colorStr, tp_Face_BetweenInformedSpace_Prop))

    for tp_Face in tp_Faces:
        tp_Face_Dictionary = Topology.Dictionary(tp_Face)
        tp_Face_BetweenInformedSpace_Prop = Dictionary.ValueAtKey(tp_Face_Dictionary, tp_Face_PropName)
        value = None

        if tp_Face_BetweenInformedSpace_Prop in tp_Face_BetweenInformedSpace_Props:
            index = tp_Face_BetweenInformedSpace_Props.index(tp_Face_BetweenInformedSpace_Prop)
            value = tp_Face_BetweenInformedSpace_Props_Number[index]
        else:
            value = 0

        color = Color.ByValueInRange(value=value, minValue=0, maxValue=len(tp_Face_BetweenInformedSpace_Props), colorScale="rainbow")
        colorStr = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"

        data = Plotly.DataByTopology(tp_Face, faceOpacity=1, faceColor=colorStr)
        dataList += data

    legend_traces = [create_legend_trace(color, label) for color, label in color_labels]
    legend_traces.insert(0, go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=0.1), name="<b>"+ tp_Face_PropName[4:].replace("_pSP_",": ")+"</b>", showlegend=True))
    dataList.extend(legend_traces)

    fig = Plotly.FigureByData(dataList)
    st.plotly_chart(fig)

def Visualize_Apertures_ByProp(tp_CellComplex,tp_Faces,tp_Aperture_PropName):
    dataList = []
    data = Plotly.DataByTopology(tp_CellComplex, faceOpacity=0.2, showVertexLegend=False, showEdgeLegend=False)
    dataList += data

    tp_Face_BetweenInformedSpace_Props = []
    
    tp_Apertures = []
    for tp_Face in tp_Faces:
        ap = Topology.Apertures(tp_Face)
        for a in ap:
            at = Aperture.ApertureTopology(a)
            tp_Apertures.append(at)

    for tp_Aperture in tp_Apertures:
        tp_Face_Dictionary = Topology.Dictionary(tp_Aperture)
        tp_Face_BetweenInformedSpace_Prop = Dictionary.ValueAtKey(tp_Face_Dictionary, tp_Aperture_PropName)
        tp_Face_BetweenInformedSpace_Props.append(tp_Face_BetweenInformedSpace_Prop)
    tp_Face_BetweenInformedSpace_Props = sorted(list(set(tp_Face_BetweenInformedSpace_Props)))
    tp_Face_BetweenInformedSpace_Props_Number = [i for i in range(len(tp_Face_BetweenInformedSpace_Props))]

    color_labels = []
    for i, tp_Face_BetweenInformedSpace_Prop in enumerate(tp_Face_BetweenInformedSpace_Props):
        value = tp_Face_BetweenInformedSpace_Props_Number[i]
        color = Color.ByValueInRange(value=value, minValue=0, maxValue=len(tp_Face_BetweenInformedSpace_Props), colorScale="rainbow")
        colorStr = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
        color_labels.append((colorStr, tp_Face_BetweenInformedSpace_Prop))

    for tp_Face in tp_Apertures:
        tp_Face_Dictionary = Topology.Dictionary(tp_Face)
        tp_Face_BetweenInformedSpace_Prop = Dictionary.ValueAtKey(tp_Face_Dictionary, tp_Aperture_PropName)
        value = None

        if tp_Face_BetweenInformedSpace_Prop in tp_Face_BetweenInformedSpace_Props:
            index = tp_Face_BetweenInformedSpace_Props.index(tp_Face_BetweenInformedSpace_Prop)
            value = tp_Face_BetweenInformedSpace_Props_Number[index]
        else:
            value = 0

        color = Color.ByValueInRange(value=value, minValue=0, maxValue=len(tp_Face_BetweenInformedSpace_Props), colorScale="rainbow")
        colorStr = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"

        data = Plotly.DataByTopology(tp_Face, faceOpacity=1, faceColor=colorStr)
        dataList += data

    legend_traces = [create_legend_trace(color, label) for color, label in color_labels]
    legend_traces.insert(0, go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=0.1), name="<b>"+ tp_Aperture_PropName[4:].replace("_pSP_",": ")+"</b>", showlegend=True))
    dataList.extend(legend_traces)

    fig = Plotly.FigureByData(dataList)
    st.plotly_chart(fig)

def Visualize_Graph(tp_CellComplex):
    dataList = []
    data = Plotly.DataByTopology(tp_CellComplex, faceOpacity=0.2, showVertexLegend=False, showEdgeLegend=False)
    dataList += data
        
    tp_CellComplex_Graph = Graph.ByTopology(tp_CellComplex,
                                            toExteriorApertures=True,
                                            viaSharedTopologies=False,
                                            viaSharedApertures=True,
                                            direct=False,
                                            directApertures=False)   
    data = Plotly.DataByGraph(tp_CellComplex_Graph,vertexColor="red",edgeWidth=3)
    dataList += data
        
    fig=Plotly.FigureByData(dataList)
    st.plotly_chart(fig)

def main():
    #Title
    st.markdown("<h1 style='font-size:24px;'>Topologic Viewer</h1>", unsafe_allow_html=True)
    st.write(relative_path)

    #CellComplex
    JSON_TopologicCellComplex_FilePath = relative_path
    tp_CellComplex = Topology.ByJSONPath(path=JSON_TopologicCellComplex_FilePath)

    #Visualization mode
    options_VisualizationMode = ['Cells','Faces','Apertures','Graph']
    selected_option_VisualizationMode = st.selectbox('Visualization Mode', options_VisualizationMode)

    #CellVisualization
    if selected_option_VisualizationMode == "Cells":
        # Define options for the dropdown menu
        options = []
        for tp_Cell in CellComplex.Cells(tp_CellComplex):
            d = Topology.Dictionary(tp_Cell)
            k = list(Dictionary.Keys(d))
            j=0
            for i in k:
                if i not in options:
                    options.append(i)
                j=j+1
        options=sorted(list(set(options)))
        selected_option = st.selectbox('Key', options)
        #Strings
        a_Cell = CellComplex.Cells(tp_CellComplex)[0]
        d = Topology.Dictionary(a_Cell)
        v = Dictionary.ValueAtKey(d,selected_option)
        if isinstance(v,str):
            # Create a sample plot using Plotly
            Visualize_Cells_ByStringProp(tp_CellComplex,selected_option,0.2)
        elif isinstance(v,float) or isinstance(v,int):
            Visualize_Cells_ByNumberProp(tp_CellComplex,selected_option,'plasma',0.2)

    #FaceVisualization
    if selected_option_VisualizationMode == "Faces":

        # Define options for the dropdown menu
        options_faceType = ['externalVerticalFaces','internalVerticalFaces','internalHorizontalFaces','bottomHorizontalFaces','topHorizontalFaces']
        selected_option_faceType = st.selectbox('FaceType', options_faceType)

        # Define options for the dropdown menu
        options = []
        tp_Faces = CellComplex.Decompose(tp_CellComplex)[selected_option_faceType]
        for tp_Face in tp_Faces:
            d = Topology.Dictionary(tp_Face)
            k = list(Dictionary.Keys(d))
            v = list(Dictionary.Values(d))
            j=0
            for i in k:
                if i not in options:
                    if isinstance(v[j],str):
                        options.append(i)
                j=j+1
        options=sorted(list(set(options)))
        selected_option = st.selectbox('Key', options)

        # Plotly
        Visualize_Face_ByStrProp(tp_CellComplex,tp_Faces,selected_option)

    #Aperture Visualizaton
    if selected_option_VisualizationMode == "Apertures":

        # Define options for the dropdown menu
        options_faceType = ['externalVerticalFaces','internalVerticalFaces','internalHorizontalFaces','bottomHorizontalFaces','topHorizontalFaces']
        selected_option_faceType = st.selectbox('FaceType', options_faceType)

        # Define options for the dropdown menu
        options = []
        tp_Faces = CellComplex.Decompose(tp_CellComplex)[selected_option_faceType]
        tp_Apertures = []
        for tp_Face in tp_Faces:
            ap = Topology.Apertures(tp_Face)
            for a in ap:
                at = Aperture.ApertureTopology(a)
            tp_Apertures.append(at)
        for tp_Aperture in tp_Apertures:
            d = Topology.Dictionary(tp_Aperture)
            k = list(Dictionary.Keys(d))
            v = list(Dictionary.Values(d))
            j=0
            for i in k:
                if i not in options:
                    if isinstance(v[j],str):
                        options.append(i)
                j=j+1
        options=sorted(list(set(options)))
        selected_option = st.selectbox('Key', options)

        # Plotly
        Visualize_Apertures_ByProp(tp_CellComplex,tp_Faces,selected_option)

    #Graph Visualization
    if selected_option_VisualizationMode == "Graph":
        Visualize_Graph(tp_CellComplex)



if __name__ == '__main__':
    main()
