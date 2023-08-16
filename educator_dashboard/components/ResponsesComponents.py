import solara

# equivalent to from reacton import ipyvuetify as rv
from solara.alias import rv
from pandas import DataFrame

# from solara.components.dataframe import HistogramCard
from ..database.Query import QueryCosmicDSApi as Query

from .Collapsable import Collapsable

import re

import solara.express as px

@solara.component
def QuestionSummary(df = None, sid = None):
    """
    Show response summary for entire class
    """
    solara.Markdown(""">The question summary shows the number of attempts for each multiple choice question and response for each free response question. 
                        A **0** means the question was skipped. A &lt;NA&gt; means the question was not seen by the student (some questions are optional).""")
    if isinstance(df, solara.Reactive):
        solara.DataFrame(df.value, scrollable=True)
    else:
        solara.DataFrame(df, scrollable=True)


@solara.component
def FreeResponseQuestionSingleStudent(fr_questions):
    dquest, set_dquest = solara.use_state(None)
    
    def fr_cell_action(column, row_index):
        tag = fr_questions['tag'].iloc[row_index]
        # take everything after first period, there may be more than 1
        if '.' in tag:
            tag = tag.split('.', 1)[1]
        qjson = Query.get_question(tag)
        if qjson is not None:
            q = qjson['question']['text']
            set_dquest(q)
        
    fr_cell_actions = [solara.CellAction('Show Question', icon='mdi-help-box', on_click=fr_cell_action)]
    
    solara.Markdown('## Free Responses')
    if dquest is not None:
        solara.Markdown(f"**Question**: {dquest}")
    solara.DataFrame(fr_questions[['Question','Answer']], cell_actions=fr_cell_actions)
    
@solara.component
def MultipleChoiceQuestionSingleStudent(mc_questions):
    dquest, set_dquest = solara.use_state(None)
    
    def mc_cell_action(column, row_index):
        tag = mc_questions['tag'].iloc[row_index]
        # take everything after first period, there may be more than 1
        if '.' in tag:
            tag = tag.split('.')[1]
        qjson = Query.get_question(tag)
        if qjson is not None:
            q = qjson['question']['text']
            set_dquest(q)
        
    mc_cell_actions = [solara.CellAction('Show Question', icon='mdi-help-box', on_click=mc_cell_action)]
    
    solara.Markdown('')

    df = DataFrame()

    tag = mc_questions.tag
    df['question'] = mc_questions.question[::3]
    df['score'] = mc_questions['value'][tag.str.contains('score')].values
    df['tries'] = mc_questions['value'][tag.str.contains('tries')].values
    df['choice'] = mc_questions['value'][tag.str.contains('choice')].values
    # df['tag'] = mc_questions['tag'][tag.str.contains('choice')].values

    completed = sum(df.score.notna())
    total = len(df)
    points = sum(df.score.dropna().astype(int))
    total_points = 10 * total
    solara.Markdown("""
                    ## Multiple Choice
                    Student completed {} out of {} multiple choice questions </br> Multiple Choice Score: {}/{}
                    """.format(completed, total, points, total_points))    

    df_nona = df.dropna()
    df_nona['tries'] = df_nona['tries'].astype(int)
    fig = px.histogram(df_nona, 'tries', custom_data= ['question'], labels={'tries': "# of Tries"})
    # solara.DataFrame(df.dropna())
    
    with Collapsable(header='Show Question Table'):
        if dquest is not None:
            solara.Markdown(f"**Question**: {dquest}")
        solara.DataFrame(df, items_per_page=len(df), cell_actions=mc_cell_actions)
    


@solara.component
def StudentQuestion(dataframe = None):
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
    fr_questions = table[table.tag.apply(lambda x: len(str(x).split('.'))==2)]
    
    fr_questions = fr_questions.rename(columns={'value': 'Answer', 'question': 'Question'})
    
    
    
    # multiple choice questions
    with solara.Columns([1,1]):
        with solara.Column():
            MultipleChoiceQuestionSingleStudent(mc_questions)
            
        with solara.Column():
            FreeResponseQuestionSingleStudent(fr_questions)
        

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
    if qtags is not None:
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
    short_qs =  list(map(lambda x: qkeys.get(x.split('.')[1])['shorthand'] , qtags))
    replacements = dict(zip(qtags, short_qs))
    questions = questions.rename(columns = replacements)
    
    sids = [int(s) for s in questions['student_id'].to_list()]

    
    
    # with solara.lab.Tabs(
    #         value = 0 if (sid.value is None or sid.value not in sids) else sids.index(sid.value), 
    #         on_value = lambda x: sid.set(sids[x])
    #         ):
    #     for i, row in questions.iterrows(): 
            
            # with solara.lab.Tab(str(row['student_id'])):
    
    IndividualStudentResponsePanel(questions, qtags = qtags, sid = sid)


@solara.component
def StudentQuestionsSummary(roster, sid = None):
    if roster.value is None:
        return
    
    # we need to replace the tag with the short version of the question
    questions = roster.value.questions()
    # questions have a '.' because we flattened a nested json file
    qtags = [c for c in questions.columns if '.tries' in c]
    
    qkeys = roster.value.question_keys()
    
    replacements = dict(zip(qtags, map(lambda x: qkeys.get(x.split('.')[1])['shorthand'] , qtags)))
    replacements.update({'student_id': 'Student ID'})
    questions = questions[['student_id'] + qtags].rename(columns = replacements)
    
    with solara.Columns([1,1]):
        with solara.Column():
            QuestionSummary(questions, sid = sid)
           
