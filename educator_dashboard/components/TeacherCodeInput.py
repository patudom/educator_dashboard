import solara

import reacton.ipyvuetify as rv
@solara.component 
def TeacherCodeEntry(class_id_list, class_keys, callback):
    
    
    code = solara.use_reactive('')
    with solara.Card(style={'position':'absolute','top':'50%', 'left':'50%', 'transform':'translate(-50%, -50%)'}, classes=["pa-16"]):
        solara.Markdown('Please enter the code provided to you by the CosmicDS team')
        with solara.Row():
            solara.InputText(label="Teacher Code", 
                             value=code, 
                             continuous_update=True, 
                             error = not(str(code.value) in ['','188', '184']), 
                             message = f'{code} is not a valid code' if (not(str(code.value) in class_keys.keys())) else f'Code: {code} valid.' )
    
        class_id_list.set(class_keys.get(str(code.value), []))
    
        solara.Button(label="Continue to Dashboard", color='lime', on_click=callback, disabled=not(str(code.value) in class_keys.keys()))

