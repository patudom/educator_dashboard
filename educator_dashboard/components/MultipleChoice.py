import solara

import reacton.ipyvuetify as rv

from pandas import DataFrame, Series, concat
from ..database.Query import QueryCosmicDSApi as Query
import plotly.express as px
from .Collapsable import Collapsable

from .TableComponents import DataTable

from numpy import hstack


def MultipleChoiceStageSummary(roster, stage = None):
    
    selected_question = solara.use_reactive('')
    
    mc_responses = roster.value.multiple_choice_questions()
        

    flat_mc_responses = {}
    q = roster.value.l2d(mc_responses[stage],fill_val={})
    for k, v in q.items():
        flat_mc_responses[k] = roster.value.l2d(v)
        # flat_mc_responses[k]['Stage'] = stage
        flat_mc_responses[k]['Question'] = roster.value.question_keys()[k]['shorttext']
        flat_mc_responses[k]['key'] = k
        flat_mc_responses[k]['student_id'] = roster.value.student_ids

    summary_stats = DataFrame(flat_mc_responses).T
    tries = summary_stats['tries']
    # N = tries.aggregate(len)
    attempts = tries.aggregate(lambda x: f"{len([i for i in x if i is not None])} / {len(x)}")
    avg_tries = tries.aggregate(lambda x: sum([i for i in x if i is not None])/len([i for i in x if i is not None]))
    summary_stats['Completed by'] = attempts
    summary_stats['Average # of Tries'] = avg_tries.round(2)
    
    def cell_action(column, row_index):
        selected_question.set(summary_stats['key'].iloc[row_index])
    

    # solara.Select(label = "Question", values = list(stage_qs.keys()), value = quest)
    with solara.Card():
        solara.Markdown(f"### Stage {stage}")
        with solara.Columns([1,1]):
            
            # column with a table of questions with average #of tries
            with solara.Column():
                
                tries_1d = hstack(tries)
                # drop None values
                tries_1d = Series(tries_1d).dropna()
                solara.Markdown("Students on average took {} tries to complete the multiple choice questions".format(tries_1d[tries_1d>0].mean().round(2)))
                

                keys = ['Question', 'Completed by', 'Average # of Tries']
                
                
                data_keys = ['Question', 'Completed by', 'Average # of Tries', 'key']
                data_values = {k: summary_stats[k].astype(str) for k in data_keys}
                # https://www.phind.com/search?cache=qn70q6onf78gz5b035fmmosx
                data_values = [dict(zip(data_values.keys(), values)) for values in zip(*data_values.values())]

                # headers appropriate for vuetify headers prop
                headers = [{'text': k, 'value': k} for k in keys]
                
                
                def on_change(v):
                    if v is None:
                        selected_question.set(None)
                        return
                    
                    q = v['key']
                    selected_question.set(q)
                    
                
                
                DataTable(
                    headers=headers,
                    items=data_values,
                    on_row_click=on_change,
                )
            
            # a column for a particular question showing all student responses
            with solara.Column():
                if (selected_question.value is not None) and (selected_question.value != '') and (selected_question.value in flat_mc_responses.keys()):
                    
                    solara.Markdown(f"""***Question:***
                                {roster.value.question_keys()[selected_question.value]['text']}
                                """)
                    
                    df = DataFrame(flat_mc_responses[selected_question.value])
                    fig = px.histogram(df, 'tries',  labels={'tries': "# of Tries"}, range_x=[-0.6,3.6], category_orders={'tries': [0,1,2,3,4]})
                    fig.update_xaxes(type='category')
                    solara.FigurePlotly(fig)
                    
                    with Collapsable(header='Show Table'):
                        DataTable(df = df[['student_id', 'tries']], class_ = "mc-question-summary-table")
                    
@solara.component
def MultipleChoiceSummary(roster):
        
    mc_responses = roster.value.multiple_choice_questions()
    
    # mc_responses is a dict that looks like {'1': [{q1: {tries:0, choice: 0, score: 0}...}..]}
    stages = list(filter(lambda s: s.isdigit(),sorted(list(sorted(mc_responses.keys())))))
    
    for stage in stages:
        MultipleChoiceStageSummary(roster, stage = stage)

@solara.component
def MultipleChoiceQuestionSingleStage(df = None, headers = None, stage = 0):
    
    if df is None:
        return
    
    if isinstance(df, solara.Reactive):
        df = df.value
    
    dquest, set_dquest = solara.use_state('')
   
    
    def row_action(row):
        key = row['key']
        stage = row['stage']
        
        qjson = Query.get_question(key)
        if qjson is not None:
            q = qjson['question']['text']
            set_dquest(q)
        

    
    # which columns do you want to see and what should the displayed name be?
    headers = headers or [{'text': k, 'value': k} for k in df.columns]


    completed = sum(df.score.notna())
    total = len(df)
    points = sum(df.score.dropna().astype(int))
    total_points = 10 * total
    def isgood(i):
        return (i is not None) and (i != 0)
    avg_tries = df.tries.aggregate(lambda x: sum([i for i in x if isgood(i)])/len([i for i in x if isgood(i)]))
    
    with solara.Card():
        with solara.Columns([1,1]):
            with solara.Column():
                solara.Markdown("""
                                ### Stage {}
                                - Completed {} out of {} multiple choice questions
                                - Multiple Choice Score: {}/{}
                                - Took on average {:0.2f} tries to complete the multiple choice questions
                                """.format(stage, completed, total, points, total_points, avg_tries))    
                
            with solara.Column():
                if dquest is not None:
                    solara.Markdown(f"**Question**: {dquest}")
                
                DataTable(df = df, headers = headers, on_row_click=row_action)
            

        
    
@solara.component
def MultipleChoiceQuestionSingleStudent(roster, sid = None):
    
    if not isinstance(sid, solara.Reactive):
        sid = solara.use_reactive(sid)

    if sid.value is None:
        return
 
    idx = roster.value.student_ids.index(sid.value)
    mc_questions = roster.value.roster[idx]['story_state']['mc_scoring']
    
    
    dflist = []
    for stage, v in mc_questions.items():

        
        df = DataFrame(v).T
        df['stage'] = stage
        df['key'] = df.index
        df['question'] = [roster.value.question_keys()[k]['shorttext'] for k in df.key]
        dflist.append(df)
        
        # which columns do you want to see and what should the displayed name be?
        headers = [
            {'text': 'Question', 'value': 'question'},
            {'text': 'Tries', 'value': 'tries'},
            {'text': 'Score', 'value': 'score'},
        ]

        MultipleChoiceQuestionSingleStage(df = df, headers = headers, stage = stage)
            
