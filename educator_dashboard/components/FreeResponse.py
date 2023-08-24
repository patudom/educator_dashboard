import solara

from ..database.Query import QueryCosmicDSApi as Query

@solara.component_vue('FreeResponseQuestion.vue')
def FreeResponseQuestion(question='', shortquestion='', responses=[], names = []):
    """
    free_response = {
        'question': '',
        'shortquestion': '',
        'responses': ['','','']
    }
    """


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
