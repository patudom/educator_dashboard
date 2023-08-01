import solara
import solara

from components.Dashboard import Dashboard, SetClass


from class_report import Roster
from typing import cast

from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go


class_id = solara.reactive(195) # add class id here
roster = solara.reactive(cast(Roster, None))
df = solara.reactive(cast(DataFrame, None))
data = solara.reactive(cast(DataFrame, None))
first_run = solara.reactive(True)

@solara.component
def Page():
    
    SetClass(class_id, df, data, roster, first_run)
    
    if class_id.value is not None:
        Dashboard(df, data) 


# The following line is required only when running the code in a Jupyter notebook:
Page()