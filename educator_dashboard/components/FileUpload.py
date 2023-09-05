import solara
from solara.components.file_drop import FileInfo
from io import BytesIO

import pandas as pd


@solara.component
def TableUpload(file_info = None, upload_complete = None, allow_excel = False):
    
    if upload_complete is None:
        return
    
    valid_file, set_valid_file = solara.use_state(False)
    
    def on_file(file: FileInfo):
        filename = file['name']
        
        if filename.endswith('.csv') or (allow_excel and (filename.endswith('.xlsx') or filename.endswith('.xls'))):
            file_info.set(file)
            upload_complete.set(True)
            set_valid_file(True)
        else:
            solara.Markdown(f"File type {filename.split('.')[-1]} not supported. Please upload a .csv or .xlsx file")
            return

    if not upload_complete.value:
        solara.FileDrop(
            label="Drag and drop a file (CSV or Excel) containing a student_id and name column. Names should NOT include commas (,) if using a CSV file",
            on_file=on_file,
            lazy=False, # puts data in the [data] part of FileInfo
        )
    else:
        def on_click():
            file_info.set(None)
            upload_complete.set(False)
        if valid_file:
            solara.Markdown("File uploaded successfully")
            solara.Button(icon_name = 'mdi-file-upload', label = "Upload another file", on_click = on_click)
        else:
            solara.Markdown("File upload failed. Please try again using a CSV file. ")


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
def SetColumns(table, out = None):
    
    if table.value is not None:

        #flexibly check for student_id and name columns
        cols = list(table.value.columns.to_numpy().astype(str))
        student_id_column = solara.use_reactive('student_id')
        name_column = solara.use_reactive('name')
    

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
            out.set(df)

