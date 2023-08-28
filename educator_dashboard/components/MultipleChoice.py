import solara
from solara.alias import rv

from pandas import DataFrame, Series, concat
from ..database.Query import QueryCosmicDSApi as Query
import plotly.express as px
from .Collapsable import Collapsable


@solara.component
def MCSummaryPart(stage_qs):
    """
    stage_qs is a dictionary of questions and tries
     = {q1: {tries:0, choice: 0, score: 0}...}
    """
    
    quest = solara.use_reactive(None)
    
    # solara.Select(label = "Question", values = list(stage_qs.keys()), value = quest)
    with solara.Columns([1,1]):
        
        # column with a table of questions with average #of tries
        with solara.Column():
            pass
        
        # a column for a particular question showing all student responses
        with solara.Column():
            pass
        
    for q in stage_qs.keys():
        quest.set(q)
        solara.Markdown(f"**Question {quest}**")
        
        df = DataFrame(stage_qs[quest.value]).dropna()
        df['tries'] = df['tries'].astype(int)
        # fig = px.histogram(df, 'tries',  labels={'tries': "# of Tries"}, range_x=[-0.6,3.6], category_orders={'tries': [0,1,2,3,4]})
        # fig.update_xaxes(type='category')
        # solara.FigurePlotly(fig)
    
# @solara.component
# def MCSummaryTable(questions, tries):
    

@solara.component
def MultipleChoiceSummary(roster):
    
    selected_question = solara.use_reactive('')
    
    mc_responses = roster.value.multiple_choice_questions()
    
    # mc_responses is a dict that looks like {'1': [{q1: {tries:0, choice: 0, score: 0}...}..]}
    stages = list(filter(lambda s: s.isdigit(),sorted(list(sorted(mc_responses.keys())))))
    
    flat_mc_responses = {}
    
    for stage in stages:
        q = roster.value.l2d(mc_responses[stage],fill_val={})
        for k, v in q.items():
            flat_mc_responses[k] = roster.value.l2d(v)
            flat_mc_responses[k]['Stage'] = stage
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
    with solara.Columns([1,1]):
        
        # column with a table of questions with average #of tries
        with solara.Column():
            
            solara.DataFrame(summary_stats[['Stage', 'Question', 'Completed by', 'Average # of Tries']], 
                             items_per_page=len(summary_stats),
                             cell_actions=[solara.CellAction(name='Show Question Stats', icon='mdi-table-eye', on_click=cell_action)]
                             )
        
        # a column for a particular question showing all student responses
        with solara.Column():
            if (selected_question.value is not None) and (selected_question.value != ''):
                
                solara.Markdown(f"""***Question:***
                            {roster.value.question_keys()[selected_question.value]['text']}
                            """)
                
                df = DataFrame(flat_mc_responses[selected_question.value])
                fig = px.histogram(df, 'tries',  labels={'tries': "# of Tries"}, range_x=[-0.6,3.6], category_orders={'tries': [0,1,2,3,4]})
                fig.update_xaxes(type='category')
                solara.FigurePlotly(fig)
                solara.DataFrame(df[['student_id', 'tries']])
    
    
@solara.component
def MultipleChoiceQuestionSingleStudent(roster, sid = None):
    
    if not isinstance(sid, solara.Reactive):
        sid = solara.use_reactive(sid)

    if sid.value is None:
        return
    
    dquest, set_dquest = solara.use_state(None)
    
    idx = roster.value.student_ids.index(sid.value)
    mc_questions = roster.value.roster[idx]['story_state']['mc_scoring']
    # {stage: {q1: {tries:0, choice: 0, score: 0}..., }
    
    
    
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
    
    dflist = []
    for stage, v in mc_questions.items():
        df = DataFrame(v).T
        df['stage'] = stage
        df['key'] = df.index
        df['question'] = [roster.value.question_keys()[k]['shorttext'] for k in df.key]
        dflist.append(df)

        # mc_df = concat(dflist,axis=0)
        mc_df = df
        df = mc_df[['key', 'question','stage', 'tries','score']]


        completed = sum(df.score.notna())
        total = len(df)
        points = sum(df.score.dropna().astype(int))
        total_points = 10 * total
        
        with solara.Card():
            with solara.Columns([1,1]):
                with solara.Column():
                    solara.Markdown("""
                                    ## Stage {} </br>
                                    Student completed {} out of {} multiple choice questions </br> Multiple Choice Score: {}/{}
                                    """.format(stage, completed, total, points, total_points))    

                    df_nona = df.dropna()
                    df_nona['tries'] = df_nona['tries'].astype(int)
                    fig = px.histogram(df_nona, 'tries', hover_data= ['question'], labels={'tries': "# of Tries"}, range_x=[-0.6,3.6], category_orders={'tries': [0,1,2,3,4]})
                    fig.update_xaxes(type='category')
                    solara.FigurePlotly(fig)
                    # solara.DataFrame(df.dropna())
                    
                with solara.Column():
                    if dquest is not None:
                        solara.Markdown(f"**Question**: {dquest}")
                    solara.DataFrame(df, items_per_page=len(df), cell_actions=mc_cell_actions)
            
