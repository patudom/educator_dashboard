import solara

import plotly.express as px
import plotly.graph_objects as go

from pandas import DataFrame

@solara.component
def ClassPlot(dataframe, 
            x_col = "est_dist_value", 
            y_col = "velocity_value", 
            label_col = "student_id", 
            xy_label = {"x":{'label': 'Distance', 'units': 'Mpc'}, "y":{'label': 'Velocity', 'units': 'km/s'}},
            on_click = None,
            select_on = None,
            selected = solara.reactive(None)
              ):
    
    
    print('Generating Class Plot')
    
    if select_on is None:
        select_on = "student_id"
    
    if dataframe is None:
        return
    
    config = {
            'remove': [
                'zoom2d', 
                'pan2d', 
                'lasso2d', 
                'zoomIn2d', 
                'zoomOut2d',
                'autoscale'
            ]
        }
    
    
    if x_col not in dataframe.columns:
        print(f"ClassPlot: {x_col} not in dataframe")
        return
    
    fig = px.scatter(dataframe, x=x_col, y=y_col, custom_data = label_col)
    fig.update_layout(modebar = config)


    xlabel = xy_label["x"]['label']+': %{x:f} ' + xy_label["x"]['units']
    ylabel = xy_label["y"]['label']+': %{y:f} ' + xy_label["y"]['units']
    hovertemplate = '<b>%{customdata}</b><br>' + xlabel + '<br>' + ylabel
    
    fig.update_traces(hovertemplate=hovertemplate) 
    
    def click_action(points):
        selected_index = points['points']['point_indexes'][0]
        selected.set(dataframe.iloc[selected_index][select_on])
        if on_click is not None:
            on_click(points)
        
    
    if selected.value is not None:    
        print('Adding trace')
        stud_data = dataframe[dataframe[select_on] == selected.value]
        hovertemplate = '<b>%{customdata}</b><br>' + xlabel + '<br>' + ylabel
        fig.add_trace(go.Scatter(x= stud_data[x_col], y= stud_data[y_col], mode = 'markers',
                                            customdata = stud_data[label_col],
                                            hovertemplate = hovertemplate,
                                            name = str(selected.value),
                                            marker_symbol = 'circle',   
                                            marker_size = 10,
                                            marker_color = 'red'))
    
    return solara.FigurePlotly(fig, on_click=click_action, )
        
