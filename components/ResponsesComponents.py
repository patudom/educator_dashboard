import solara
from pandas import DataFrame

# from solara.components.dataframe import HistogramCard

import solara.express as px

@solara.component
def QuestionSummary(df = None, sid = None):
    """
    Show response summary for entire class
    """
    if isinstance(df, solara.Reactive):
        solara.DataFrame(df.value)
    else:
        solara.DataFrame(df)
        


@solara.component
def StudentQuestion(df = None):
    """
    Show the responses for a single student
    """
    
    if isinstance(df, solara.Reactive):
        # solara.DataFrame(df.value)
        table = df.value
    else:
        # solara.DataFrame(df)
        table = df
        
    # table is pandas dataframe with columns: question and score
    # solara.DataFrame(table)
    #mc_questions rows with value where len(value.split('.'))==3
    mc_questions = table[table.question.apply(lambda x: len(str(x).split('.'))==3)]
    #fr_questions rows with value where len(value.split('.'))==2
    fr_questions = table[table.question.apply(lambda x: len(str(x).split('.'))==2)]
    
    # multiple choice questions
    with solara.Columns([1,1]):
        with solara.Column():
            solara.Markdown('**Multiple Choice**')
            # solara.DataFrame(mc_questions)
            px.histogram(mc_questions.dropna(), 'score', custom_data= ['question'],)
            # solara.FigurePlotly(fig.)
        with solara.Column():
            solara.Markdown('**Free Response**')
            solara.DataFrame(fr_questions)
        
        
@solara.component
def IndividualStudentResponses(roster, sid=None):
    """
    Show response detail for each student
    sid is the currently selected student
    """
    
    if roster.value is None:
        return
    

    questions = roster.value.questions()
    sids = questions['student_id'].to_list()
    with solara.lab.Tabs(
        value = 0 if (sid.value is None or sid.value not in sids) else sids.index(sid.value), 
        on_value = lambda x: sid.set(sids[x])
        ):
        for i, row in questions.iterrows(): 
            with solara.lab.Tab(str(row['student_id'])):
                solara.Markdown(f"**Student {row['student_id']}**")
                df = row.drop('student_id').rename('score').to_frame()
                # copy the index to a column
                df['question'] = df.index
                # drop rows where question contains score or choice in string
                df = df[~df['question'].str.contains('score|choice')]
                StudentQuestion(df[['question', 'score']])

@solara.component
def StudentQuestions(roster, sid = None):
    if roster.value is None:
        return
    
    questions = roster.value.questions()
    with solara.Columns([1,1]):
        with solara.Column():
            QuestionSummary(questions, sid = sid)
           
