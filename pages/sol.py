import os
import sys
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import solara

from components.Dashboard import Dashboard, SetClass


from class_report import Roster
from typing import cast

from pandas import DataFrame


class_id = solara.reactive(195) # add class id here
roster = solara.reactive(cast(Roster, None))
df = solara.reactive(DataFrame())
data = solara.reactive(DataFrame())
first_run = solara.reactive(True)

@solara.component
def Page():

    SetClass(class_id, df, data, roster, first_run)
    
    Dashboard(df, data, roster) 
    # solara.DataFrame(df.value)


# The following line is required only when running the code in a Jupyter notebook:
Page()