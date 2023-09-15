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
            selected = solara.reactive(None),
            allow_click = True,
            subset = None,
            subset_label = None,
            subset_color='mediumpurple',
              ):
    
    
    print('Generating Class Plot')
    
    if select_on is None:
        select_on = "student_id"
    
    if dataframe is None:
        solara.Markdown("No data")
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
        solara.Markdown(f"**{x_col}** not in dataframe")
        return
    
    labels =  {x_col: "{label} ({units})".format(**xy_label['x']),  
               y_col: "{label} ({units})".format(**xy_label['y'])}
    fig = px.scatter(dataframe, x=x_col, y=y_col, custom_data = label_col, labels = labels)
    fig.update_traces(marker_color='grey')
    fig.update_layout(modebar = config, title="Class Hubble Diagram", xaxis_showgrid=False, yaxis_showgrid=False, plot_bgcolor="white")
    fig.update_xaxes(linecolor='black')
    fig.update_yaxes(linecolor='black')
    # add empty trace to show on legend
    fig.add_trace(go.Scatter(x=[None], y=[None], mode = 'markers', name = 'Full Class', marker_color = 'grey'))

    xlabel = xy_label["x"]['label']+': %{x:f} ' + xy_label["x"]['units']
    ylabel = xy_label["y"]['label']+': %{y:f} ' + xy_label["y"]['units']
    hovertemplate = '<b>%{customdata}</b><br>' + xlabel + '<br>' + ylabel
    
    fig.update_traces(hovertemplate=hovertemplate) 
    
    def click_action(points):
        if not allow_click:
            return
        selected_index = points['points']['point_indexes'][0]
        selected.set(dataframe.iloc[selected_index][select_on])
        if on_click is not None:
            on_click(points)
        
    
    if subset is not None:
        print('Adding seen trace')
        sub_data = dataframe[subset]
        hovertemplate = '<b>%{customdata}</b><br>' + xlabel + '<br>' + ylabel
        fig.add_trace(go.Scatter(x= sub_data[x_col], y= sub_data[y_col], mode = 'markers',
                                            customdata = sub_data[label_col],
                                            hovertemplate = hovertemplate,
                                            name = subset_label,
                                            marker_symbol = 'circle',   
                                            marker_size = 7,
                                            marker_color = subset_color))
        
    if selected.value is not None:    
        print('Adding student trace')
        stud_data = dataframe[dataframe[select_on] == str(selected.value)]

        hovertemplate = '<b>%{customdata}</b><br>' + xlabel + '<br>' + ylabel
        fig.add_trace(go.Scatter(x= stud_data[x_col], y= stud_data[y_col], mode = 'markers',
                                            customdata = stud_data[label_col],
                                            hovertemplate = hovertemplate,
                                            name = str(selected.value),
                                            marker_symbol = 'circle',   
                                            marker_size = 10,
                                            marker_color = 'red'))
    
    
    
    return solara.FigurePlotly(fig, on_click=click_action, )
        
