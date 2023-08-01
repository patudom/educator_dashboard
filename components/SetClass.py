import solara

from class_report import Roster
from pandas import DataFrame

@solara.component
def SetClass(class_id, student_summary, student_data, roster, first_run = False):
    def on_value(value):
        if value is None:
            return
        elif int(value) <= 183:
            class_id.set(None)
            return
        else:
            class_id.set(int(value))
            print("setting class id", value)
            roster.set(Roster(int(value)))
            student_summary.set(roster.value.short_report())
            student_data.set(DataFrame(roster.value.get_class_data()))
            
    
    if first_run.value and class_id.value is not None:
        print("first run")
        first_run.set(False)
        on_value(class_id.value)
    
    if class_id.value is None:
        warning_text = """There was a problem with this class. Look at the python output to see what. We currently can't handle class ids below 183.
        This will be fixed in the future as we turn away from the old class_report code.            
            """
        solara.Markdown(warning_text, style="color: red; font-size: 2em" )
    
    solara.InputText(label="Class ID",  value = str(class_id), on_value=on_value)
