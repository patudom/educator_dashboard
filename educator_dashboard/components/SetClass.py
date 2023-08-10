import solara

from educator_dashboard.database.class_report import Roster
from pandas import DataFrame

@solara.component
def SetClass(class_id, student_summary, student_data, roster, first_run = False):
    
    print('in SetClass')
    
    
    def on_value(value):
        print("SetClass: on_value", value)
        if value is None:
            print("SetClass: class_id is None")
            class_id.set(None)
            roster.set(None)
            student_summary.set(None)
            student_data.set(None)
        elif first_run.value or (class_id.value != value):
            print("SetClass: class id", value)
            class_id.set(int(value))
            roster.set(Roster(int(value)))
            student_summary.set(roster.value.short_report())
            student_data.set(DataFrame(roster.value.get_class_data()))
    
    if first_run.value and class_id.value is not None:
        print("SetClass: first run", )
        on_value(class_id.value)
        first_run.set(False)
        

            
    
    
    if class_id.value is None:
        warning_text = """There was a problem with this class. Look at the python output to see what. We currently can't handle class ids below 183.
        This will be fixed in the future as we turn away from the old class_report code.            
            """
        solara.Markdown(warning_text, style="color: red; font-size: 2em" )
    
    solara.InputText(label="Class ID",  value = str(class_id), on_value=on_value)
