import solara

from class_report import Roster
from pandas import DataFrame

@solara.component
def SetClass(class_id, student_summary, student_data, roster, first_run = False):
    def on_value(value):
        if value is None:
            return
        class_id.set(int(value))
        print("setting class id", value)
        roster.set(Roster(int(value)))
        student_summary.set(roster.value.short_report())
        student_data.set(DataFrame(roster.value.get_class_data()))
    
    if first_run and class_id.value is not None:
        print("first run")
        first_run.set(False)
        on_value(class_id.value)
    
    solara.InputText(label="Class ID",  value = str(class_id), on_value=on_value)
