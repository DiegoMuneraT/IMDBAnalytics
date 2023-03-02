from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie, Map
import pandas as pd
import geopandas as gpd
from django.conf import settings
import plotly.express as px

def home(request):

    #load dataframe
    df = pd.DataFrame(list(Movie.objects.all().values()))

    #load shp file
    worldMap =  Map.objects.filter()[0]
    file_name = worldMap.file_shp.path
    geo_df = gpd.read_file(file_name)[['ADMIN', 'ADM0_A3', 'geometry']]

    # Rename columns
    geo_df.columns = ['country', 'country_code', 'geometry']    

    #Process
    df = df.groupby('country').size().to_frame('Movies')
    df = pd.merge(left=geo_df, right=df, how='left', left_on='country', right_on='country')

    #Create figure
    fig = px.choropleth_mapbox(df,
                           geojson=df.geometry,
                           locations=df.index,
                           color="Movies",
                           mapbox_style="open-street-map",
                           opacity = 0.5,
                           zoom=0.5,
                           width = 1000,
                           height = 800,
                           labels = {'country': 'country'},

                           )
    #Convert figure to html                               
    chart = fig.to_html()
    context = {'chart': chart}
    
    #Sent figure to the template
    return render(request,'home.html',context)