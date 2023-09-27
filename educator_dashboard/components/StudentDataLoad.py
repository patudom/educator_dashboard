import solara

from .FileLoad import TableLoad, SetColumns, TableDisplay

import reacton.ipyvuetify as rv

import copy

@solara.component
def StudentDataLoadInterface(name_dataframe = None, on_load = None, table_set = None):
    
    
    file_info = solara.use_reactive(None)
    has_header = solara.use_reactive(True)
    table = solara.use_reactive(None)
    table_set = solara.use_reactive(table_set)
    
    def on_clear(value):
        if not value:
            table.set(None)
            table_set.set(False)
    
    file_loaded = solara.use_reactive(False, on_change = on_clear)

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
        SetColumns(table, fixed_table = name_dataframe, table_set = table_set)
        



@solara.component
def StudentLoadDialog(student_names = None, student_names_set = None, dialog_open = False):
    
    student_names = solara.use_reactive(student_names)
    student_names_set = solara.use_reactive(student_names_set)
    
    dialog_open = solara.use_reactive(dialog_open)
      
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
            StudentDataLoadInterface(student_names, table_set = student_names_set)
            if student_names_set.value:
                solara.Success("Successfully updated student names!", dense=True, outlined=True)
            with solara.CardActions():
                solara.Button(icon_name="mdi-close-circle",label = "Close", on_click = lambda: dialog_open.set(False), text=True, outlined=True)



@solara.component
def StudentNameLoad(roster, student_names = None, names_set = None, on_update = None):
    print("student name load component")
    roster = solara.use_reactive(roster)
    student_names = solara.use_reactive(student_names)
    student_names_set = solara.use_reactive(names_set)
    
    StudentLoadDialog(student_names, student_names_set = student_names_set)
    r = copy.copy(roster.value)
    if student_names.value is not None:
        print("updating student names")
        student_names_dict = {row['student_id']: row['name'] for _, row in student_names.value.iterrows()}
        r.set_student_names(student_names_dict)
        r.short_report(refresh = True)
        roster.set(r)
        student_names_set.set(True)
        on_update(student_names.value)
        student_names.set(None)
