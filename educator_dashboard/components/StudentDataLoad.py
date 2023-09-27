import solara

from .FileLoad import TableLoad, SetColumns, TableDisplay

import reacton.ipyvuetify as rv

import copy

@solara.component
def StudentDataLoadInterface(name_dataframe = None, on_load = None):
    
    
    file_info = solara.use_reactive(None)
    has_header = solara.use_reactive(True)
    table = solara.use_reactive(None)
    
    file_loaded = solara.use_reactive(False)

    with solara.Columns([1, 1]):
        with solara.Column():
            TableLoad(file_info, load_complete = file_loaded)
        with solara.Column(gap="5px"):
            rv.Checkbox(v_model = has_header.value, 
                        on_v_model = has_header.set,
                        v_slots=[{
                            'name': 'label',
                            'children': [solara.Markdown('Does the file have a header row? <br> (Un/check if unsure. First row will be used as header if checked.)')]
                        }]
                        )
            TableDisplay(file_info, has_header, on_table = table.set)
    
    with solara.Div():
        SetColumns(table, fixed_table = name_dataframe)
        



@solara.component
def StudentNameLoad(roster = None, student_names = None, on_update = None):
    

    roster = solara.use_reactive(roster)
    student_names = solara.use_reactive(student_names)
    student_names_set = solara.use_reactive(False)
    
    dialog_open = solara.use_reactive(False)
      
    dialog = rv.Dialog(
        v_model = dialog_open.value,
        on_v_model=dialog_open.set,
        v_slots = [{
            'name': 'activator',
            'variable': 'dummy_var',
            'children': 
                solara.Tooltip(tooltip="Use local csv file to convert IDs to names", 
                    children = [solara.Button(label = "ID → Name", icon_name='mdi-google-spreadsheet', on_click = lambda: dialog_open.set(True), classes=["my-buttons"])]
                )
        }]
    )
    
    with dialog:
        with solara.Card():
            StudentDataLoadInterface(student_names)
            if student_names_set.value:
                solara.Success("Successfully updated student names!", dense=True, outlined=True)
            with solara.CardActions():
                solara.Button(icon_name="mdi-close-circle",label = "Close", on_click = lambda: dialog_open.set(False), text=True, outlined=True)
        
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
        student_names_set.set(True)
        student_names.set(None)
