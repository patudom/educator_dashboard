import solara

@solara.component_vue("MultiStepProgressBar.vue")
def MultiStepProgressBar(
    steps = None,
    currentStep = None,
    currentStepProgress = None,
    height = None,
    gap="0px",
    ): pass
    
