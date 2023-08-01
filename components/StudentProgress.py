
import solara

from components.MultiStepProgressBar import MultiStepProgressBar


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
        'steps': number_of_stages,
        'currentStep': current_stage,
        'currentStepProgress': current_stage_progress,
    }
    
    ProgressRow(student=student, 
                progress_bar=MultiStepProgressBar(steps=number_of_stages, 
                                                currentStep=current_stage, 
                                                currentStepProgress=current_stage_progress, 
                                                height='4px'))
    
    

@solara.component
def StudentProgressTable(df):
    with solara.Card():
        for i in range(len(df.value)):
            current_progress = df.value.iloc[i].progress.split('%')[0]
            if current_progress.isnumeric():
                current_progress = int(current_progress)
            else:
                current_progress = 100
            StudentProgressRow(student_id = int(df.value.iloc[i].student_id), 
                            student_name = df.value.iloc[i].username, 
                            total_points = int(df.value.iloc[i].total_score), 
                            number_of_stages = 6, 
                            current_stage = int(df.value.iloc[i].max_stage_index), 
                            current_stage_progress = current_progress
                            )
    
