import solara

from class_report import Roster
from typing import cast

from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go

from components.ClassPlot import ClassPlot
from components.SetClass import SetClass
from components.TableDisplay import TableDisplay
from components.StudentProgress import StudentProgressTable


@solara.component
def StudentData(dataframe = None, id_col = 'student_id',  sid = None, cols_to_display = None, on_sid = None, allow_id_set = True):
    if sid is None:
        print("no sid")
        return

    single_student_df = dataframe.value[dataframe.value[id_col] == sid.value]
    
    def on_value(value):
        print("setting sid", value)
        sid.set(int(value))
        if on_sid is not None:
            on_sid(int(value))
    
    with solara.Column(gap="0px"):
        if allow_id_set:
            # val = str(sid.value)
            solara.InputText(label="Student ID",  value = str(sid), on_value=on_value)
        else:
            solara.Markdown(f"**Student {sid}**")
        
        if cols_to_display is None:
            cols_to_display = single_student_df.columns
        TableDisplay(single_student_df[cols_to_display])


@solara.component
def Dashboard(df, data):
    if df.value is None:
        solara.Markdown("No class selected", style="color: red; font-size: 2em" )
        return
    
    student_id = solara.use_reactive(None)
    
    
    def on_cell_click(column, row_index):   
        student_id.set(df.value.iloc[row_index].student_id)

    cell_actions = [solara.CellAction(name=None, icon="mdi-account-details",on_click=on_cell_click)]

    TableDisplay(df.value,items_per_page=len(df.value)//3,cell_actions = cell_actions)
    
    StudentProgressTable(df)

    with solara.Card(elevation=1):
        with solara.Row():
            
            def on_plot_click(points):
                print("plot clicked")
                if points is not None:
                    selected_index = points['points']['point_indexes'][0]
                    student_id.set(data.value.iloc[selected_index].student_id)
                else:
                    student_id.set(None)
            
            with solara.Columns([1,1]):
                ClassPlot(data.value, on_click=on_plot_click, select_on = 'student_id', selected = student_id)
            
                if student_id:
                    cols = ['student_id', 'velocity_value', 'est_dist_value', 'obs_wave_value', 'ang_size_value']
                    StudentData(dataframe = data, id_col="student_id", sid = student_id, cols_to_display = cols)
                    
