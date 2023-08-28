import solara

from .FreeResponse import FreeResponseQuestionSingleStudent, FreeResponseSummary
from .MultipleChoice import MultipleChoiceQuestionSingleStudent, MultipleChoiceSummary

## TODO: persitantly hightlight selected row in question summary
## TODO: split summary into stages like the inidividual student responses

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
            
            solara.Select(label = 'Select Student', values = roster.value.student_ids, value=sid)
            
            return
        
        solara.Markdown(f"**Current Student**: {sid}")
        
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

