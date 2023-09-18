
import solara

from ..components.Dashboard import Dashboard
from ..components.SetClass import SetClass
from ..components.StudentDataLoad import StudentNameLoad
from ..components.ReportDownload import ShowReport


from ..database.class_report import Roster
from typing import cast

from pandas import DataFrame


class_id_list = [188, 195, 192, 185, 172, 170]

@solara.component
def Page():
    solara.Title("CosmicDS Dashboard")

    
    # for testing use 
    # - 195 (a full current class)
    # - 192 (an empty class)
    # - 188 (real spring beta class)
    # - 185 (testing spring beta class)
    # - 172 (old outdated class - should show stuff but probably incorrect)
    # - 170 (outdated class - should show nothing)
    class_id = solara.use_reactive(195) # add class id here
    roster = solara.use_reactive(cast(Roster, None))
    student_names = solara.use_reactive(None)
    first_run = solara.use_reactive(True)
    
    story_name = "HubbleDS"
    
    with solara.Columns([1, 9, 3]):
        # solara.Image("https://github.com/cosmicds/cds-website/raw/main/public/cosmicds_logo_transparent_for_light_backgrounds.png")
        solara.Image(image="static/assets/cosmicds_logo_transparent.png")

        solara.Markdown(f"#{story_name} Educator Dashboard", style={'text-align': 'center', 'width': '100%'})

        with solara.Column(gap="0px"):
            SetClass(class_id, roster, first_run, class_id_list)
            ShowReport(roster)
            StudentNameLoad(roster, student_names)
            
                

    Dashboard(roster, student_names=student_names) 
    # solara.DataFrame(df.value)


# The following line is required only when running the code in a Jupyter notebook:
Page()