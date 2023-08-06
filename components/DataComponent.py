import solara
from components.ClassPlot import ClassPlot
from components.TableDisplay import TableDisplay


@solara.component
def DataSummary(data = None, student_id = None, on_student_id = None):
    """
    Display a summary of the data
    """
    if data.value is None:
        return
    
    if on_student_id is None:
        on_student_id = student_id.set
    
    def on_plot_click(points):
        print("plot clicked")
        if points is not None:
            selected_index = points['points']['point_indexes'][0]
            on_student_id(data.value.iloc[selected_index].student_id)
        else:
            on_student_id(None)
    
    ClassPlot(data.value, on_click=on_plot_click, select_on = 'student_id', selected = student_id)
    



@solara.component
def StudentData(dataframe = None, id_col = 'student_id',  sid = None, cols_to_display = None, on_sid = None, allow_id_set = True):
    """
    Display a single student's data
    """
    if sid is None:
        print("no sid")
        return
    
    if dataframe is None:
        print("no dataframe")
        return

    single_student_df = dataframe.value[dataframe.value[id_col] == sid.value]
    
    def on_value(value):
        print("setting sid", value)
        sid.set(int(value))
        if on_sid is not None:
            on_sid(int(value))
    
    with solara.Column(gap="0px"):
        if allow_id_set:
            # val = str(sid.value)
            solara.InputText(label="Student ID",  value = str(sid), on_value=on_value)
        else:
            solara.Markdown(f"**Student {sid}**")
        
        if cols_to_display is None:
            cols_to_display = single_student_df.columns
        TableDisplay(single_student_df[cols_to_display])
