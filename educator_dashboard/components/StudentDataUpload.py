import solara

from .FileUpload import TableUpload, SetColumns, TableDisplay

import reacton.ipyvuetify as rv

import copy

@solara.component
def StudentDataUploadInterface(name_dataframe = None, on_upload = None):
    
    
    file_info = solara.use_reactive(None)
    has_header = solara.use_reactive(False)
    table = solara.use_reactive(None)
    
    file_uploaded = solara.use_reactive(False)

    with solara.Columns([1, 1]):
        with solara.Column():
            TableUpload(file_info, upload_complete = file_uploaded)
        with solara.Column(gap="5px"):
            solara.Checkbox(label = "Does the file have a header row? (Un)Check if the displayed table looks incorrect",
                    value=has_header,
                )
            TableDisplay(file_info, has_header, on_table = table.set)
    
    with solara.Div(style="border-top: 1px solid black; padding-top: 2rem"):
        SetColumns(table, fixed_table = name_dataframe)
        
        


@solara.component
def StudentNameUpload(roster = None, student_names = None, on_update = None):
    

    roster = solara.use_reactive(roster)
    student_names = solara.use_reactive(student_names)
    

    dialog = rv.Dialog(
        v_slots = [{
            'name': 'activator',
            'variable': 'x',
            'children': rv.Btn(v_on='x.on', color='primary', dark=True, children=['Upload Student Names File'])
            
        }]
    )
    
    with dialog:
        StudentDataUploadInterface(student_names)
        
    # need a copy in order to update
    r = copy.copy(roster.value)
    if student_names.value is not None:
        
        student_names_dict = {row['student_id']: row['name'] for _, row in student_names.value.iterrows()}
        roster.value.set_student_names(student_names_dict)
        roster.value.short_report(refresh = True)
        if on_update is not None:
            on_update(copy.copy(roster.value))
        else:
            roster.set(copy.copy(roster.value))
        student_names.set(None)
