import solara

from .FreeResponse import FreeResponseQuestionSingleStudent, FreeResponseSummary
from .MultipleChoice import MultipleChoiceQuestionSingleStudent, MultipleChoiceSummary
from .DataComponent import StudentDataSummary
from .LayoutComponents import ScrollY
from pandas import DataFrame

## TODO: persitantly hightlight selected row in question summary
## TODO: split summary into stages like the inidividual student responses

@solara.component
def IndividualStudentResponses(roster, sid=None):
    """
    Show response detail for each student
    sid is the currently selected student
    """
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return
    

    if sid.value is None:
        solara.Markdown(f"####  Select a student from the table above to see their responses.")
        return
    
    # multiple choice questions
    with solara.lab.Tabs():
        with solara.lab.Tab("Multiple Choice", classes=["horizontal-tabs"]):
            with ScrollY(height='55vh'):
                MultipleChoiceQuestionSingleStudent(roster, sid = sid)
            
        with solara.lab.Tab("Free Response", classes=["horizontal-tabs"]):
            with ScrollY(height='55vh'):
                FreeResponseQuestionSingleStudent(roster, sid = sid)
        
        with solara.lab.Tab("Data", classes=["horizontal-tabs"]):
            StudentDataSummary(roster, student_id = sid.value, allow_sid_set=False)


@solara.component
def StudentQuestionsSummary(roster, sid = None):

    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return

    with solara.lab.Tabs():
        with solara.lab.Tab("Multiple Choice", classes=["horizontal-tabs"]):
            # if not empty_class:
            solara.Markdown(f"####  Click any row for more detailed question information.")
            with ScrollY(height='55vh'):
                MultipleChoiceSummary(roster)
            
        with solara.lab.Tab("Free Response", classes=["horizontal-tabs"]):
            with ScrollY(height='55vh'):
                FreeResponseSummary(roster)
        
        with solara.lab.Tab("Data", classes=["horizontal-tabs"]):
            StudentDataSummary(roster, student_id = None, allow_sid_set=False)
