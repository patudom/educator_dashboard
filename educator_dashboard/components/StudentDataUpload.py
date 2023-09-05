import solara

from .FileUpload import TableUpload, SetColumns, TableDisplay

@solara.component
def StudentDataUploadInterface(name_dataframe = None, on_upload = None):
    
    
    file_info = solara.use_reactive(None)
    has_header = solara.use_reactive(False)
    table = solara.use_reactive(None)
    

    with solara.Columns([1, 1]):
        with solara.Column():
            TableUpload(file_info)
            SetColumns(table, out = name_dataframe)
        with solara.Column(gap="5px"):
            if file_info.value is not None:
                solara.Checkbox(label = "Does the file have a header row? (Un)Check if the displayed table looks incorrect",
                        value=has_header,
                    )
                TableDisplay(file_info, has_header, on_table = table.set)
        
        
    
    