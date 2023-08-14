import solara


from typing import cast

from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go

from .StudentProgress import StudentProgressTable
from .ResponsesComponents import StudentQuestions
from .ResponsesComponents import IndividualStudentResponses
from .DataComponent import DataSummary
from .DataComponent import StudentData

@solara.component
def initStudentID(student_id, roster):
    if roster.value is not None:
        if len(roster.value.student_ids) > 0:
            if student_id.value not in roster.value.student_ids:
                student_id.set(None)
            return
    student_id.set(None)
    return 
        

@solara.component
def Dashboard(df, data, roster): 
    
    student_id = solara.use_reactive(None)
    
    # a non-displaying component to 
    # make sure the student_id is valid
    initStudentID(student_id, roster)
    

    def on_cell_click(column, row_index):   
        student_id.set(df.value.iloc[row_index].student_id)

    cell_actions = [solara.CellAction(name=None, icon="mdi-account-details",on_click=on_cell_click)]

    # TableDisplay(df.value,items_per_page=len(df.value)//3,cell_actions = cell_actions)

    with solara.Column():
        StudentProgressTable(df, on_student_id=student_id.set)
    
        solara.Markdown(f"**Student {student_id}**")
    
    with solara.lab.Tabs():
        
        with solara.lab.Tab("Student Question Summary"):
            StudentQuestions(roster, student_id)
            
        with solara.lab.Tab("Individual Student Questions"):
            IndividualStudentResponses(roster, student_id)
    
        with solara.lab.Tab("Student Data", style={"transition": "none"}):
                
            with solara.Columns([1,1]):
                with solara.Column():
                    DataSummary(data, student_id)
                
                with solara.Column():
                    cols = ['student_id', 'galaxy_id','velocity_value', 'est_dist_value', 'obs_wave_value', 'ang_size_value']
                    StudentData(dataframe = data, id_col="student_id", sid = student_id, cols_to_display = cols)
                        
