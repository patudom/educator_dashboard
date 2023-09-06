import solara

@solara.component_vue('ProgressRow.vue')
def ProgressRow(column_data=None, 
                selected = False, 
                on_selected = None,
                steps = None,
                currentStep = None,
                currentStepProgress = None,
                height = None,
                gap="0px",
                ):
    pass