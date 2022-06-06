# coding: utf-8

import branca.colormap as cm
import folium
from folium import plugins
import geopandas as gpd

# foliumでマップ作成

# ベースマップ
map = folium.Map(
    tiles = None,
    location = [34.5496419, 135.7788521],
    zoom_start = 9,
    control_scale = True
)

# 国土地理院(白地図)
folium.raster_layers.TileLayer(
    'https://cyberjapandata.gsi.go.jp/xyz/blank/{z}/{x}/{y}.png',
    name = "国土地理院(白地図)",
    attr = "<a href='https://maps.gsi.go.jp/development/ichiran.html'>国土地理院</a>"
).add_to(map)

# Googleマップ標準
folium.raster_layers.TileLayer(
    'https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    subdomains = ['mt0','mt1','mt2','mt3'],
    name = "Google Map",
    attr = "<a href='https://developers.google.com/maps/documentation' target='_blank'>Google Map</a>"
).add_to(map)

# Googleマップ(航空写真)
folium.raster_layers.TileLayer(
    'https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',
    subdomains = ['mt0','mt1','mt2','mt3'],
    name = "Google Map(航空写真)",
    attr = "<a href='https://developers.google.com/maps/documentation' target='_blank'>Google Map</a>"
).add_to(map)

# TACポリゴン
gdf_TAC = gpd.read_file('TAC_Rakuten.geojson')

colormap = cm.StepColormap(
    colors=['#FF0000', '#FF9932', '#FFFF00', '#65FF32', '#008000', '#32CCFF', '#3265FF', '#FF32FF', '#ffffff', '#656565'],
    vmin=0,
    vmax=10,
    index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
)

def ReturnNumber(nums):
    str_nums = str(nums)
    return int(str(int(str_nums[-1]) + int(str_nums[-2]))[-1])

TAC = folium.GeoJson(
    data=gdf_TAC.to_json(),
    style_function = lambda feature:{
        "fillColor": colormap(ReturnNumber(feature['properties']['TAC'])),
        'fillOpacity': 0.7,
        "stroke": False
    },
    highlight_function = lambda feature:{
        "fillColor": colormap(ReturnNumber(feature['properties']['TAC'])),
        'fillOpacity': 0.8,
        'color': 'red',
        "stroke": True
    },
    name='TAC',
    show=True,
    tooltip = folium.features.GeoJsonTooltip(
        fields=['N03_001_x', 'TAC', 'samples'],
        aliases=['都道府県名', 'TAC', 'サンプル数']
    )
).add_to(map)

# TAC検索
plugins.Search(
    layer = TAC,
    geom_type = "Polygon",
    position = "topleft",
    placeholder = "TAC",
    search_label = "TAC",
    collapsed = False
).add_to(map)

# フルスクリーン
folium.plugins.Fullscreen(position = 'bottomright').add_to(map)

# レイヤーコントロール
folium.LayerControl().add_to(map)

# 現在値ボタン
folium.plugins.LocateControl(position = 'bottomright').add_to(map)

map.save('map_tac.html')
