
import solara
from ..components.TeacherCodeInput import TeacherCodeEntry
from ..components.Dashboard import Dashboard
from ..components.SetClass import SetClass
from ..components.StudentDataLoad import StudentNameLoad
from ..components.ReportDownload import DownloadReport
import reacton.ipyvuetify as rv

from ..database.class_report import Roster
from typing import cast

from ..database.Query import QueryCosmicDSApi


from ..components.RefreshClass import RefreshClass

@solara.component
def Page():
    query = QueryCosmicDSApi()
    show_dashboard, set_show_dashboard = solara.use_state(False)
    class_id_list = solara.use_reactive([None])
    class_id = solara.use_reactive(None) # add class id here
    if not show_dashboard: 
        def callback():
            set_show_dashboard(True)
        TeacherCodeEntry(class_id_list, class_id, callback, query = query)
        return
    
    solara.Title("CosmicDS Dashboard")
    print(" ================== main page ================== ")
    
    # for testing use 
    # - 199 (test class for dashboard refresh)
    # - 195 (a full current class)
    # - 192 (an empty class)
    # - 188 (real spring beta class)
    # - 185 (testing spring beta class)
    # - 172 (old outdated class - should show stuff but probably incorrect)
    # - 170 (outdated class - should show nothing)
    
    roster = solara.use_reactive(cast(Roster, None), on_change=lambda x: print("roster changed"))
    student_names = solara.use_reactive(None)
    dashboard_names = solara.use_reactive(None)#, on_change=on_change_names)
    first_run = solara.use_reactive(True)
    are_names_set = solara.use_reactive(False)
    
    story_name = "HubbleDS"
    

    with solara.Columns([1, 9, 3], classes=["my-column"]):
        # solara.Image("https://github.com/cosmicds/cds-website/raw/main/public/cosmicds_logo_transparent_for_light_backgrounds.png")
        with rv.Html(tag="a", attributes={'href':"https://www.cosmicds.cfa.harvard.edu/", 'target':"_blank"}):
            solara.Image(image="static/assets/cosmicds_logo_transparent.png")
         
        solara.Markdown(f"#{story_name} Educator Dashboard", style={'text-align': 'center', 'width': '100%'})


        with solara.Column(gap="0px", classes=["my-column"]):
            SetClass(class_id, roster, first_run, class_id_list, query)
            StudentNameLoad(roster, student_names, names_set=are_names_set, on_update=dashboard_names.set)
            DownloadReport(roster) 
                
            RefreshClass(rate_minutes=20./60., roster = roster, student_names = dashboard_names.value,
                         show_refresh_button=False, stop_start_button=False, refresh_button_text=None,
                         # show button to manually refresh and to start/stop autorefresh. no text cuz icon_only is set
                         refresh_button_color='primary', start_button_color='#777', stop_button_color='#ccc', 
                         icon_only=True)
        
    Dashboard(roster, dashboard_names, add_names = dashboard_names.value is not None) 

    # solara.DataFrame(df.value)


# The following line is required only when running the code in a Jupyter notebook:
Page()