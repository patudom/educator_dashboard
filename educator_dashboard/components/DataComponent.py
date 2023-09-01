import solara
from .ClassPlot import ClassPlot
from .TableDisplay import TableDisplay
from pandas import DataFrame
import plotly.express as px

from numpy import around
from math import ceil, floor



@solara.component
def DataSummary(data = None, student_id = None, on_student_id = None, allow_click = True):
    """
    Display a summary of the data
    """
    
    print('Displaying data summary')
    
    if isinstance(data, solara.Reactive):
        data = data.value
        
    if data is None:
        return
    
    if not isinstance(student_id, solara.Reactive):
        student_id = solara.use_reactive(student_id)
    
    if on_student_id is None:
        on_student_id = student_id.set
    
    def on_plot_click(points):
        print("DataSummary: ClassPlot clicked")
        if points is not None:
            selected_index = points['points']['point_indexes'][0]
            on_student_id(data.iloc[selected_index].student_id)
        else:
            on_student_id(None)
    
    if allow_click:
        with solara.Column(gap="0px"):
            solara.Markdown(f"Click on a point to show all data for that student", style={'font-size': 'small'})
            ClassPlot(data, on_click=on_plot_click, select_on = 'student_id', selected = student_id, allow_click=allow_click)
    else:
        with solara.Column():
            ClassPlot(data, select_on = 'student_id', selected = student_id, allow_click = allow_click)
    

from math import nan
def get_slope(x, y):
    # slope through origin
    return nan if (sum(x**2) == 0) else (sum(x*y)/sum(x**2))
def slope2age(h0):
    return 977.79222 / h0 # age of universe in Gyr


@solara.component
def AgeHoHistogram(data, age_col = 'age', h0_col = 'h0', which = 'age'):
    
    xmin, xmax = floor(data[age_col].min()), ceil(data[age_col].max())
    categories = list(range(xmin, xmax+1))
    fig = px.histogram(data_frame = data, x = which, labels={age_col:'Age of Universe (Gyr)'}, category_orders={age_col: categories})
    fig.update_xaxes(type='category')
    fig.update_layout(showlegend=False, title_text='Class Age Distribution')
    # show ticks every 1
    # fig.update_xaxes(dtick=1)

    solara.FigurePlotly(fig)
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
                # if allow_id_set:
                #     # val = str(sid.value)
                #     solara.InputText(label="Student ID",  value = str(sid), on_value=on_value)
                # else:
                #     solara.Markdown(f"**Student {sid}**")
            # with solara.Column():
                #hubble's constant
                # age of universe
                h0 = get_slope(single_student_df['est_dist_value'], single_student_df['velocity_value'])
                age = slope2age(h0)
                solara.Markdown(f"**Hubble Constant**: {h0:.1f} km/s/Mpc")
                solara.Markdown(f"**Age of Universe**: {age:.1f} Gyr")
                
        
        if cols_to_display is None:
            cols_to_display = single_student_df.columns
        TableDisplay(single_student_df[cols_to_display])


@solara.component
def StudentDataSummary(roster = None, student_id = None, allow_sid_set = True):
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return

    dataframe = DataFrame(roster.get_class_data())
    if dataframe is None:
        return
    
    if not isinstance(dataframe, solara.Reactive):
        dataframe = solara.use_reactive(dataframe)
    
    if not isinstance(student_id, solara.Reactive):
        student_id = solara.use_reactive(student_id)
    
    with solara.Columns([1,1]):
        with solara.Column():
            DataSummary(dataframe, student_id, allow_click=allow_sid_set)
        
        with solara.Column():
            cols = ['student_id', 'galaxy_id','velocity_value', 'est_dist_value', 'obs_wave_value', 'ang_size_value']
            StudentData(dataframe = dataframe, id_col="student_id", sid = student_id, cols_to_display = cols, allow_id_set = allow_sid_set)
                            