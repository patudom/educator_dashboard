import solara
from solara.components.file_drop import FileInfo
from io import BytesIO

import pandas as pd

import re

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
            * You can load a single name file that includes students from multiple classes, and they will be applied when the relevant class is being viewed. (If you use separate name files for each class, you will need to reload the file every time you toggle between classes).
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

def strip_non_alpha(string):
    return (''.join([c for c in str(string) if c.isalpha()])).lower()

def is_header_row(array):
    return all([strip_non_alpha(c).isalpha() for c in array])

def verify_table(df):
    # check that the columns are 'student_id' and 'name'
    return ('student_id' in df.columns) and ('name' in df.columns)
    
@solara.component
def CSVFileInfoToTable(file_info, on_table = None, display = True):
    
    use_first_row_as_header = solara.use_reactive(True)
    
        
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
    # check for commas that are inbetween words enclosed in double quotes and remove that comma
    # using regex and string methods
    regex = r',(?!(?:[^"]*"[^"]*")*[^"]*$)'
    matches = re.findall(regex, bytes_data.decode('utf-8'))
    if len(matches) > 0:
        solara.Warning("We found some commas that are inbetween words enclosed in double quotes. Will attempt removal. If data appears mangled, please remove them manually.")
    bytes_data = re.sub(regex, '', bytes_data.decode('utf-8')).encode('utf-8')    
    
    if filename.endswith('.csv'):
        # read in the table assuming it has no header row
        table = pd.read_csv(BytesIO(bytes_data), header=None, skip_blank_lines=True, quotechar='"', encoding='utf-8')
        # if the first row is a valid header row, read in the table again
        if is_header_row(table.iloc[0].to_numpy()) and use_first_row_as_header.value:
            table = pd.read_csv(BytesIO(bytes_data), header=0, skip_blank_lines=True, quotechar='"', encoding='utf-8')
            if verify_table(table):
                solara.Success("It has a valid header row!", dense=True)
            else:
                solara.Warning("Let's double check the headers. Use the panel on the left to set the ID and Name columns", dense=True)
                use_first_row_as_header.set(False)
    else:
        ext = filename.split('.')[-1]
        solara.Error(f"The dashboard cannot read ${ext} files. Please convert your file to a CSV (comma-separate values file) and try again.")
        return
    
    if len(table.columns) != 2:
        solara.Error("Your table does not have exactly two columns. Please check your file for extra commas and try again.")
        return
    
    do_on_table(table)
    
    if display:
        solara.DataFrame(table.head(5))

@solara.component
def SetColumns(table, fixed_table = None, table_set = None):
    
    student_id_column = solara.use_reactive('student_id')
    name_column = solara.use_reactive('name')
    table_set = solara.use_reactive(table_set)
    
    if table.value is None:
        fixed_table.set(None)
    
    skip_setting = False

    if table.value is not None:

        cols = list(table.value.columns.to_numpy().astype(str))
        cols = [c.strip() for c in cols]
        table.value.columns = cols

        
        if ('student_id' in cols) and ('name' in cols):
            skip_setting = True
        
        if not skip_setting:
            
            if 'student_id' not in cols:
                if student_id_column.value not in cols:
                    solara.Markdown("File does not have a column with header `student_id`. < br> Please select the column that contains student ids")
                solara.Select(label = 'Student ID column', values = cols, value = student_id_column, dense=True, style="width: 30ch")
            if 'name' not in cols:
                if name_column.value not in cols:
                    solara.Markdown("File does not have a column with header 'name'. </br> Please select the column that contains student names")
                solara.Select(label = 'Student name column', values = cols, value = name_column, dense=True, style="width: 30ch")

        if student_id_column.value in cols and name_column.value in cols:
            df = table.value[[student_id_column.value, name_column.value]]
            df.columns = ['student_id', 'name']
            table_set.set(df is not None)
            fixed_table.set(df)
            
    

