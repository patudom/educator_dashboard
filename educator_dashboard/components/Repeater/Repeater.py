import solara

import reacton.ipyvuetify as rv
import ipyvuetify as v

from traitlets import Unicode, List, Dict, Int, Bool, Instance, Any

import os

import inspect

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


class _vRepeater(v.VuetifyTemplate):
    template_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "Repeater.vue"))
    # props
    
    # - settings
    periodInMilliseconds = Int(default_value=5 * 60 * 1000).tag(sync=True)
    maxRepeat = Int(default_value=10).tag(sync=True)
    
    # - UI options
    manualRefresh = Bool(default_value=True).tag(sync=True) # show manual refresh button
    stopStart = Bool(default_value=False).tag(sync=True) # show stop/start button
    
    # - styling
    manualRefreshColor = Unicode(default_value="grey").tag(sync=True)
    startColor = Unicode(default_value="#8FBC8F").tag(sync=True)
    stopColor = Unicode(default_value="#B22222").tag(sync=True)
    
    # callback
    callbacks = List(Instance(solara.CellAction), default_value=[]).tag(sync=True, to_json=_drop_keys_from_list_of_mappings(['on_click']))
    
    #data
    loopCount = Int(default_value=0).tag(sync=True)
    intervalId = Int(default_value=0).tag(sync=True)
    paused = Bool(default_value=False).tag(sync=True)

    
    def vue_on_refresh(self, data):
        for callback in self.callbacks:
            callback.on_click(data['loopCount'])
    

@solara.component
def _Repeater(periodInMilliseconds = 5 * 60 * 1000, 
             on_refresh = lambda _loopCount: None, 
             maxRepeat = 0,
             countdownStep = 1000,
             manualRefresh = False,
             stopStart = False,
             manualRefreshColor = "primary",
             startColor = "#ccc",
             stopColor = "#777",
             **kwargs
             ):
    
    
    cell_actions = [solara.CellAction(name=None, icon="mdi-refresh-circle",on_click=on_refresh)]
    
    repeater = _vRepeater.element(
        periodInMilliseconds = periodInMilliseconds,
        maxRepeat = maxRepeat,
        countdownStep = countdownStep,
        callbacks = cell_actions,
        manualRefresh = manualRefresh,
        stopStart = stopStart,
        manualRefreshColor = manualRefreshColor,
        startColor = startColor,
        stopColor = stopColor,
        **kwargs
        )    

    return repeater
        
@solara.component
def Repeater(periodInMilliseconds = 5 * 60 * 1000, 
           on_refresh = lambda _loopCount: None, 
           maxRepeat = 0,
           show_refresh_button = False,
           stop_start_button = False,
           buttonColor = "grey",
           **kwargs):
           
    """    
    Parameters
    ----------
    periodInMilliseconds : int, optional
        The time between refreshes, by default 5 * 60 * 1000 (30 seconds)
    on_refresh : function, optional
        A function that takes 1 argument, the loopCount, by default lambda _loopCount: None
    maxRepeat : int, optional
        The number of times to repeat, 0 means repeat forever, by default 0
    show_refresh_button : bool, optional
        Whether to show the manual refresh button, by default False
    stop_start_button : bool, optional
        Whether to show the stop/start button, by default False
    buttonColor : str, optional
        The color of the manual refresh button button, by default "grey". Use CSS compatible colors.
    
    Other Parameters
    ----------------
    Any other parameters are passed to the underlying Vue component. They are:
        - countdownStep: the number of milliseconds to count down by, by default 1000
        - startColor: the color of the start button, by default "#ccc" (light grey)
        - stopColor: the color of the stop button, by default "#777" (dark grey)
    """
    
    if len(inspect.getfullargspec(on_refresh).args) == 0:
        # the callback function must take at least 1 argument
        callback = lambda _loopCount: on_refresh()
    else:
        callback = on_refresh
    
    
    periodInMilliseconds = solara.use_reactive(periodInMilliseconds)
    
    return _Repeater(
        periodInMilliseconds = periodInMilliseconds.value,
        maxRepeat = maxRepeat,
        on_refresh = callback,
        manualRefresh = show_refresh_button,
        stopStart = stop_start_button,
        manualRefreshColor = buttonColor,
        **kwargs
        )
