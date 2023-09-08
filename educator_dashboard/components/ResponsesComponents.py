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
        with solara.lab.Tab("Multiple Choice"):
            with ScrollY(height='50vh'):
                MultipleChoiceQuestionSingleStudent(roster, sid = sid)
            
        with solara.lab.Tab("Free Response"):
            with ScrollY(height='50vh'):
                FreeResponseQuestionSingleStudent(roster, sid = sid)
        
        with solara.lab.Tab("Data"):
            StudentDataSummary(roster, student_id = sid.value, allow_sid_set=False)


@solara.component
def StudentQuestionsSummary(roster, sid = None):
    
    css = """
    #click-any-row-for-more-detailed-question-information {
        padding-left: 10px;    
    }
    #select-a-student-from-the-table-above-to-see-their-responses {
        padding-left: 10px;    
    }
    body {
        padding-inline: 5% 
    }

    /* This disables the plotly tools */
    .modebar{
      display: none !important;
    }   

    """

    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return

    with solara.lab.Tabs():
        with solara.lab.Tab("Multiple Choice"):
            solara.Style(css)
            # if not empty_class:
            solara.Markdown(f"####  Click any row for more detailed question information.")
            with ScrollY(height='50vh'):
                MultipleChoiceSummary(roster)
            
        with solara.lab.Tab("Free Response"):
            with ScrollY(height='50vh'):
                FreeResponseSummary(roster)
        
        with solara.lab.Tab("Data"):
            StudentDataSummary(roster, student_id = None, allow_sid_set=False)
