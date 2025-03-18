import solara
from solara.lab import Tabs, Tab
from typing import Optional

from .ClassProgress import ClassProgress
from .StudentProgress import StudentProgressTable
from .ResponsesComponents import StudentQuestionsSummary
from .ResponsesComponents import IndividualStudentResponses
from .StudentDataLoad import StudentNameLoad
from .ReportDownload import DownloadReport


from ..logger_setup import logger
from ..class_report import Roster
from solara.reactive import Reactive

from solara.alias import rv
import pandas as pd

import inspect
def print_function_name(func):
    def wrapper(*args, **kwargs):
        calling_function_name = inspect.stack()[1][3]
        logger.debug(f"Calling  {func.__name__} from {calling_function_name}")
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
def Dashboard(roster: Reactive[Roster] | Roster, student_names = None, add_names = False): 
    logger.info(" ========= dashboard component =========")
    roster = solara.use_reactive(roster)
    are_names_set = solara.use_reactive(add_names)
    
    
    # student_id = solara.use_reactive(None)
    student_names = solara.use_reactive(student_names)
    # if 'cds-student-names' in solara.cache.storage:
    #     if class_id.value in solara.cache.storage['cds-student-names']:
    #         logger.debug("loading student names from cache")
    #         student_name_dataframe = pd.read_json(solara.cache.storage['cds-student-names'][class_id.value])
    #         try:
    #             student_names.set({row['student_id']: row['name'] for _, row in student_name_dataframe.iterrows()})
    #             are_names_set.set(True)
    #         except:
    #             pass
    #     else:
    #         logger.debug("no student names in cache")
    # else:
    #     logger.debug("no cache for student names")
    
    show_student_tab = solara.use_reactive(0)
    sub_tab_index = solara.use_reactive(0)
    def on_sid_set(value):
        if value is not None:
            logger.info(f"Setting student_id to {value}")
            show_student_tab.set(1)
    student_id = solara.use_reactive(None, on_change=print_function_name(on_sid_set))
    
    if roster.value is None:
        return
    
    if are_names_set.value:
        roster.value.set_student_names({row['student_id']: row['name'] for _, row in student_names.value.iterrows()})
        # roster.value.short_report(refresh = True)
        roster.value.refresh_data()
        # roster.set(roster.value)
    
    # a non-displaying component to 
    # make sure the student_id is valid
    initStudentID(student_id, roster)

    # ClassProgress(df, roster)
    labels = ['Stage 1: </br> Velocities', 
              'Stage 2: </br> Distance Intro', 
              'Stage 3: </br> Distances',
              'Stage 4: </br> Universe Age',
              'Stage 5: </br> Uncertainties',
              'Stage 6: </br> Professional Data'
              ]
    
    stage_titles = ['Velocities', 
              'Distance Intro', 
              'Distances',
              'Universe Age',
              'Uncertainties',
              'Professional Data'
              ]
    
    with solara.GridFixed(columns=1, row_gap='10px', justify_items='stretch', align_items='start'):
        with solara.Card(elevation=4):
            with solara.Row(classes=["align-center"]):
                solara.Markdown (f"## Class Progress")
                ClassProgress(roster)
                rv.Spacer(style_="flex-grow: 1;")
                # solara.Markdown (f"{student_names.value}")
                StudentNameLoad(roster, student_names, names_set=are_names_set)
                DownloadReport(roster) 
            StudentProgressTable(roster, student_id = student_id, stage_labels = labels, height='50vh')

        with solara.Card(elevation=4):
            solara.Markdown(f"##Student Responses and Data")

            # Heads up: Tabs are considered experimental in Solara and the API may change in the future
            with Tabs(vertical=True, align='right', dark=True, value = show_student_tab):
                
                with Tab(label="Class Summary", icon_name="mdi-text-box-outline", classes=["vertical-tabs"]):
                    StudentQuestionsSummary(roster, student_id, stage_labels = stage_titles, which_tab = sub_tab_index)
                    
                with Tab(label="Student Responses" if student_id.value is None else f"Student {student_id.value}", classes=["vertical-tabs"]):
                    IndividualStudentResponses(roster, student_id, stage_labels = stage_titles, which_tab = sub_tab_index)
            
                # with solara.lab.Tab("Student Data", icon_name="mdi-chart-scatter-plot"):
                #     StudentDataSummary(roster, student_id = student_id)
        # This is just so the "This website runs on Solara" credit doesn't land on top of the Student Response card
        solara.Markdown("   ")  
        solara.Markdown("   ")