
import solara
from pandas import DataFrame

from .MultiStepProgressBar import MultiStepProgressBar
from .TableFromRows import TableFromRows
from .ProgressRow import ProgressRow

@solara.component
def StudentProgressRow(student_id = None, 
                    student_name = None, 
                    total_points = None, 
                    number_of_stages = None,
                    current_stage = None,
                    current_stage_progress = None,
                    on_student_id = None
                    ):
    """
    The student progress should show
    student_id  student_name total_points progress_bar
    """


    student = {
        'id': student_id,
        'name': student_name,
        'total_points': total_points,
    }
    
    def on_row_click(event):
            print(event, student_id)
            on_student_id(student_id)
    
    ProgressRow(column_data=student, 
                on_selected=on_row_click,
                progress_bar=MultiStepProgressBar(steps=number_of_stages, 
                                                currentStep=current_stage, 
                                                currentStepProgress=current_stage_progress, 
                                                height='0.5em', gap="5px"))
 

@solara.component
def StudentProgressTable(progress_data, on_student_id =None):
    """
    progress_data should be either a dataframe or a dictionary
    this will work with reactive or non-reactive data
    
    If a dictionary it can be either a list of records
    or a record with a list of values for each key
    
    progress_data should have the following keys:
    student_id, username, total_score, max_stage_index, progress
    where progress is the progress of the max stage
    
    """
    
    if progress_data.value is None:
        return
    
    data = progress_data.value
    
    # make sure we have a dataframe
    if isinstance(data, dict):
        data = DataFrame(data)
    
    def on_student_id_wrapper(student_id):
        on_student_id(int(student_id))
    
    rows = []
    for i in range(len(data)):
        max_stage_progress = data['progress'][i].split('%')[0]
        if max_stage_progress.isnumeric():
            max_stage_progress = int(max_stage_progress)
        else:
            max_stage_progress = 100
        rows.append(
            StudentProgressRow(
                            student_id = str(data['student_id'][i]), 
                            student_name = data['username'][i],
                            total_points = str(data['total_score'][i]), 
                            number_of_stages = 6, 
                            current_stage = int(data['max_stage_index'][i]), 
                            current_stage_progress = max_stage_progress,
                            on_student_id = on_student_id_wrapper
                            ) 
        )
    
    with solara.Card():
        TableFromRows(headers=['Student ID', 'Student Name', 'Total Points', 'Progress'], 
                      rows=rows,
                      )
