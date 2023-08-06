import solara
from pandas import DataFrame


@solara.component
def QuestionSummary(df = None, sid = None):
    """
    Show response summary for entire class
    """
    if df is not None:
        if isinstance(df, solara.Reactive):
            df = df.value
        solara.DataFrame(df)
        

@solara.component
def StudentQuestion(df = None):
    """
    Show the responses for a single student
    """
    if df is not None:
        if isinstance(df, solara.Reactive):
            df = df.value
        solara.DataFrame(df)
        
        
@solara.component
def IndividualStudentResponses(roster, sid=None):
    """
    Show response detail for each student
    sid is the currently selected student
    """
    if not isinstance(sid, solara.Reactive):
        sid = solara.reactive(sid)
    
    questions = roster.value.questions()
    sids = questions['student_id'].to_list()
    with solara.lab.Tabs(
        value = 0 if (sid.value is None or sid.value not in sids) else sids.index(sid.value), 
        on_value = lambda x: sid.set(sids[x])
        ):
        for i, row in questions.iterrows(): 
            with solara.lab.Tab(str(row['student_id'])):
                solara.Markdown(f"**Student {row['student_id']}**")
                df = DataFrame(row.drop('student_id'))
                # copy the index to a column
                df['question'] = df.index
                # drop rows where question contains score or choice in string
                df = df[~df['question'].str.contains('score|choice')]
                StudentQuestion(df)

@solara.component
def StudentQuestions(roster, sid = None):
    if not isinstance(sid, solara.Reactive):
        sid = solara.reactive(sid)
    
    questions = roster.value.questions()
    with solara.Columns([1,1]):
        with solara.Column():
            QuestionSummary(questions, sid = sid)
           
