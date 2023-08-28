import solara

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
    
    solara.Select(label = "Question", values = list(stage_qs.keys()), value = quest)
    if quest.value is not None:
            solara.Markdown(f"**Question {quest}**")
            
            df = DataFrame(stage_qs[quest.value]).dropna()
            df['tries'] = df['tries'].astype(int)
            fig = px.histogram(df, 'tries',  labels={'tries': "# of Tries"}, range_x=[-0.6,3.6], category_orders={'tries': [0,1,2,3,4]})
            fig.update_xaxes(type='category')
            solara.FigurePlotly(fig)
    

@solara.component
def MultipleChoiceSummary(roster):
    
    
    mc_responses = roster.value.multiple_choice_questions()
    
    # mc_responses is a dict that looks like {'1': [{q1: {tries:0, choice: 0, score: 0}...}..]}
    keys = list(sorted(mc_responses.keys()))
    
    stages = list(filter(lambda s: s.isdigit(),sorted(keys)))
    
    with solara.lab.Tabs():
        for stage in stages:
            with solara.lab.Tab(f"Stage {stage}"):
                if mc_responses[stage] is None:
                    continue
                
                solara.Markdown(f"### Stage {stage} ")
                
                stage_qs = roster.value.l2d(mc_responses[stage],fill_val={}) # {q1: {tries:0, choice: 0, score: 0}...}
                MCSummaryPart(stage_qs)


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
    
    with solara.Row():
        with solara.Column():
            dflist = []
            for stage, v in mc_questions.items():
                df = DataFrame(v).T
                df['stage'] = stage
                df['key'] = df.index
                df['question'] = [roster.value.question_keys()[k]['shorttext'] for k in df.key]
                dflist.append(df)

                mc_df = concat(dflist,axis=0)
                df = mc_df[['key', 'question','stage', 'tries','score']]


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
                fig = px.histogram(df_nona, 'tries', hover_data= ['question'], labels={'tries': "# of Tries"}, range_x=[-0.6,3.6], category_orders={'tries': [0,1,2,3,4]})
                fig.update_xaxes(type='category')
                solara.FigurePlotly(fig)
                # solara.DataFrame(df.dropna())
            
        with Collapsable(header='Show Question Table'):
            if dquest is not None:
                solara.Markdown(f"**Question**: {dquest}")
            solara.DataFrame(df, items_per_page=len(df), cell_actions=mc_cell_actions)
    
