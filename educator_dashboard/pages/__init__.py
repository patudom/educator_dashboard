
import solara

from ..components.Dashboard import Dashboard
from ..components.SetClass import SetClass



from ..database.class_report import Roster
from typing import cast

from pandas import DataFrame




@solara.component
def Page():
    
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
    
    story_name = "Hubble Data Story"
    
    with solara.Card():
        #center on page
        solara.Markdown(f"# {story_name.title()} Educator Dashboard", style={'text-align': 'center', 'width': '100%'})

        SetClass(class_id, roster, first_run)
        
        Dashboard(roster, student_names=student_names) 
        # solara.DataFrame(df.value)


# The following line is required only when running the code in a Jupyter notebook:
Page()