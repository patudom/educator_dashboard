import solara

from .FileLoad import TableLoad, SetColumns, CSVFileInfoToTable

import reacton.ipyvuetify as rv

import copy

@solara.component
def StudentDataLoadInterface(name_dataframe = None, on_load = None, table_set = None, id_validator = lambda x: (True, [])):
    
    
    file_info = solara.use_reactive(None)
    table = solara.use_reactive(None)
    table_set = solara.use_reactive(table_set)
    
    def on_clear(value):
        if not value:
            table.set(None)
            table_set.set(False)
            name_dataframe.set(None)
    
    file_loaded = solara.use_reactive(False, on_change = on_clear)

    with solara.Row():
        with solara.Column():
            TableLoad(file_info, load_complete = file_loaded)
    with solara.Row(gap="10px"):
        with solara.Div():
            SetColumns(table, fixed_table = name_dataframe, table_set = table_set, id_validator=id_validator)
        CSVFileInfoToTable(file_info, on_table = table.set)
            
            # with solara.Column():
            #     if table.value is not None:
            #         solara.Markdown("Does your table look okay? If data appears in your header row, press the button below")
            #         rv.Checkbox(v_model = has_header.value, 
            #                 on_v_model = has_header.set,
            #                 label = f'Header row is {"" if has_header.value else "not"} correct'
            #                 )   

@solara.component
def StudentLoadDialog(student_names = None, student_names_set = None, dialog_open = False, no_dialog = False, validator = lambda x: (True, [])):
    
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
    comp = dialog if not no_dialog else solara.Div()
    with comp:
        with solara.Card():
            StudentDataLoadInterface(student_names, table_set = student_names_set, id_validator = validator)
            if student_names_set.value:
                valid, missing = validator(student_names.value)
                if not valid:
                    solara.Error(f"Some students ({missing}) in the loaded class are not present in the loaded table. You may still proceed, but their names will not be loaded", dense=True, outlined=True)
                else:
                    solara.Success("Successfully updated student names.", dense=True, outlined=True)
            with solara.CardActions():
                solara.Button(icon_name="mdi-close-circle",label = "Close", on_click = lambda: dialog_open.set(False), text=True, outlined=True, classes=["dialog-button"])



@solara.component
def StudentNameLoad(roster, student_names = None, names_set = None, on_update = None):
    print("student name load component")
    roster = solara.use_reactive(roster)
    student_names = solara.use_reactive(student_names)
    student_names_set = solara.use_reactive(names_set)
    
    def validator(table, id_col = 'student_id'):
        if table is None:
            return False, []
        # check all roster sids are in the loaded table
        sids = table[id_col].tolist()
        roster_ids = roster.value.student_ids
        present = [(rid in sids) for rid in roster_ids]
        # get the missing roster_ids
        missing = [rid for rid, p in zip(roster_ids, present) if not p]
        return all(present), missing
    
    
    StudentLoadDialog(roster, student_names, student_names_set = student_names_set, validator = validator)
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
