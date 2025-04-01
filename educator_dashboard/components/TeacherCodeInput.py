import solara
from ..database.Query import QueryCosmicDSApi
import json
import reacton.ipyvuetify as rv
from typing import Optional

from ..logger_setup import logger
from ..class_report import Roster
from solara.reactive import Reactive

class_query_res = [
    # {'id': 172, 'name': '172: Stress test + New Teachers'},
    # {'id': 204, 'name': '204: HubbleDS PR291'},
    # {'id': 280, 'name': '270'},
    # {'id': 214, 'name': '214'},
    {'id': 212, 'name': '212: 2024-01-04 stress test'},
    {'id': 211, 'name': '211: 2023-12-13 SED test'},
    {'id': 209, 'name': '209: 2023-12-05 Summative Class 6'},
    {'id': 207, 'name': '207: 2023-12-04 Summative Class 5'},
    {'id': 206, 'name': '206: 2023-11-29 Summative Class 4'},
    # {'id': 205, 'name': '205: 2023-11-29 Summative Class 3'},
    # {'id': 203, 'name': '203: 2023-11-16 Summative Class 2'},
    # {'id': 202, 'name': '202: 2023-11-16 Summative Class 1'},
    # {'id': 201, 'name': 'HubbleDS PR302 Small Test 201'},  1 person class   
    # {'id': 200, 'name': '200: sample_class_1'}, these were rolled into 199
    {'id': 199, 'name': '199: Ed Dashboard Sample Class'},
    {'id': 215, 'name': '215: Solara Test Class'},
    # {'id': 216, 'name': '216: Lewis Class'},
    {'id': 282, 'name': '282: Lewis Test Class'},
    {'id': 286, 'name': '286: Lewis Empty Class'}, 
    # {'id': 197, 'name': '197: betaclass3'},
    # {'id': 196, 'name': '196: pat-local-test'},
    # {'id': 195, 'name': '195: 2023-07 Formative Class 6'},
    # {'id': 194, 'name': '194: 2023-07 2i2c_beta'},
    # {'id': 193, 'name': '193: 2023-07 Pat Test Class'},
    # {'id': 192, 'name': '192: Empty Class'},                
    # {'id': 191, 'name': '191: No data test'},
    # {'id': 190, 'name': '190: 2023-05-10 Formative Class 5'},
    # {'id': 188, 'name': '188: 2023-05-10 Formative Class 4'},
    # {'id': 189, 'name': '189'},
    # {'id': 185, 'name': '185: Beta2 Test Class 2'}, 
    # {'id': 184, 'name': '184: 2023-05-08 Formative Class 3'},
    # {'id': 179, 'name': '179: Pat\'s Test Class'}, 
    # {'id': 178, 'name': '178: 2022-10-25 Formative Class 2'}, 
    # {'id': 177, 'name': '177: 2022-10-25 Formative Class 1'},         
    ]

@solara.component 
def TeacherCodeEntry(class_id_list, class_id, callback, query = None, roster: Reactive[Roster] | Roster = None):
    logger.debug('================== TeacherCodeEntry ==================')
    if query is None:
        query = QueryCosmicDSApi()
    code = solara.use_reactive('')
    class_id = solara.use_reactive(class_id)
    class_id_list = solara.use_reactive(class_id_list)
    proceed_to_dashboard = solara.use_reactive(False)
    
    dev_mode = query.in_dev_mode()
    if dev_mode:
        # class_id_list.set([199, 200, 195, 192, 184, 188, 190, 191, 170, 172])
        
        class_id_list.set(class_query_res)
        class_id.set(282)
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
            logger.debug(f'class id is {class_id.value}')
            solara.Button(label="Continue to Dashboard", classes=["my-buttons"], on_click=callback, disabled=(not proceed_to_dashboard.value))

