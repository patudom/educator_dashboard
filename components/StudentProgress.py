
import solara
from pandas import DataFrame

from components.MultiStepProgressBar import MultiStepProgressBar
from components.TableFromRows import TableFromRows


@solara.component_vue('ProgressRow.vue')
def ProgressRow(student=None, progress_bar = None):
    pass

@solara.component
def StudentProgressRow(student_id = None, 
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


    student = {
        'id': student_id,
        'name': student_name,
        'total_points': total_points,
    }
    
    ProgressRow(student=student, 
                progress_bar=MultiStepProgressBar(steps=number_of_stages, 
                                                currentStep=current_stage, 
                                                currentStepProgress=current_stage_progress, 
                                                height='0.5em', gap="5px"))
 

@solara.component
def StudentProgressTable(progress_data):
    """
    progress_data should be either a dataframe or a dictionary
    this will work with reactive or non-reactive data
    
    If a dictionary it can be either a list of records
    or a record with a list of values for each key
    """
    
    if progress_data.value is None:
        return
    
    data = progress_data.value
    
    # make sure we have a dataframe
    if isinstance(data, dict):
        data = DataFrame(data)
    
    rows = []
    for i in range(len(data)):
        current_progress = data['progress'][i].split('%')[0]
        if current_progress.isnumeric():
            current_progress = int(current_progress)
        else:
            current_progress = 100
        rows.append(
            StudentProgressRow(
                            student_id = str(data['student_id'][i]), 
                            student_name = data['username'][i],
                            total_points = str(data['total_score'][i]), 
                            number_of_stages = 6, 
                            current_stage = int(data['max_stage_index'][i]), 
                            current_stage_progress = current_progress
                            )
        )
    with solara.Card():
        TableFromRows(headers=['Student ID', 'Student Name', 'Total Points', 'Progress'], 
                      rows=rows)
