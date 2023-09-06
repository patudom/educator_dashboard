
import solara

from ..components.Dashboard import Dashboard
from ..components.SetClass import SetClass



from ..database.class_report import Roster
from typing import cast

from pandas import DataFrame




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
    first_run = solara.use_reactive(True)
    
    story_name = "HubbleDS"
    
    with solara.Columns([1, 10, 2]):
        solara.Image("https://github.com/cosmicds/cds-website/raw/main/public/cosmicds_logo_transparent_for_light_backgrounds.png")

        solara.Markdown(f"#{story_name} Educator Dashboard", style={'text-align': 'center', 'width': '100%'})

        SetClass(class_id, roster, first_run)
    
    Dashboard(roster) 
    # solara.DataFrame(df.value)


# The following line is required only when running the code in a Jupyter notebook:
Page()