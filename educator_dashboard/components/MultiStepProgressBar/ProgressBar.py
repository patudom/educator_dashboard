import solara


@solara.component_vue("ProgressBar.vue")
def ProgressBar(progress=None, 
                backgroundColor=None,
                unfiledColor=None,
                height='20px'
                ):
    pass