import solara
import reacton.ipyvuetify as rv
from .ClassPlot import ClassPlot
from .TableDisplay import TableDisplay
from pandas import DataFrame, to_datetime
import plotly.express as px

from numpy import around, isnan
from math import ceil, floor

from .TableComponents import DataTable
from .AgeHistogram import AgeHoHistogram
from .BetterTooltip import Tooltip


def get_class_subset(data, sid, ungroup = True):
    if isinstance(sid, solara.Reactive):
        sid = sid.value
    if sid is None:
        return None
    sid = str(sid)
    
    # convert last_modified to datetime
    data['last_modified'] = to_datetime(data['last_modified'])
    data['student_id'] = data['student_id'].apply(str)

    # group by student_id
    grouped = data.groupby('student_id')

    # get people who completed and their times
    time = DataFrame(grouped['last_modified'].max())
    size = grouped.size()
    if all(size == 1):
        complete = (size == 1)
    else:
        complete = (size == 5)
    
    before = time['last_modified'] <= time[time.index == sid]['last_modified'].max()
    ten_earlist_completed = time[complete].sort_values('last_modified').head(10)
    ten_earliest_mask = time.index.isin(ten_earlist_completed.index)
    subset = (before & complete) | ten_earliest_mask | (time.index == sid)
    
    if not ungroup:
        return subset.to_list()

    # put complete back into data
    subset = data['student_id'].isin(time[subset].index).to_list()
    
    # assert sum(subset) % 5 == 0
    
    
    return subset



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
    
    data = roster.get_class_data(df=True)
    
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
    
    subset = None
    subset_name = None
    if student_id.value is not None:
        
        subset = get_class_subset(data, student_id)
        subset_name = f'Data seen by {student_id.value}'
        
    
    if allow_click:
        with solara.Column(gap="0px"):
            ClassPlot(data, on_click=on_plot_click, select_on = 'student_id', selected = student_id, allow_click=True, subset = subset, subset_label=subset_name, subset_color='mediumpurple')
    else:
        with solara.Column():
            ClassPlot(data, select_on = 'student_id', selected = student_id, allow_click = False, subset = subset, subset_label=subset_name, subset_color='mediumpurple')

    

from numpy import nan, array
def get_slope(x, y):
    if (x is None) or (y is None):
        return nan
    # drop None values
    pairs = [(xi,yi) for xi,yi in zip(x,y) if (xi is not None) and (yi is not None)]
    if len(pairs) == 0:
        return nan
    x, y = array(pairs).T
    # slope through origin
    return nan if (sum(x**2) == 0) else (sum(x*y)/sum(x**2))
def slope2age(h0):
    return 977.79222 / h0 # age of universe in Gyr



    
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
    
    dataframe = roster.get_class_data(df = True)
    if len(dataframe) == 0:
        solara.Markdown("There is no data for this class")
        return


    if sid is not None and sid.value is not None:        
        StudentMeasurementTable(roster, sid, headers = cols_to_display)
            
@solara.component
def StudentAgeHubble(roster = None, sid = None, allow_id_set = True):

    if isinstance(roster, solara.Reactive):
        roster = roster.value
    if roster is None:
        return
    
    dataframe = roster.get_class_data(df = True)
    if len(dataframe) == 0:
        solara.Markdown("There is no data for this class")
        return

    if sid is not None and sid.value is not None:        
        single_student_df = roster.get_student_data(sid.value, df = True)
        print("single_student", sid, sid.value, single_student_df)
        h0 = get_slope(single_student_df['est_dist_value'].to_numpy(), single_student_df['velocity_value'].to_numpy())
        age = slope2age(h0)
        solara.Markdown(f"#### Student Age of Universe:")
        solara.Markdown(f"{age:.0f} Gyr")
        solara.Markdown(f"#### Student Hubble Constant:")
        solara.Markdown(f"{h0:.0f} km/s/Mpc")


@solara.component
def DataHistogram(roster = None, id_col = 'student_id',  sid = None):
    """
    Display a single student's data
    """
    
    print('Displaying single students data')
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
    if roster is None:
        return
    
    dataframe = roster.get_class_data(df = True)
    dataframe['last_modified'] = to_datetime(dataframe['last_modified'])
    if len(dataframe) == 0:
        solara.Markdown("There is no data for this class")
        return

    grouped = dataframe.groupby(id_col)
    h0 = grouped.apply(lambda x: get_slope(x['est_dist_value'].to_numpy(), x['velocity_value'].to_numpy()))
    age = h0.apply(slope2age)
    time = grouped['last_modified'].max()
    data = DataFrame({'h0': h0, 'age': age, 'last_modified': time}).reset_index()
    # student_id to str
    data['student_id'] = data['student_id'].apply(str)
    data['h0'] = data['h0'].apply(lambda x: around(x,0))
    data['age'] = data['age'].apply(lambda x: around(x,0))
    

    if sid is not None and sid.value is not None:
            
        subset = get_class_subset(data, sid, ungroup = False)

        AgeHoHistogram(data, 
                       which = 'age', 
                       subset = subset, 
                       subset_label = f'Data seen by {sid.value}', 
                       subset_color = 'mediumpurple',
                       title = f'Class Age Distribution seen by {sid.value}')
    else:

        # print out number of students with good data
        num_good = len(data[~isnan(data['h0'])])
        num_total = len(data)
        n_students = len(roster.student_ids)
        line1 = f"**Number of students**: {n_students} "
        line2 = f"**Number of students with measurements**: {num_total}"
        line3 = f"**Number of students with good measurements**: {num_good}"
        
        with Tooltip(tooltip = solara.Markdown('<br>'.join([line1,line2,line3])), 
                     color = 'white',
                     top=True):
            solara.Text(f"{num_good}/{num_total} have good data")
        
        AgeHoHistogram(data)


@solara.component
def StudentDataSummary(roster = None, student_id = None, allow_sid_set = True):
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
    if roster is None:
        return

    if not isinstance(student_id, solara.Reactive):
        student_id = solara.use_reactive(student_id)

    with solara.Row():
        with solara.Columns([1,1]):
            with solara.Card(style='height: 95%'):
                DataSummary(roster, student_id, allow_click=allow_sid_set)

            with solara.Card(style='height: 95%'):
                DataHistogram(roster, sid = student_id)

    if student_id is not None and student_id.value is not None:
        with solara.Row():
            with solara.Columns([1,1]):
                with solara.Card(style='height: 90%'):
                    solara.Markdown(f"#### Student Galaxy Measurements")
                    
                    headers = [
                        {'value': 'galaxy_id', 'text': 'Galaxy ID'},
                        {'value': 'obs_wave_value', 'text': 'Observed Wavelength <br/> (Angstrom)'},
                        {'value': 'velocity_value', 'text': 'Velocity <br/> (km/s)'},
                        {'value': 'ang_size_value', 'text': 'Angular Size <br/> (arcsecond)'},
                        {'value': 'est_dist_value', 'text': 'Distance <br/> (Mpc)'},
                    ]
                    
                    StudentData(roster, id_col="student_id", sid = student_id, cols_to_display = headers, allow_id_set = allow_sid_set)

                with solara.Card(style='height: 90%'):
                    StudentAgeHubble(roster, sid = student_id)

        
                          
                          

        
          