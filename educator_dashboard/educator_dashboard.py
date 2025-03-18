import solara
from .components.TeacherCodeInput import class_query_res
from .components.Dashboard import Dashboard
from .components.SetClass import SetClass
from .components.StudentDataLoad import StudentNameLoad
from .components.ReportDownload import DownloadReport
import reacton.ipyvuetify as rv

from .class_report import Roster
from typing import cast, Any, Dict, List

from .database.Query import QueryCosmicDSApi


from .components.RefreshClass import RefreshClass


@solara.component
def EducatorDashboard(educator_code = None):
    router = solara.use_router()
    if router.search is not None:
        url_params = {x.split("=")[0]: x.split("=")[1] for x in router.search.split("&")}
    else:
        url_params = {}
    
    url_id = int(url_params["id"]) if "id" in url_params else None

    query = QueryCosmicDSApi()
    
    # What to show and when
    # No educator code
    #  - in dev mode: show test set of classes
    #  - not in dev mode: deny access
    # Educator code provided
    #  - if no class id provided: show first class for educator code
    #  - if class id provided: show class if it exists for educator code
    
    if educator_code is None and query.in_dev_mode():
        
        educator_code = "test"
        class_id_list = solara.use_reactive(class_query_res)  # [int]
        class_id = solara.use_reactive(url_id)
        
        solara.Warning(f"Running in dev mode with class_id {url_id}")
        
    elif educator_code is None:
        solara.Error("No educator code provided", color="error")
        return
    
    else: # educator_code provided
        class_list = query.get_class_for_teacher(educator_code) 
        class_id_list = solara.use_reactive(cast(List[Dict[str, Any]], class_list['classes']))
        
        # if no classes are found for the educator code, show an error message
        if len(class_list['classes']) == 0:
            educator_info = query.get_teacher_info(educator_code)['educator']
            with solara.Card():
                solara.Error(f"No classes found for educator code: {educator_code}", color="error")
                solara.Markdown(f"""
                            No classes found for educator code: {educator_code}\n
                            Educator Info: \n
                            - Name: {educator_info['first_name']} {educator_info['last_name']} \n
                            - id: {educator_info['id']}\n
                            - Email: {educator_info['email']}"""
                            )
                solara.Text(f"{class_list}")
            return
        
        
        # go to provided class id else the first class id
        if any(url_id == x.get('id', -999) for x in class_id_list.value):
            class_id = solara.use_reactive(url_id)  # add class id here
        else:
            class_id = solara.use_reactive(class_id_list.value[0]['id'])  # set to None if not found
            if (url_id is not None):
                solara.Error(f"Invalid class id {url_id} provided for educator code: {educator_code}", color="error")
                return
            else:
                solara.Warning(f"No class id provided. Using first class found for educator code: {educator_code}", color="error")
        
    
    

    roster = solara.use_reactive(
        cast(Roster, None), on_change=lambda x: print("roster changed")
    )
    student_names = solara.use_reactive(None)
    dashboard_names = solara.use_reactive(None)  # , on_change=on_change_names)
    first_run = solara.use_reactive(True)
    are_names_set = solara.use_reactive(False)

    story_name = "HubbleDS"

    # with solara.Columns([6, 3, 3], classes=["my-column"]):
    with rv.Row():
        with rv.Col(cols=8):
            SetClass(class_id, roster, first_run, class_id_list, query)

        # with rv.Col(cols=2):
        #     StudentNameLoad(
        #         roster,
        #         student_names,
        #         names_set=are_names_set,
        #         on_update=dashboard_names.set,
        #     )

        # with rv.Col(cols=2):
        #     DownloadReport(roster)

        RefreshClass(
            rate_minutes=20.0 / 60.0,
            roster=roster,
            student_names=dashboard_names.value,
            show_refresh_button=False,
            stop_start_button=False,
            refresh_button_text=None,
            # show button to manually refresh and to start/stop autorefresh. no text cuz icon_only is set
            refresh_button_color="primary",
            start_button_color="#777",
            stop_button_color="#ccc",
            icon_only=True,
        )

    Dashboard(roster, dashboard_names, add_names=dashboard_names.value is not None)

    # solara.DataFrame(df.value)
