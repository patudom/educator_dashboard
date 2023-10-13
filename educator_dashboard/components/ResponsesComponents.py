import solara

from .FreeResponse import FreeResponseQuestionSingleStudent, FreeResponseSummary
from .MultipleChoice import MultipleChoiceQuestionSingleStudent, MultipleChoiceSummary
from .DataComponent import StudentDataSummary
from .LayoutComponents import ScrollY

## TODO: persitantly hightlight selected row in question summary
## TODO: split summary into stages like the inidividual student responses

@solara.component
def IndividualStudentResponses(roster, sid=None, stage_labels=[]):
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
            with ScrollY(height='40vh'):
                MultipleChoiceQuestionSingleStudent(roster, sid = sid, stage_labels=stage_labels)
            
        with solara.lab.Tab("Free Response", classes=["horizontal-tabs"]):
            with ScrollY(height='40vh'):
                FreeResponseQuestionSingleStudent(roster, sid = sid, stage_labels=stage_labels)
        
        with solara.lab.Tab("Data", classes=["horizontal-tabs"]):
            StudentDataSummary(roster, student_id = sid.value, allow_sid_set=False)


@solara.component
def StudentQuestionsSummary(roster, sid = None, stage_labels=[]):

    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return

    with solara.lab.Tabs():
        with solara.lab.Tab("Multiple Choice", classes=["horizontal-tabs"]):
            # if not empty_class:
            solara.Markdown(f"####  Click any row for more detailed question information.")
            with ScrollY(height='40vh'):
                MultipleChoiceSummary(roster, stage_labels=stage_labels)
            
        with solara.lab.Tab("Free Response", classes=["horizontal-tabs"]):
            with ScrollY(height='40vh'):
                FreeResponseSummary(roster, stage_labels=stage_labels)
        
        with solara.lab.Tab("Data", classes=["horizontal-tabs"]):
            StudentDataSummary(roster, student_id = None, allow_sid_set=False)
