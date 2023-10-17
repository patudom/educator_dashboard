import solara

import reacton.ipyvuetify as rv

import pandas as pd
from pandas import DataFrame, Series
from ..database.Query import QueryCosmicDSApi as Query
import plotly.express as px
from .Collapsible import Collapsible

from .TableComponents import DataTable

from numpy import hstack, around

@solara.component
def MultipleChoiceStageSummary(roster, stage = None, label= None):
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return
    
    selected_question = solara.use_reactive('')
    
    mc_responses = roster.multiple_choice_questions()
        

    flat_mc_responses = {}
    q = roster.l2d(mc_responses[stage],fill_val={})
    for k, v in q.items():
        flat_mc_responses[k] = roster.l2d(v)
        # flat_mc_responses[k]['Stage'] = stage
        flat_mc_responses[k]['Question'] = roster.question_keys()[k]['shorttext']
        flat_mc_responses[k]['key'] = k
        flat_mc_responses[k]['student_id'] = roster.student_ids

    summary_stats = DataFrame(flat_mc_responses).T
    tries = summary_stats['tries']
    # N = tries.aggregate(len)
    attempts = tries.aggregate(lambda x: f"{len([i for i in x if i is not None])} / {len(x)}")
    avg_tries = tries.aggregate(lambda x: sum([i for i in x if i is not None])/len([i for i in x if i is not None]))
    summary_stats['Completed by'] = attempts
    summary_stats['Average # of Tries'] = avg_tries.round(2)
    
    tries_1d = hstack(tries)
    tries_1d = Series(tries_1d).dropna()
    
    with solara.GridFixed(columns=1, justify_items='stretch', align_items='start') as main:
        solara.Markdown(f"### Stage {stage}: {label}")

        # Table of questions with average #of tries across whole space
        with solara.Column():
            
            avg_tries = around(tries_1d[tries_1d>0].mean(),2)
            solara.Markdown("Students on average took {} tries to complete the multiple choice questions".format(avg_tries))

            keys = ['Question', 'Completed by', 'Average # of Tries']
            # headers appropriate for vuetify headers prop
            headers = [{'text': k, 'value': k} for k in keys]
            
            
            data_keys = ['Question', 'Completed by', 'Average # of Tries', 'key']
            
            # https://www.phind.com/search?cache=qn70q6onf78gz5b035fmmosx
            data_values = {k: summary_stats[k].astype(str) for k in data_keys}
            data_values = [dict(zip(data_values.keys(), values)) for values in zip(*data_values.values())]


            def on_change(v):                    
                selected_question.set(v if v is None else v['key'])
            
            DataTable(
                headers=headers,
                items=data_values,
                on_row_click=on_change,
                show_index=True,
                class_ = "mc-question-summary-table"
            )

        with solara.Columns([1,1]):
            if (selected_question.value is not None) and (selected_question.value != '') and (selected_question.value in flat_mc_responses.keys()):
            
                # a column for a particular question showing all student responses
                with solara.Column():
                        # Add numeral index after Question
                        solara.Markdown(f"""***Question:***
                                    {roster.question_keys()[selected_question.value]['text']}
                                    """)
                        
                        df = DataFrame(flat_mc_responses[selected_question.value])
                        fig = px.histogram(df, 'tries',  labels={'tries': "# of Tries"}, range_x=[-0.6,3.6], category_orders={'tries': [0,1,2,3,4]})
                        fig.update_xaxes(type='category')
                        solara.FigurePlotly(fig)
                                        
                with Collapsible(header='Individual Student Tries for Question'):
                    # Round tries to integers and leave a blank for nan values
                    df['rounded_tries'] = df['tries'].round().astype('Int64')
                    df['rounded_tries'] = df['rounded_tries'].apply(lambda x: '' if pd.isna(x) else x)

                    if 'name' in roster.students.columns:
                        headers = [{'text': 'Name', 'value': 'name'}, {'text': 'Tries', 'value': 'rounded_tries'}]
                        # add names to df
                        df = df.merge(roster.students[['student_id', 'name']], on='student_id', how='left')
                    else:
                        headers = [{'text': 'Student ID', 'value': 'student_id'}, {'text': 'Tries', 'value': 'rounded_tries'}]
                    DataTable(df = df, headers = headers, item_key = 'student_id', class_ = "mc-question-students-table")
        rv.Divider()
    return main

                
@solara.component
def MultipleChoiceSummary(roster, stage_labels=[]):
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return
        
    mc_responses = roster.multiple_choice_questions()
    
    # mc_responses is a dict that looks like {'1': [{q1: {tries:0, choice: 0, score: 0}...}..]}
    stages = list(filter(lambda s: s.isdigit(),sorted(list(sorted(mc_responses.keys())))))
    
    for stage in stages:
        index = int(stage) - 1
        label = stage_labels[index]
        MultipleChoiceStageSummary(roster, stage = stage, label = label)

@solara.component
def MultipleChoiceQuestionSingleStage(df = None, headers = None, stage = 0, label = None):
    
    if df is None:
        solara.Markdown("There are no completed multiple choice questions for this stage")
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
    
    def avg(x):
        top = sum([i for i in x if isgood(i)])
        bot = len([i for i in x if isgood(i)])
        if bot == 0:
            return '--'
        return str(round(top/bot,2))
    
    avg_tries = df.tries.aggregate(avg)
    

    with solara.Row():
        solara.Markdown("""
                        ### Stage {}: {}
                        - Completed {} out of {} multiple choice questions
                        - Multiple Choice Score: {}/{}
                        - Took on average {} tries to complete the multiple choice questions
                        """.format(stage, label,  completed, total, points, total_points, avg_tries))    
        
    with solara.Row():
        with solara.Columns([1,1]):
            with solara.Column():
                if len(dquest)>0:
                    solara.Markdown(f"**Question**: {dquest}")
                else:
                    solara.Markdown(f"**Select a row from table to see full question text.** ")
            with solara.Column():
                DataTable(df = df, headers = headers, on_row_click=row_action, show_index=True, class_ = "mc-individual-student-table")
    rv.Divider()
            

        
    
@solara.component
def MultipleChoiceQuestionSingleStudent(roster, sid = None, stage_labels = []):
    
    if not isinstance(sid, solara.Reactive):
        sid = solara.use_reactive(sid)

    if sid.value is None:
        return
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return
 
    idx = roster.student_ids.index(sid.value)
    mc_questions = roster.roster[idx]['story_state']['mc_scoring']
    
    
    dflist = []
    for stage, v in mc_questions.items():
        index = int(stage) - 1
        label = stage_labels[index]
        
        df = DataFrame(v).T
        df['stage'] = stage
        df['key'] = df.index
        df['question'] = [roster.question_keys()[k]['shorttext'] for k in df.key]
        dflist.append(df)
        
        # which columns do you want to see and what should the displayed name be?
        headers = [
            {'text': 'Question', 'value': 'question'},
            {'text': 'Tries', 'value': 'tries'},
            {'text': 'Score', 'value': 'score'},
        ]
        MultipleChoiceQuestionSingleStage(df = df, headers = headers, stage = stage, label = label)
            
