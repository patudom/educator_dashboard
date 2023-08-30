import solara


from typing import cast

from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go

from .ClassProgress import ClassProgress
from .StudentProgress import StudentProgressTable
from .ResponsesComponents import StudentQuestionsSummary
from .ResponsesComponents import IndividualStudentResponses
from .DataComponent import DataSummary
from .DataComponent import StudentData
from .DataComponent import StudentDataSummary

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
def Dashboard(roster): 
    
    if len(roster.value.roster) == 0:
        solara.Markdown(f"There are no students in the class {roster.value.class_id}")
    
    student_id = solara.use_reactive(None)
    old_set = student_id.set
    student_id.set = print_function_name(old_set)
    
    # a non-displaying component to 
    # make sure the student_id is valid
    initStudentID(student_id, roster)
    

    # ClassProgress(df, roster)
    StudentProgressTable(roster, student_id = student_id)
    
        
    with solara.Card():
        with solara.lab.Tabs(vertical=True, align='right', dark=True):
            
            with solara.lab.Tab(label="Summary", icon_name="mdi-text-box-outline"):
                StudentQuestionsSummary(roster, student_id)
                
            with solara.lab.Tab(label="Per Student", icon_name="mdi-file-question-outline"):
                IndividualStudentResponses(roster, student_id)
        
            with solara.lab.Tab("Student Data", icon_name="mdi-chart-scatter-plot"):
                StudentDataSummary(roster, student_id = student_id)