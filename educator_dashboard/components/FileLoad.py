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
            * You can load a single name file that includes students from multiple classes, and they will be applied when the relevant class is viewed. (If you use separate name files for each class, you will need to reload the file every time you toggle between classes).
        ''')
        if not load_complete.value:
            solara.FileDrop(
                on_file=on_file,
                lazy=False, # puts data in the [data] part of FileInfo
            )
        if load_complete.value and valid_file:
            solara.Button("Clear data", on_click=on_click)
        elif load_complete.value and not valid_file:
            solara.Error(msg, dense=True, outlined=True, icon='mdi-file-alert')
            solara.Button("Try another file", on_click=on_click)
            

def strip_non_alpha(string):
    return (''.join([c for c in str(string) if c.isalpha()])).lower()

def is_header_row(array):
    return all([strip_non_alpha(c).isalpha() for c in array])

def is_numeric_array(array):
    return all((str(val).isnumeric() for val in array))

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
        solara.Warning("Some cells in your csv file contain commas, possibly in the form 'last name, first name.' If student names do not look right, you may need to remove extra commas and reload the file.")
    bytes_data = re.sub(regex, '', bytes_data.decode('utf-8')).encode('utf-8')
    
    if filename.endswith('.csv'):
        # read in the table assuming it has no header row
        table = pd.read_csv(BytesIO(bytes_data), header=None, skip_blank_lines=True, quotechar='"', encoding='utf-8')
        # if the first row is a valid header row, read in the table again
        if is_header_row(table.iloc[0].to_numpy()) and use_first_row_as_header.value:
            table = pd.read_csv(BytesIO(bytes_data), header=0, skip_blank_lines=True, quotechar='"', encoding='utf-8')
            if not verify_table(table):
                solara.Warning("Let's double check the headers. Use the panel on the left to set the ID and Name columns", dense=True)
                use_first_row_as_header.set(False)
    else:
        ext = filename.split('.')[-1]
        solara.Error(f"The dashboard cannot read ${ext} files. Please convert your file to a CSV (comma-separate values file) and try again.")
        use_first_row_as_header.set(True)
        return
    
    do_on_table(table)
    
    if display:
        solara.DataFrame(table.head(5))
    use_first_row_as_header.set(True)


def validate_column_choices(table, id_col, name_col, id_validator = lambda x: (True, [])):
    if id_col == name_col:
        return False

    if id_col not in table.columns:
        return False

    if name_col not in table.columns:
        return False

    if is_numeric_array(table[id_col]):
        valid, _ = id_validator(table)
        if valid:
            pass
        else:
            return False
    else:
        return False

    return True


@solara.component
def SetColumns(table, fixed_table = None, table_set = None, id_validator = lambda x: (True, [])):
    
    student_id_column = solara.use_reactive('student_id')
    name_column = solara.use_reactive('name')
    table_set = solara.use_reactive(table_set)
    skip_setting = False
    fixed_table = solara.use_reactive(fixed_table)
    
    if table.value is None:
        fixed_table.set(None)
    
    

    if table.value is not None:

        cols = list(table.value.columns.to_numpy().astype(str))
        cols = [c.strip() for c in cols]
        table.value.columns = cols

        valid_id_cols = [c for c in cols if is_numeric_array(table.value[c])]
        
        if validate_column_choices(table.value, 'student_id', 'name', id_validator = id_validator):
            student_id_column.set('student_id')
            name_column.set('name')
            skip_setting = True
        
        elif 'student_id' in cols and 'name' in cols:
            solara.Error('`student_id` and `name` found, but not labeling the correct columns. Please select the correct columns', dense=True, outlined=True, icon='mdi-file-alert')
        
        if not skip_setting:
            
            with solara.Card():
                solara.Markdown("Please select the column that contains student ids.")
                solara.Select(label = 'Student ID column', values = valid_id_cols, value = student_id_column, dense=True, style="width: 40ch")
            
            with solara.Card():
                solara.Markdown("Please select the column that contains student names.")
                solara.Select(label = 'Student name column', values = cols, value = name_column, dense=True, style="width: 40ch")

        if validate_column_choices(table.value, student_id_column.value, name_column.value):
            df = table.value[[student_id_column.value, name_column.value]]
            df.columns = ['student_id', 'name']
            table_set.set(df is not None)
            fixed_table.set(df)
            if not skip_setting:
                solara.Markdown('Preview corrected table:')
                solara.DataFrame(df.head(5))
        else:
            solara.Error("Please select valid columns", dense=True, outlined=True)
            fixed_table.set(None)
            table_set.set(False)
            
    

