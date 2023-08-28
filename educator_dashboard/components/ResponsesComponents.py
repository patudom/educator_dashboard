import solara

from .FreeResponse import FreeResponseQuestionSingleStudent, FreeResponseSummary
from .MultipleChoice import MultipleChoiceQuestionSingleStudent, MultipleChoiceSummary


@solara.component
def IndividualStudentResponses(roster, sid=None):
    """
    Show response detail for each student
    sid is the currently selected student
    """
    
    if roster.value is None:
        return
    
    with solara.Card():
        if sid.value is None:
            solara.Markdown('**Select a student to see their responses**')
            return
        
        # multiple choice questions
        with solara.lab.Tabs():
            with solara.lab.Tab("Multiple Choice"):
                MultipleChoiceQuestionSingleStudent(roster, sid = sid)
                
            with solara.lab.Tab("Free Response"):
                FreeResponseQuestionSingleStudent(roster, sid = sid)


@solara.component
def StudentQuestionsSummary(roster, sid = None):
    if roster.value is None:
        return
    
    
    with solara.Card():
        with solara.lab.Tabs():
            with solara.lab.Tab("Multiple Choice"):
                MultipleChoiceSummary(roster)
                
            with solara.lab.Tab("Free Response"):
                FreeResponseSummary(roster)

