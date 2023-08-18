import solara

from pandas import DataFrame
from ..database.Query import QueryCosmicDSApi as Query
import plotly.express as px
from .Collapsable import Collapsable

   
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
    fig = px.histogram(df_nona, 'tries', hover_data= ['question'], labels={'tries': "# of Tries"}, range_x=[-0.6,3.6], category_orders={'tries': [0,1,2,3,4]})
    fig.update_xaxes(type='category')
    solara.FigurePlotly(fig)
    # solara.DataFrame(df.dropna())
    
    with Collapsable(header='Show Question Table'):
        if dquest is not None:
            solara.Markdown(f"**Question**: {dquest}")
        solara.DataFrame(df, items_per_page=len(df), cell_actions=mc_cell_actions)
    
