import solara

from solara.alias import rv

from pandas import DataFrame


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
def FreeResponseQuestionResponseSummary(question_responses, question_text, names = None):
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
    def set_quest2(val):
        set_selected_question(inv[val])
    
    
    values = [question_text[k]['shorttext'] for k,v in question_responses.items()]    
    solara.Select(label = "Question", values = values, value = selected_question, on_value = set_quest2)
    
    # for k in stage_qs.keys():
    #     set_selected_question(k)
    if selected_question is not None:
        question = question_text[selected_question]['text']
        shortquestion = question_text[selected_question]['shorttext']
        try:
            responses = question_responses[selected_question]
        except:
            responses = []
        
        FreeResponseQuestion(question = question, shortquestion = shortquestion, responses = responses, names = names)


@solara.component
def FreeResponseSummary(roster):
    
    if not isinstance(roster, solara.Reactive):
        roster = solara.use_reactive(roster)
    
    df = roster.value.questions()
    # solara.DataFrame(df)
    
    fr_questions = roster.value.free_response_questions()
    
    question_text = roster.value.question_keys() # {'key': {'text': 'question text', 'shorttext': 'short question text'}}
    
    stages = list(filter(lambda s: s.isdigit(),sorted(fr_questions.keys())))
    
    with solara.lab.Tabs(grow=True):

        with solara.lab.Tab("Show All Responses"):
            # make dataframe just adds the student id as the first row
            fr_df = roster.value.make_dataframe(df[list(filter(lambda x: len(str(x).split('.'))==2, df.columns))], include_student_id = True,  include_class_id = False, include_username = False)
            solara.DataFrame(fr_df)
        
        with solara.lab.Tab("Show By Question"):
            with solara.lab.Tabs():
                for stage in stages:
                    with solara.lab.Tab(f"Stage {stage}"):
                        
                        solara.Markdown(f"## Stage {stage}")
                        
                        question_responses = roster.value.l2d(fr_questions[stage]) # {'key': ['repsonse1', 'response2',...]}
                        
                        FreeResponseQuestionResponseSummary(question_responses, question_text, names = roster.value.student_ids)
            
        

@solara.component
def FreeResponseQuestionSingleStudent(roster, sid = None):
    
    if sid is None:
        return 
    
    if not isinstance(sid, solara.Reactive):
        sid = solara.use_reactive(sid)
    
    if not isinstance(roster, solara.Reactive):
        roster = solara.use_reactive(roster)
    
    # grab index for student    
    idx = roster.value.student_ids.index(sid.value)
    
    
    fr_questions = roster.value.roster[idx]['story_state']['responses']   
    print(fr_questions)     
    question_text = roster.value.question_keys() # {'key': {'text': 'question text', 'shorttext': 'short question text', nicetag: 'nicetag'}}
    
    with solara.Card():
        solara.Markdown('Hello')
        for k, v in fr_questions.items():
            solara.Markdown(f"## Stage {k}")
            for qkey, qval in v.items():
                question = question_text[qkey]['text']
                shortquestion = question_text[qkey]['shorttext']
                responses = qval
                FreeResponseQuestion(question = question, 
                                    shortquestion = shortquestion, 
                                    responses = responses, 
                                    names = [sid.value])
        