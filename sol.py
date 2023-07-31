import solara

from class_report import Roster
from typing import cast

from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go


@solara.component
def TableDisplay(*args, **kwargs):
    """
    Thin wrapper around solara.DataFrame
    """
    return solara.DataFrame(*args, **kwargs)

@solara.component
def StudentData(dataframe = None, id_col = 'student_id',  sid = None, cols_to_display = None, on_sid = None, allow_id_set = True):
    if sid is None:
        return
    
    if not isinstance(sid, solara.Reactive):
        sid = solara.use_reactive(sid)

    single_student_df = dataframe[dataframe[id_col] == sid.value]
    
    def on_value(value):
        sid.set(int(value))
        on_sid(int(value))
    
    with solara.Column(gap="0px"):
        if allow_id_set:
            solara.InputText(label="Student ID",  value = str(sid), on_value=on_value)
        else:
            solara.Markdown(f"**Student {sid}**")
        
        if cols_to_display is None:
            cols_to_display = single_student_df.columns
        TableDisplay(single_student_df[cols_to_display])

@solara.component
def ClassPlot(dataframe, 
            x_col = "est_dist_value", 
            y_col = "velocity_value", 
            label_col = "student_id", 
            xy_label = {"x":{'label': 'Distance', 'units': 'Mpc'}, "y":{'label': 'Velocity', 'units': 'km/s'}},
            on_click = None,
            select_on = None,
            selected = None
              ):
    
    if select_on is None:
        select_on = "student_id"
    
    selected = solara.use_reactive(selected)
    select_on = solara.use_reactive(select_on)
    
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
        
    fig = px.scatter(dataframe, x=x_col, y=y_col, custom_data = [label_col])
    fig.update_layout(modebar = config)


    xlabel = xy_label["x"]['label']+': %{x:f} ' + xy_label["x"]['units']
    ylabel = xy_label["y"]['label']+': %{y:f} ' + xy_label["y"]['units']
    hovertemplate = '<b>%{customdata[0]}</b><br>' + xlabel + '<br>' + ylabel
    
    fig.update_traces(hovertemplate=hovertemplate) 
    
    def click_action(points):
        selected_index = points['points']['point_indexes'][0]
        selected.set(dataframe.iloc[selected_index][select_on.value])
        if on_click is not None:
            on_click(points)
        
    
    
    
    if selected.value is not None:    
        stud_data = dataframe[dataframe[select_on.value] == selected.value]
        fig.add_trace(go.Scatter(x= stud_data[x_col], y= stud_data[y_col], mode = 'markers',
                                            customdata = [stud_data[label_col]],
                                            hovertemplate = hovertemplate,
                                            name = str(selected.value),
                                            marker_symbol = 'circle',   
                                            marker_size = 10,
                                            marker_color = 'red'))
    
    return solara.FigurePlotly(fig, on_click=click_action, )
        




class_id = solara.reactive() # add class id here
roster = solara.reactive(cast(Roster, None))
df = solara.reactive(cast(DataFrame, None))
data = solara.reactive(cast(DataFrame, None))

@solara.component
def SetClass(first_run = False):
    def on_value(value):
        class_id.set(int(value))
        print("setting class id", value)
        roster.set(Roster(int(value)))
        df.set(roster.value.short_report())
        data.set(DataFrame(roster.value.get_class_data()))
    
    if first_run:
        print("first run")
        on_value(class_id.value)
    
    solara.InputText(label="Class ID",  value = str(class_id), on_value=on_value)

@solara.component
def Dashboard(df, data):
    if df.value is None:
        print("no df")
        return
    
    student_id, set_student_id = solara.use_state(None)
    old_set_student_id = set_student_id
    def set_student_id(sid):
        print('setting student id',sid, type(sid))
        old_set_student_id(sid)
    
    
    def on_cell_click(column, row_index):   
        set_student_id(df.value.iloc[row_index].student_id)

    cell_actions = [solara.CellAction(name=None, icon="mdi-account-details",on_click=on_cell_click)]

    TableDisplay(df.value,items_per_page=len(df.value)//3,cell_actions = cell_actions)
    with solara.Card():
        for i in range(len(df.value)):
            student_id = int(df.value.iloc[i].student_id)
            studnt_name = df.value.iloc[i].username
            total_points = int(df.value.iloc[i].total_score)
            current_stage = int(df.value.iloc[i].max_stage_index)
            current_progress = df.value.iloc[i].progress.split('%')[0]
            if current_progress.isnumeric():
                current_progress = int(current_progress)
            else:
                current_progress = 100
            StudentProgress(student_id = student_id, student_name = studnt_name, total_points = total_points, number_of_stages = 6, current_stage = current_stage, current_stage_progress = current_progress)
    

    with solara.Row():
        
        def on_plot_click(points):
            print("plot clicked")
            if points is not None:
                selected_index = points['points']['point_indexes'][0]
                set_student_id(data.value.iloc[selected_index].student_id)
            else:
                set_student_id(None)
        

        ClassPlot(data.value, on_click=on_plot_click, select_on = 'student_id', selected = student_id)
        
        if student_id:
            with solara.Column():
                cols = ['student_id', 'velocity_value', 'est_dist_value', 'obs_wave_value', 'ang_size_value']
                StudentData(dataframe = data.value, id_col="student_id", sid = student_id, on_sid = set_student_id, cols_to_display = cols)
                



@solara.component_vue("MultiStepProgressBar.vue")
def MultiStepProgressBar(
    steps = None,
    currentStep = None,
    currentStepProgress = None,
    height = None,
    ): pass
    



@solara.component
def StudentProgress(student_id = None, 
                    student_name = None, 
                    total_points = None, 
                    number_of_stages = None,
                    current_stage = None,
                    current_stage_progress = None,
                    ):
    """
    The student progress should show
    student_id  student_name total_points progress_bar
    """
    with solara.Row():
        with solara.Columns([2,6]):
            solara.Markdown(f"{student_id} {student_name} {total_points}", style="font-size: 1.5em;")
            MultiStepProgressBar(steps=number_of_stages, currentStep=current_stage, currentStepProgress=current_stage_progress, height='4px')

    
    

@solara.component
def Page():
    first_run = solara.use_reactive(True)

    SetClass(first_run.value)
    first_run.set(False)
    
   
    Dashboard(df, data) 
    if df.value is None:
        solara.Markdown("No class selected")
    


# The following line is required only when running the code in a Jupyter notebook:
Page()