import solara
from solara.components.file_drop import FileInfo
from io import BytesIO

import pandas as pd


@solara.component
def TableLoad(file_info = None, load_complete = None, allow_excel = False):
    
    
    file_info = solara.use_reactive(file_info)
    load_complete = solara.use_reactive(load_complete)
    
    valid_file, set_valid_file = solara.use_state(True)
    msg, set_msg = solara.use_state("")
    
    def on_file(file: FileInfo):
        filename = file['name']
        
        isCSV = filename.endswith('.csv')
        isExcel = filename.endswith('.xlsx') or filename.endswith('.xls')

        if isCSV or (isExcel and allow_excel):
            file_info.set(file)
            set_valid_file(True)
            set_msg(f"Successfully read in {filename}!")
        else:
            set_valid_file(False)
            set_msg(f"Failed to read {filename}. Please select a valid CSV file.")
        
        load_complete.set(True)
    
    def on_click():
        file_info.set(None)
        load_complete.set(False)
        set_msg("")
    
    with solara.Div():
        solara.Markdown(r'''
            Read in a local CSV (comma-separated value) file containing student IDs and names to display names in the dashboard.
                        
            * Include a header row with column names 'student_id' and 'name'. 
            * To protect student privacy, this information remains on your computer and will NOT be uploaded to CosmicDS servers.
        ''')
        if not load_complete.value:
            solara.FileDrop(
                on_file=on_file,
                lazy=False, # puts data in the [data] part of FileInfo
            )
        if load_complete.value and valid_file:
            solara.Success(msg, dense=True, outlined=True, icon='mdi-file-check')
        elif load_complete.value and not valid_file:
            solara.Error(msg, dense=True, outlined=True, icon='mdi-file-alert')
        
        solara.Button("Clear", on_click=on_click, disabled=not load_complete.value)

    
    
    
@solara.component
def TableDisplay(file_info, has_header = False, on_table = None):
    
    if isinstance(file_info, solara.Reactive):
        file_info = file_info.value
    
    if isinstance(on_table, solara.Reactive):
        do_on_table = on_table.set
    else:
        do_on_table = on_table
    
    if file_info is None:
        return
    
    filename = file_info['name']
    bytes_data = file_info['data']
    
    if filename.endswith('.csv'):
        try:
            table = pd.read_csv(BytesIO(bytes_data), header=0 if has_header.value else None, skip_blank_lines=True)
        except pd.errors.ParserError:
            has_header.set(True)
            table = pd.read_csv(BytesIO(bytes_data), header=0 if has_header.value else None, skip_blank_lines=True)
        
        table.columns = [f"Col{i}" if str(c).isdigit() else c for i,c in enumerate(table.columns)]
    else:
        table = pd.read_excel(BytesIO(bytes_data))
    
    do_on_table(table)
    
    solara.DataFrame(table.head(5))

@solara.component
def SetColumns(table, fixed_table = None, table_set = None):
    
    student_id_column = solara.use_reactive('student_id')
    name_column = solara.use_reactive('name')
    table_set = solara.use_reactive(table_set)
    
    if table.value is None:
        fixed_table.set(None)
        

    if table.value is not None:

        cols = list(table.value.columns.to_numpy().astype(str))
        cols = [c.strip() for c in cols]
        table.value.columns = cols


        if 'student_id' not in cols:
            if student_id_column.value not in cols:
                solara.Markdown("File does not have a column named 'student_id'. Please select the column that contains student ids")
            solara.Select(label = 'Select student ID column', values = cols, value = student_id_column, dense=True, style="width: 30ch")
        if 'name' not in cols:
            if name_column.value not in cols:
                solara.Markdown("File does not have a column named 'name'. Please select the column that contains student names")
            solara.Select(label = 'Select student name column', values = cols, value = name_column, dense=True, style="width: 30ch")

        if student_id_column.value in cols and name_column.value in cols:
            df = table.value[[student_id_column.value, name_column.value]]
            df.columns = ['student_id', 'name']
            table_set.set(df is not None)
            fixed_table.set(df)
            
    

