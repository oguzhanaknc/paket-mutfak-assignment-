import plotly.graph_objects as go

circle_radius_mt = 1000

# define the custom marker symbol as a circle
circle_marker = dict(
    color='blue',
    opacity=0.5,
    size=circle_radius_mt,
    symbol='circle'
)

def visualizer(baskets):
    fig = go.Figure()

    # add marker
    for i,basket in enumerate(baskets):
        fig.add_trace(go.Scattermapbox(
                lat=[basket[0][0]],
                lon=[basket[0][1]],
                mode='markers',
                marker=circle_marker,
                text=f"SEPETNO#{i+1}",
                name=f"SEPETNO#{i+1}",
            ))
        for j,point in enumerate(basket):
            fig.add_trace(go.Scattermapbox(
                lat=[point[0]],
                lon=[point[1]],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color='red'
                ),
                text=f"item#{j+1}",
                name=f"item#{j+1}",
            ))
   
    # map settings
    fig.update_layout(
        title='Geocode Verileri',
        mapbox=go.layout.Mapbox(
            style="open-street-map",
            center=go.layout.mapbox.Center(
                lat=41.11138009478656,
                lon=29.020377292939678
            ),
            zoom=14
        )
    )

    fig.show()




