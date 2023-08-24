import solara


from typing import cast

from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go

from .StudentProgress import StudentProgressTable
from .ResponsesComponents import StudentQuestionsSummary
from .ResponsesComponents import IndividualStudentResponses
from .DataComponent import DataSummary
from .DataComponent import StudentData

from solara.alias import rv

import inspect
def print_function_name(func):
    def wrapper(*args, **kwargs):
        calling_function_name = inspect.stack()[1][3]
        print(f"Calling  {func.__name__} from {calling_function_name}")
        return func(*args, **kwargs)
    return wrapper

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
    old_set = student_id.set
    student_id.set = print_function_name(old_set)
    
    # a non-displaying component to 
    # make sure the student_id is valid
    initStudentID(student_id, roster)
    

    def on_cell_click(column, row_index):   
        student_id.set(df.value.iloc[row_index].student_id)

    cell_actions = [solara.CellAction(name=None, icon="mdi-account-details",on_click=on_cell_click)]

    # TableDisplay(df.value,items_per_page=len(df.value)//3,cell_actions = cell_actions)


    StudentProgressTable(df, student_id = student_id)
    
    
    # solara.Markdown(f"**Currently selected student**: {student_id}")
    def safe_set(x):
        try:
            student_id.set(int(x))
        except:
            student_id.set(None)
    
   
    rv.Select(label = 'Select Student', 
            v_model = student_id.value, 
            on_v_model=safe_set,
            items = roster.value.student_ids, 
            rounded=True,
            outlined=True,
            dense=True,
            class_="mx-a student-select",
        )

        
    with solara.Card():
        with solara.lab.Tabs(vertical=True, align='right', dark=True):
            
            with solara.lab.Tab(label="Summary", icon_name="mdi-text-box-outline"):
                StudentQuestionsSummary(roster, student_id)
                
            with solara.lab.Tab(label="Individual Qs", icon_name="mdi-file-question-outline"):
                IndividualStudentResponses(roster, student_id)
        
            with solara.lab.Tab("Student Data", icon_name="mdi-chart-scatter-plot"):
                    
                with solara.Columns([1,1]):
                    with solara.Column():
                        DataSummary(data, student_id)
                    
                    with solara.Column():
                        cols = ['student_id', 'galaxy_id','velocity_value', 'est_dist_value', 'obs_wave_value', 'ang_size_value']
                        StudentData(dataframe = data, id_col="student_id", sid = student_id, cols_to_display = cols)
                            
