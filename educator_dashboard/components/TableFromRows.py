import solara 

   
@solara.component_vue('TableFromRows.vue', vuetify=True)
def TableFromRows(children = [], headers = None, select_key = None, selected = None): 
    """
    build a table from a sequence of rows
    the rows should be solara components which
    return an HTML table row
    with the same number of columns as the headers
    
    """
    pass