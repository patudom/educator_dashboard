import solara
from solara.lab import Tab, Tabs
from typing import Optional
from ..class_report import Roster
from solara.reactive import Reactive

from .FreeResponse import FreeResponseQuestionSingleStudent, FreeResponseSummary
from .MultipleChoice import MultipleChoiceQuestionSingleStudent, MultipleChoiceSummary
from .DataComponent import StudentDataSummary
from .LayoutComponents import ScrollY

## TODO: persitantly hightlight selected row in question summary
## TODO: split summary into stages like the inidividual student responses

@solara.component
def IndividualStudentResponses(roster: Reactive[Roster] | Roster, sid: Reactive[Optional[int]]=Reactive(None), stage_labels=[], which_tab = 0):
    """
    Show response detail for each student
    sid is the currently selected student
    """
    which_tab = solara.use_reactive(which_tab)
    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return
    

    if sid.value is None:
        solara.Markdown(f"####  Select a student from the table above to see their responses.")
        return
    
    
    # multiple choice questions
    with Tabs(value = which_tab):
        with Tab("Multiple Choice", classes=["horizontal-tabs"]):
            with ScrollY(height='40vh'):
                MultipleChoiceQuestionSingleStudent(roster, sid = sid, stage_labels=stage_labels)
            
        with Tab("Free Response", classes=["horizontal-tabs"]):
            with ScrollY(height='40vh'):
                FreeResponseQuestionSingleStudent(roster, sid = sid, stage_labels=stage_labels)
        
        with Tab("Data", classes=["horizontal-tabs"]):
            StudentDataSummary(roster, student_id = sid.value, allow_sid_set=False)


@solara.component
def StudentQuestionsSummary(roster: Reactive[Roster] | Roster, sid = None, stage_labels=[], which_tab = 0):
    which_tab = solara.use_reactive(which_tab)
    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return
    
    
    with Tabs(value = which_tab):
        with Tab("Multiple Choice", classes=["horizontal-tabs"]):
            # if not empty_class:
            solara.Markdown(f"####  Click any row for more detailed question information.")
            with ScrollY(height='40vh'):
                MultipleChoiceSummary(roster, stage_labels=stage_labels)
            
        with Tab("Free Response", classes=["horizontal-tabs"]):
            with ScrollY(height='40vh'):
                FreeResponseSummary(roster, stage_labels=stage_labels)
        
        with Tab("Data", classes=["horizontal-tabs"]):
            StudentDataSummary(roster, student_id = None, allow_sid_set=False)
