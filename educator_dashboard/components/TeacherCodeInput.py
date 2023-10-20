import solara
from ..database.Query import QueryCosmicDSApi
import json
import reacton.ipyvuetify as rv
@solara.component 
def TeacherCodeEntry(class_id_list, class_id, callback, query = None):
    print('================== TeacherCodeEntry ==================')
    if query is None:
        query = QueryCosmicDSApi()
    code = solara.use_reactive('')
    class_id = solara.use_reactive(class_id)
    class_id_list = solara.use_reactive(class_id_list)
    proceed_to_dashboard = solara.use_reactive(False)
    
    dev_mode = query.in_dev_mode()
    if dev_mode:
        # class_id_list.set([199, 200, 195, 192, 184, 188, 190, 191, 170, 172])
        class_query_res = [
                {'id': 199, 'name': 'Test Class 199'},
                {'id': 200, 'name': 'Test Class 200'},
                {'id': 195, 'name': 'Test Class 195'},
                {'id': 192, 'name': 'Test Class 192'},
                {'id': 184, 'name': 'Test Class 184'},
                {'id': 188, 'name': 'Test Class 188'},
                {'id': 190, 'name': 'Test Class 190'},
                {'id': 191, 'name': 'Test Class 191'},
                {'id': 170, 'name': 'Test Class 170'},
                {'id': 172, 'name': 'Test Class 170'},
             ]
        class_id_list.set(class_query_res)
        class_id.set(199)
        code.set('dev')
        solara.Markdown('In dev mode, so skipping code entry')
        proceed_to_dashboard.set(True)
        callback()
        # solara.Button(label="Continue to Dashboard", classes=["my-buttons"], on_click=callback, disabled=(not proceed_to_dashboard.value))
        return
        
    with solara.Card(style={'position':'absolute','top':'50%', 'left':'50%', 'transform':'translate(-50%, -50%)'}, classes=["pa-16"]):
        solara.Markdown('Please enter the code provided to you by the CosmicDS team')
        with solara.Row():
            solara.InputText(label="Educator Code", 
                             value=code, 
                             continuous_update=False,
                             message = f'You entered {code.value}',
                             )

        class_query_res = query.get_class_for_teacher(str(code.value))
        class_query_res = class_query_res.get('classes', {})
        if code.value != '' and len(class_query_res) == 0:
            solara.Error(f'No classes found for code {code.value}')
        elif code.value != '' and len(class_query_res) > 0:
            solara.Success(f'Found {len(class_query_res)} classes.')
            proceed_to_dashboard.set(True)
            class_id_list.set(class_query_res)
            # solara.Select(label="Select Class",values = class_id_list.value, value = class_id)

            rv.Select(label='Select item',
                    items=class_id_list.value, 
                    item_text = 'name',
                    item_value = 'id',
                    v_model=class_id.value, 
                    on_v_model=class_id.set
                    )
            
        
        
        if class_id.value is not None:
            print(f'class id is {class_id.value}')
            solara.Button(label="Continue to Dashboard", classes=["my-buttons"], on_click=callback, disabled=(not proceed_to_dashboard.value))

