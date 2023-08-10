import solara

@solara.component
def TableDisplay(*args, **kwargs):
    """
    Thin wrapper around solara.DataFrame
    """
    return solara.DataFrame(*args, **kwargs)


