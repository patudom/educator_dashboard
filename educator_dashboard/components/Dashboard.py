import solara


from typing import cast

from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go

from .ClassProgress import ClassProgress
from .StudentProgress import StudentProgressTable
from .ResponsesComponents import StudentQuestionsSummary
from .ResponsesComponents import IndividualStudentResponses

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
def Dashboard(roster, student_names = None): 
    
    if roster.value is None:
        return
    
    # student_id = solara.use_reactive(None)
    student_names = solara.use_reactive(student_names)
    show_student_tab = solara.use_reactive(0)
    def on_sid_set(value):
        if value is not None:
            print(f"Setting student_id to {value}")
            show_student_tab.set(1)
    student_id = solara.use_reactive(None, on_change=print_function_name(on_sid_set))
    
    
    
    # a non-displaying component to 
    # make sure the student_id is valid
    initStudentID(student_id, roster)

    # ClassProgress(df, roster)
    labels = ['Stage 1: </br> Velocities', 
              'Stage 2: </br> Ang size Intro', 
              'Stage 3: </br> Angular Size',
              'Stage 4: </br> Find H0',
              'Stage 5: </br> Uncertainty',
              'Stage 6: </br> Professional Data'
              ]
    
    with solara.GridFixed(columns=1, row_gap='0px', justify_items='stretch', align_items='start'):
        with solara.Card():
            solara.Markdown (f"## Class Progress")
            ClassProgress(roster)
            StudentProgressTable(roster, student_id = student_id, stage_labels = labels, height='30vh')

        with solara.Card():
            solara.Markdown(f"##Student Responses and Data")

            # Heads up: Tabs are considered experimental in Solara and the API may change in the future
            with solara.lab.Tabs(vertical=True, align='right', dark=True, value = show_student_tab):
                
                with solara.lab.Tab(label="Class Summary", icon_name="mdi-text-box-outline", classes=["vertical-tabs"]):
                    StudentQuestionsSummary(roster, student_id)
                    
                with solara.lab.Tab(label="Student Responses" if student_id.value is None else f"Student {student_id.value}", classes=["vertical-tabs"]):
                    IndividualStudentResponses(roster, student_id)
            
                # with solara.lab.Tab("Student Data", icon_name="mdi-chart-scatter-plot"):
                #     StudentDataSummary(roster, student_id = student_id)