import solara

from .FileUpload import TableUpload, SetColumns, TableDisplay

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
        
        
    
    