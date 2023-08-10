
import solara

from educator_dashboard.components import Dashboard, SetClass


from educator_dashboard.database.class_report import Roster
from typing import cast

from pandas import DataFrame




@solara.component
def Page():
    
    class_id = solara.use_reactive(195) # add class id here
    roster = solara.use_reactive(cast(Roster, None))
    df = solara.use_reactive(DataFrame())
    data = solara.use_reactive(DataFrame())
    first_run = solara.use_reactive(True)

    SetClass.SetClass(class_id, df, data, roster, first_run)
    
    Dashboard.Dashboard(df, data, roster) 
    # solara.DataFrame(df.value)


# The following line is required only when running the code in a Jupyter notebook:
Page()