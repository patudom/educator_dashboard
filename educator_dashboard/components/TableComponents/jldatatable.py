import solara

import reacton.ipyvuetify as rv
import ipyvuetify as v

from traitlets import Unicode, List, Dict, Int, Bool, Instance, Any
import os

# stolen from solara/datatypes.py (thanks Maarten!)
import dataclasses
def _ensure_dict(d):
    if dataclasses.is_dataclass(d):
        return dataclasses.asdict(d)
    return d

def _drop_keys_from_list_of_mappings(drop):
    def closure(list_of_dicts, widget):
        return [{k: v for k, v in _ensure_dict(d).items() if k not in drop} for d in list_of_dicts]
    return closure



@solara.component
def vDataTableWrapper(df = None, headers = None, items = None, on_row_click = lambda *args: None,  **kwargs):
    """
    on_row_click should 1 argument which will be the row that was clicked
    
    """
    
    if df is not None:
        headers = headers or [{'text': h, 'value': h} for h in df.columns]
        items = items or df.to_dict('records')
    
    table = rv.DataTable(
        headers=headers,
        items=items,
        **kwargs
    )
    
    def on_click_row(*args):
        on_row_click(args[-1])
    
    rv.use_event(table,'click:row', on_click_row)
    
    return table



# Make a new component that creates a simple v-data-table which has a row click event and 
# keeps the selected row highlighted

class _DataTableHighlight(v.VuetifyTemplate):
    template_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "DataTable.vue"))
    headers = List(Dict()).tag(sync=True)
    items = List(Dict()).tag(sync=True)
    itemKey = Unicode().tag(sync=True)
    singleSelect = Bool().tag(sync=True)
    callbacks = List(Instance(solara.CellAction), default = []).tag(sync=True, to_json=_drop_keys_from_list_of_mappings(['on_click']))
    disable_pagination = Bool(default_value=True).tag(sync=True)
    selected = Any(default = None).tag(sync=True)
    highlight = Bool(default_value=True).tag(sync=True)
    deselect = Bool(default_value=True).tag(sync=True)
    
    def vue_on_click(self,data):
        self.callbacks[0].on_click(data)
    

@solara.component
def DataTableHighlight(headers = None, items = None, itemKey = None, singleSelect = True, on_click = lambda *args: None):


    cell_actions = [solara.CellAction(name=None, icon="mdi-account-details",on_click=on_click)]

    
    el = _DataTableHighlight.element(
        headers=headers,
        items=items,
        itemKey=itemKey,
        singleSelect=singleSelect,
        callbacks = cell_actions) 
    
    return el
    




@solara.component
def DataTableWithRowClick(headers = None, items = None, df = None, item_key = None, on_row_click = lambda *args: None, class_ = None, **kwargs):
    """
    on_row_click takes 1 arguments: the row that was clicked
    
    """
    
    if df is not None:
        headers = headers or [{'text': h, 'value': h} for h in df.columns]
        items = items or df.astype(str).to_dict('records')
    
    headers = [{'text': '#', 'value': 'id'}] + headers
    items = [{**item, 'id': str(i+1)} for i, item in enumerate(items)]
    
    item_key = item_key or 'id'
    
    def on_click(data):
        # print(data)
        on_row_click(data)
        
    table = DataTableHighlight(headers=headers, 
                               items=items, 
                               itemKey=item_key, 
                               on_click=on_click)
    

    return table
