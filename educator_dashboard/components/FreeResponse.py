import solara

from solara.alias import rv

## discriminate between blank answers from not reached vs not done
## free question row

@solara.component_vue('FreeResponseQuestion.vue')
def FreeResponseQuestion(question='', shortquestion='', responses=[], names = [],
                         hideShortQuestion = False, hideQuestion = False, hideResponses = False, hideName = False):
    """
    free_response = {
        'question': '',
        'shortquestion': '',
        'responses': ['','','']
    }
    """


@solara.component
def FreeResponseQuestionResponseSummary(question_responses, question_text, names = None,
                                        hideShortQuestion = False, hideQuestion = False, hideResponses = False, hideName = False
                                        ):
    """
    question_responses = {'key': ['response1', 'response2',...]}
    question_text = {'key': {'text': 'question text', 
                             'shorttext': 'short question text', 
                             'nicetag': 'nicetag'
                            }}
    names = ['name1', 'name2',...] with same length as question_responses['key']
    """
    

    
    selected_question, set_selected_question = solara.use_state(None)
    
    inv = {v['shorttext']:k for k,v in question_text.items()}
    # def set_quest2(val):
    #     set_selected_question(inv[val])
    
    
    # values = [question_text[k]['shorttext'] for k,v in question_responses.items()]    
    # solara.Select(label = "Question", values = values, value = selected_question, on_value = set_quest2)
    
    with rv.ExpansionPanels():
        for selected_question in question_responses.keys():
            # set_selected_question(k)
            if selected_question is not None:
                question = question_text[selected_question]['text']
                shortquestion = question_text[selected_question]['shorttext']
                try:
                    responses = question_responses[selected_question]
                except:
                    responses = []
                
                with rv.ExpansionPanel():
                    with rv.ExpansionPanelHeader():
                        solara.Markdown(f"**{shortquestion}**")
                    with rv.ExpansionPanelContent():
                        FreeResponseQuestion(question = question, 
                                             shortquestion = shortquestion, 
                                             responses = responses, 
                                             names = names,
                                             hideShortQuestion = hideShortQuestion, 
                                             hideQuestion = hideQuestion, 
                                             hideResponses = hideResponses,
                                             hideName = hideName)


@solara.component
def FreeResponseSummary(roster, stage_labels=[]):
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return
        
    fr_questions = roster.free_response_questions()
    
    question_text = roster.question_keys() # {'key': {'text': 'question text', 'shorttext': 'short question text'}}
    
    stages = list(filter(lambda s: s.isdigit(),sorted(fr_questions.keys())))
    

    with solara.Columns([5, 1], style={"height": "100%"}):
        with solara.Column():
            for stage in stages:
                index = int(stage) - 1
                label = stage_labels[index]
                question_responses = roster.l2d(fr_questions[stage]) # {'key': ['response1', 'response2',...]}
                with rv.Container(id=f"fr-summary-stage-{stage}"):
                    solara.Markdown(f"### Stage {stage}: {label}")
                    FreeResponseQuestionResponseSummary(question_responses, question_text, names = roster.student_names, hideShortQuestion=True)
        with solara.Column():
            with rv.NavigationDrawer(permanent=True, right=True, clipped=True):
                with rv.List():
                    for stage in stages:
                        with rv.ListItem(link=True, href=f"#fr-summary-stage-{stage}"):
                            with rv.ListItemTitle():
                                solara.Markdown(f"Stage {stage}")
            
        

@solara.component
def FreeResponseQuestionSingleStudent(roster, sid = None, stage_labels=[]):
    
    if sid is None:
        return 
        
    
    if not isinstance(sid, solara.Reactive):
        sid = solara.use_reactive(sid)
    
    if isinstance(roster, solara.Reactive):
        roster = roster.value
        if roster is None:
            return
    
    # grab index for student    
    idx = roster.student_ids.index(sid.value)
    
    
    fr_questions = roster.roster[idx]['story_state']['responses']   

    question_text = roster.question_keys() # {'key': {'text': 'question text', 'shorttext': 'short question text', nicetag: 'nicetag'}}
    
    
    if len(fr_questions) == 0:
        solara.Markdown("Student has not answered any free response questions yet.")
    for k, v in fr_questions.items():
        index = int(k) - 1
        label = stage_labels[index]
        solara.Markdown(f"### Stage {k}: {label}")
        for qkey, qval in v.items():
            question = question_text[qkey]['text']
            shortquestion = question_text[qkey]['shorttext']
            responses = qval
            FreeResponseQuestion(question = question, 
                                shortquestion = shortquestion, 
                                responses = responses, 
                                hideShortQuestion = True,
                                hideName = True
                                )
        