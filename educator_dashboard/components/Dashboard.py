import solara


from typing import cast

from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go

from .ClassProgress import ClassProgress
from .StudentProgress import StudentProgressTable
from .ResponsesComponents import StudentQuestionsSummary
from .ResponsesComponents import IndividualStudentResponses
from .StudentDataUpload import StudentNameUpload

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
def ShowReport(roster):
    if len(roster.value.roster) == 0:
        return
    dialog = rv.Dialog(
        v_slots = [{
            'name': 'activator',
            'variable': 'x',
            'children': rv.Btn(v_on='x.on', color='primary', dark=True, children=['Show Table'])
            
        }]
    )
    with dialog:
        solara.DataFrame(roster.value.short_report())

@solara.component
def Dashboard(roster, student_names = None): 
    
    if roster.value is None:
        return
    
    if len(roster.value.roster) == 0:
        solara.Markdown(f"There are no students in the class {roster.value.class_id}")
    
    student_id = solara.use_reactive(None)
    student_names = solara.use_reactive(student_names)
    old_set = student_id.set
    student_id.set = print_function_name(old_set)
    
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
    
    
    StudentNameUpload(roster, student_names)
    
    with solara.GridFixed(columns=1, row_gap='0px', justify_items='stretch', align_items='start'):
        ClassProgress(roster)
        ShowReport(roster)
        StudentProgressTable(roster, student_id = student_id, stage_labels = labels, height='30vh')
        
            

        with solara.lab.Tabs(vertical=True, align='right', dark=True):
            
            with solara.lab.Tab(label="Summary", icon_name="mdi-text-box-outline"):
                StudentQuestionsSummary(roster, student_id)
                
            with solara.lab.Tab(label="Per Student" if student_id.value is None else f"For Student {student_id.value}", icon_name="mdi-file-question-outline"):
                IndividualStudentResponses(roster, student_id)
        
            # with solara.lab.Tab("Student Data", icon_name="mdi-chart-scatter-plot"):
            #     StudentDataSummary(roster, student_id = student_id)