import solara
from .ClassPlot import ClassPlot
from .TableDisplay import TableDisplay
from pandas import DataFrame
import plotly.express as px

from numpy import around
from math import ceil, floor

from .TableComponents import DataTable


@solara.component
def DataSummary(roster = None, student_id = None, on_student_id = None, allow_click = True):
    """
    Display a summary of the data
    """
    
    print('Displaying data summary')
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
    if roster is None:
        return
    
    data = DataFrame(roster.get_class_data())
    
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
            ClassPlot(data, on_click=on_plot_click, select_on = 'student_id', selected = student_id, allow_click=True)
    else:
        with solara.Column():
            ClassPlot(data, select_on = 'student_id', selected = student_id, allow_click = False)
    

from math import nan
def get_slope(x, y):
    # slope through origin
    return nan if (sum(x**2) == 0) else (sum(x*y)/sum(x**2))
def slope2age(h0):
    return 977.79222 / h0 # age of universe in Gyr


@solara.component
def AgeHoHistogram(data, age_col = 'age', h0_col = 'h0', which = 'age'):
    
    col_data = data[age_col]; 
    col_data = col_data[col_data>0]; 
    xmin, xmax = floor(col_data.min()), ceil(col_data.max())
    categories = list(range(xmin, xmax+1))
    fig = px.histogram(data_frame = data, x = which, labels={age_col:'Age of Universe (Gyr)'}, category_orders={age_col: categories})
    fig.update_xaxes(type='category')
    fig.update_layout(showlegend=False, title_text='Class Age Distribution')
    # show only integers on y-axis
    fig.update_yaxes(tick0=0, dtick=1)
    # show ticks every 1
    # fig.update_xaxes(dtick=1)

    solara.FigurePlotly(fig)
    
@solara.component
def StudentMeasurementTable(roster = None, sid = None, headers = None, show_class = False, show_index = False):
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
    if roster is None:
        return
    
    if isinstance(sid, solara.Reactive):
        sid = sid.value
        
    if sid in roster.student_ids:
        dataframe = DataFrame(roster.get_student_data(sid))
    elif (sid is None) and show_class:
        dataframe = DataFrame(roster.get_class_data(df = True))
    else:
        solara.Markdown('Provided invalid student id')
        return
       

    if isinstance(headers, list):
        if isinstance(headers[0], dict) and {'text','value'}.issubset(headers[0].keys()):
            print('Good heaaders')
        elif isinstance(headers[0], str):
            headers = [{'text': h, 'value': h} for h in headers]
        else:
            print('StudentMeasurementTable: headers is a list but not of the form [{"text": "header", "value": "col_name"}, ...]')
            print('defaulting to displaying all columns  with their column names')
            headers = [{'text': h, 'value': h} for h in dataframe.columns]
    elif isinstance(headers, dict):
        headers = [{'text': v, 'value': k} for k,v in headers.items()]
    else:
        headers = [{'text': h, 'value': h} for h in dataframe.columns]
    
    
    DataTable(df = dataframe, headers = headers, class_ = "student-measurement-table", show_index=show_index)

@solara.component
def StudentData(roster = None, id_col = 'student_id',  sid = None, cols_to_display = None, on_sid = None, allow_id_set = True):
    """
    Display a single student's data
    """
    
    print('Displaying single students data')
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
    if roster is None:
        return


    if sid is not None and sid.value is not None:
        
        with solara.Column(gap="0px"):
            with solara.Column(gap="0px"):
                single_student_df = roster.get_student_data(sid.value, df = True)
                h0 = get_slope(single_student_df['est_dist_value'], single_student_df['velocity_value'])
                age = slope2age(h0)
                solara.Markdown(f"**Hubble Constant**: {h0:.1f} km/s/Mpc")
                solara.Markdown(f"**Age of Universe**: {age:.1f} Gyr")
                    
            
            StudentMeasurementTable(roster, sid, headers = cols_to_display)
    else:
        dataframe = roster.get_class_data(df = True)
        if len(dataframe) == 0:
            solara.Markdown("There is no data for this class")
            return
        sids = dataframe[id_col].unique()
        h0 = [get_slope(dataframe[dataframe[id_col] == sid]['est_dist_value'], dataframe[dataframe[id_col] == sid]['velocity_value']) for sid in sids]
        age = [slope2age(h) for h in h0]
        
        data = DataFrame({'sids': [str(s) for s in sids], 'h0': around(h0,0).astype(int), 'age': around(age,0).astype(int)})
        
        AgeHoHistogram(data)


@solara.component
def StudentDataSummary(roster = None, student_id = None, allow_sid_set = True):
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
    if roster is None:
        return

    if not isinstance(student_id, solara.Reactive):
        student_id = solara.use_reactive(student_id)
    
    with solara.Columns([1,1]):
        with solara.Column():
            DataSummary(roster, student_id, allow_click=allow_sid_set)
        
        with solara.Column():
            
            headers = [
                {'value': 'student_id', 'text': 'Student ID'},
                {'value': 'galaxy_id', 'text': 'Galaxy ID'},
                {'value': 'velocity_value', 'text': 'Velocity <br/> (km/s)'},
                {'value': 'est_dist_value', 'text': 'Distance <br/> (Mpc)'},
                {'value': 'obs_wave_value', 'text': 'Observed Wavelength <br/> (Angstrom)'},
                {'value': 'ang_size_value', 'text': 'Angular Size <br/> (arcsecond)'}
            ]
            StudentData(roster, id_col="student_id", sid = student_id, cols_to_display = headers, allow_id_set = allow_sid_set)
                            