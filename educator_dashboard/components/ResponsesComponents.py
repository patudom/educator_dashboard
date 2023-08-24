import solara

# equivalent to from reacton import ipyvuetify as rv
from solara.alias import rv
from pandas import DataFrame


from .FreeResponse import FreeResponseQuestionSingleStudent, FreeResponseSummary
from .MultipleChoice import MultipleChoiceQuestionSingleStudent, MultipleChoiceSummary

with solara.Card():
        with solara.Column():
            pass
        with solara.Column():
            pass
        


@solara.component
def StudentQuestion(dataframe = None, roster=None, sid = None):
    """
    Show the responses for a single student
    """
    
    if isinstance(dataframe, solara.Reactive):
        # solara.DataFrame(df.value)
        table = dataframe.value
    else:
        # solara.DataFrame(df)
        table = dataframe
    # table = table.to_frame()
    table['question'] = table.index
    
    
    mc_questions = table[table.tag.apply(lambda x: len(str(x).split('.'))==3)]

    
    
    
    # multiple choice questions
    with solara.lab.Tabs():
        with solara.lab.Tab("Multiple Choice"):
            MultipleChoiceQuestionSingleStudent(mc_questions)
            
        with solara.lab.Tab("Free Response"):
            FreeResponseQuestionSingleStudent(roster, sid = sid)
        

@solara.component
def IndividualStudentResponsePanel(questions, qtags = None, sid = None):
    
    if sid.value is None:
        solara.Markdown('**Select a student to see their responses**')
        return
    
    
    # squeeze dataframe to a series
    row = questions[questions['student_id'] == sid.value].squeeze()
    
    # # drop student id and rename series to value
    df = row.drop('student_id').rename('value').to_frame()
    
    # # add full N.tag.?(triest|score|choice) tag as a column
    df['tag'] = qtags
    
    # solara.DataFrame(df)
    StudentQuestion(df)

@solara.component
def IndividualStudentResponses(roster, sid=None):
    """
    Show response detail for each student
    sid is the currently selected student
    """
    
    if roster.value is None:
        return
    
    # we need to replace the tag with the short version of the question
    questions = roster.value.questions()
    qtags = [c for c in questions.columns if '.' in c]
    qkeys = roster.value.question_keys()
    short_qs =  list(map(lambda x: qkeys.get(x.split('.')[1])['shorttext'] , qtags))
    replacements = dict(zip(qtags, short_qs))
    # questions = questions.rename(columns = replacements)
    
    sids = [int(s) for s in questions['student_id'].to_list()]
    
    with solara.Card():
        if sid.value is None:
            solara.Markdown('**Select a student to see their responses**')
            return
        
        
        # squeeze dataframe to a series
        row = questions[questions['student_id'] == sid.value].squeeze()
        
        # # drop student id and rename series to value
        df = row.drop('student_id').rename('value').to_frame()
        
        # # add full N.tag.?(triest|score|choice) tag as a column
        df['tag'] = qtags
        
        # solara.DataFrame(df)
        StudentQuestion(df, roster, sid)


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

