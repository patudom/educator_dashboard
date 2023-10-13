
import solara
from pandas import DataFrame

from .TableFromRows import TableFromRows
from .ProgressRow import ProgressRow

@solara.component
def StudentProgressRow(progress,
                    on_selected_id = None,
                    selected_id = None
                    ):
    """
    progress should be a dictionary with the following keys:
    student_id, student_name, total_points, number_of_stages, current_stage, current_stage_progress

    """
    
    
    student_id = progress['student_id']
    
    if student_id is None:
        selected = solara.use_reactive(False)
    elif selected_id is None:
        selected_id = solara.use_reactive(None)
    else:
        selected = solara.use_reactive(str(selected_id.value) == str(int(student_id)))

    student_data = {
        'ID': progress['student_id'],
        'Name': progress['student_name'],
        'Total Points': progress['total_points'],
        'Progress': f"{progress['percent_complete']}%"
    }
    
    def on_row_click(event):
            selected.set(event)

            if on_selected_id is None:
                selected_id.set(int(student_id) if event else None)
            else:
                on_selected_id(int(student_id) if event else None)

    
    ProgressRow(column_data=student_data, 
                selected = selected.value, #str(selected_id.value) == str(student_id),
                on_selected=on_row_click,
                steps=progress['number_of_stages'], 
                currentStep=progress['current_stage'], 
                currentStepProgress=progress['current_stage_progress'], 
                height='100%', gap="5px")


@solara.component
def StudentProgressTable(roster = None, 
                         progress_data = None, 
                         student_id = None, 
                         on_student_id = None, 
                         headers = None, 
                         stage_labels = [],
                         height = '100%'
                         ):
    """
    progress_data should be either a dataframe or a dictionary
    this will work with reactive or non-reactive data
    
    If a dictionary it can be either a list of records
    or a record with a list of values for each key
    
    progress_data should have the following keys:
    student_id, username, total_score, max_stage_index, progress
    where progress is the progress of the max stage
    
    """
    
    roster = solara.use_reactive(roster)
    data = roster.value.short_report()
    
    if data is None:
        return solara.Error(label="No data available. Please contact the CosmicDS team for help.", outlined=True, text = True)
    
    
    # make sure we have a dataframe
    if isinstance(data, dict):
        data = DataFrame(data)
    

    def on_student_id_wrapper(value):
        setfunc = on_student_id or student_id.set
        
        if value is None:
            setfunc(None)
        else:
            setfunc(int(value))

    

    if headers is None:
        headers = ['', 'Student<br>ID', 'Student<br>Name', 'Points/<br>available', 'Progress<br>(%)'] + stage_labels
    with TableFromRows(headers=headers, table_height=height):
        for i in range(len(data)):
            max_stage_progress = data['progress'][i].split('%')[0]
            if max_stage_progress.isnumeric():
                max_stage_progress = int(max_stage_progress)
            else:
                max_stage_progress = 100
            
            # set up dictionary with progress
            student_progress = {
                'student_id': str(data['student_id'][i]),
                'student_name': data['name'][i] if 'name' in data.columns else data['username'][i],
                'total_points': f"{data['total_score'][i]}/{data['out_of_possible'][i]}",
                'number_of_stages': 6,
                'current_stage': int(data['max_stage_index'][i]),
                'current_stage_progress': max_stage_progress,
                'percent_complete': data['percent_story_complete'][i]
            }

            StudentProgressRow(progress = student_progress,
                                selected_id = student_id,
                                on_selected_id = on_student_id_wrapper,
                                ) 

    
    