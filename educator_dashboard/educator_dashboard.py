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
def EducatorDashboard(url_params = {}, class_list = []):
    query = QueryCosmicDSApi()
    
    router = solara.use_router()
    if router.search is not None:
        url_params = {x.split("=")[0]: x.split("=")[1] for x in router.search.split("&")}
    else:
        url_params = {}
    
    url_id = int(url_params["id"]) if "id" in url_params else None
    
    
    class_id = solara.use_reactive(url_id)
    class_id_list = solara.use_reactive(class_list)
    

    
    
    # What to show and when
    # No educator code
    #  - in dev mode: show test set of classes
    #  - not in dev mode: deny access
    # Educator code provided
    #  - if no class id provided: show first class for educator code
    #  - if class id provided: show class if it exists for educator code
    
    
    
    

    roster = solara.use_reactive(
        cast(Roster, None), on_change=lambda x: print("roster changed")
    )
    student_names = solara.use_reactive(None)
    dashboard_names = solara.use_reactive(None)  # , on_change=on_change_names)
    first_run = solara.use_reactive(True)
    are_names_set = solara.use_reactive(False)

    story_name = "HubbleDS"

    # with solara.Columns([6, 3, 3], classes=["my-column"]):
    with rv.Html(tag="div", class_="cds-dashboard"):
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
