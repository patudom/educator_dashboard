import solara
from educator_dashboard.components.ClassPlot import ClassPlot
from educator_dashboard.components.TableDisplay import TableDisplay


@solara.component
def DataSummary(data = None, student_id = None, on_student_id = None):
    """
    Display a summary of the data
    """
    
    print('Displaying data summary')
    
    if data.value is None:
        return
    
    if on_student_id is None:
        on_student_id = student_id.set
    
    def on_plot_click(points):
        print("DataSummary: ClassPlot clicked")
        if points is not None:
            selected_index = points['points']['point_indexes'][0]
            on_student_id(data.value.iloc[selected_index].student_id)
        else:
            on_student_id(None)
    
    ClassPlot(data.value, on_click=on_plot_click, select_on = 'student_id', selected = student_id)
    

from math import nan
def get_slope(x, y):
    # slope through origin
    return nan if (sum(x**2) == 0) else (sum(x*y)/sum(x**2))
def slope2age(h0):
    return 977.79222 / h0 # age of universe in Gyr

@solara.component
def StudentData(dataframe = None, id_col = 'student_id',  sid = None, cols_to_display = None, on_sid = None, allow_id_set = True):
    """
    Display a single student's data
    """
    
    print('Displaying single students data')
    
    if sid.value is None:
        print("StudentData: no sid")
        return
    
    if dataframe.value is None:
        print("StudentData: no dataframe")
        return

    single_student_df = dataframe.value[dataframe.value[id_col] == sid.value]
    
    def on_value(value):
        print("StudentData: on_value: setting sid", value)
        sid.set(int(value))
        if on_sid is not None:
            on_sid(int(value))
    
    with solara.Column(gap="0px"):
        with solara.Columns([1,1]):
            with solara.Column():
                if allow_id_set:
                    # val = str(sid.value)
                    solara.InputText(label="Student ID",  value = str(sid), on_value=on_value)
                else:
                    solara.Markdown(f"**Student {sid}**")
            with solara.Column():
                #hubble's constant
                # age of universe
                h0 = get_slope(single_student_df['est_dist_value'], single_student_df['velocity_value'])
                age = slope2age(h0)
                solara.Markdown(f"**Hubble Constant**: {h0:.1f} km/s/Mpc")
                solara.Markdown(f"**Age of Universe**: {age:.1f} Gyr")
                
        
        if cols_to_display is None:
            cols_to_display = single_student_df.columns
        TableDisplay(single_student_df[cols_to_display])
