import solara
from ..database.Query import QueryCosmicDSApi

import reacton.ipyvuetify as rv
@solara.component 
def TeacherCodeEntry(class_id_list, class_id, callback):
    print('================== TeacherCodeEntry ==================')
    q = QueryCosmicDSApi()
    code = solara.use_reactive('')
    class_id = solara.use_reactive(class_id)
    class_id_list = solara.use_reactive(class_id_list)
    proceed_to_dashboard = solara.use_reactive(False)
    with solara.Card(style={'position':'absolute','top':'50%', 'left':'50%', 'transform':'translate(-50%, -50%)'}, classes=["pa-16"]):
        solara.Markdown('Please enter the code provided to you by the CosmicDS team')
        with solara.Row():
            solara.InputText(label="Teacher Code", 
                             value=code, 
                             continuous_update=False,
                             message = f'You entered {code.value}',
                             )
        
        class_query_res = q.get_class_for_teacher(str(code.value))
        if code.value != '' and len(class_query_res) == 0:
            solara.Error(f'No classes found for code {code.value}')
        elif code.value != '' and len(class_query_res) > 0:
            solara.Success(f'Found {len(class_query_res)} classes for code {code.value}. {class_query_res}')
            proceed_to_dashboard.set(True)
            class_id_list.set(class_query_res)
            solara.Select(label="Select Class",values = class_id_list.value, value = class_id)
        
        
        if class_id.value is not None:
            print(f'class id is {class_id.value}')
            solara.Button(label="Continue to Dashboard", color='lime', on_click=callback, disabled=(not proceed_to_dashboard.value))

