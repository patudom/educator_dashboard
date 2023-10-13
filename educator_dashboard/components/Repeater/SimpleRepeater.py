import solara

import ipyvuetify as v

from traitlets import List, Int, Bool, Instance

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

def _callback_wrapper(callback):
    argspec = inspect.getfullargspec(callback)
    if argspec.varargs is None:
        return lambda *_: callback()
    else:
        return callback
    
class _vSimpleRepeater(v.VuetifyTemplate):
    template_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "SimpleRepeater.vue"))
    # props
    
    # - settings
    periodInMilliseconds = Int(default_value=5 * 60 * 1000).tag(sync=True)
    maxRepeat = Int(default_value=10).tag(sync=True)
    reset = Bool(default_value=False).tag(sync=True)
    pause = Bool(default_value=False).tag(sync=True)
    showDebug = Bool(default_value=False).tag(sync=True)
    ping = Int(default_value=0).tag(sync=True) # this is a dummy variable to force the component to refresh. Increment it to refresh the component.

    # callback
    callbacks = List(Instance(solara.CellAction), default_value=[]).tag(sync=True, to_json=_drop_keys_from_list_of_mappings(['on_click']))
    
    #data
    loopCount = Int(default_value=0).tag(sync=True)
    intervalId = Int(default_value=0).tag(sync=True)
    done = Bool(default_value=False).tag(sync=True)
    
    # this emits events ['simple-repeat:reset', 'simple-repeat:pause', 'simple-repeat:unpause', 'simple-repeat:done']
    
    def vue_on_refresh(self, *args, **kwargs):
        # print(f"vue_on_refresh: args {args}, kwargs {kwargs}")
        for callback in self.callbacks:
            callback.on_click()
    

@solara.component
def _SimpleRepeater(periodInMilliseconds = 5 * 60 * 1000, 
             on_refresh = lambda _loopCount: None, 
             maxRepeat = 0,
             reset = False,
             pause = False,
             ping = 0,
             showDebug = False):
    
    periodInMilliseconds = solara.use_reactive(periodInMilliseconds)
    reset = solara.use_reactive(reset)
    pause = solara.use_reactive(pause)
    ping = solara.use_reactive(ping)
    showDebug = solara.use_reactive(showDebug)
    
    
    
    cell_actions = [solara.CellAction(name=None, icon="mdi-refresh-circle",on_click=on_refresh)]
    
    repeater = _vSimpleRepeater.element(
        periodInMilliseconds = periodInMilliseconds.value,
        maxRepeat = maxRepeat,
        callbacks = cell_actions,
        reset = reset.value,
        pause = pause.value,
        ping = ping.value,
        showDebug = showDebug.value)    
    
    # create event listeners
    # repeater.on_event('simple-repeat:reset', lambda *_: reset.set(True))
    
    return repeater
        
@solara.component
def SimpleRepeater(periodInMilliseconds = 5 * 60 * 1000, 
           on_refresh = lambda *_: None, 
           maxRepeat = 0,
           reset = False,
           pause = False,
           ping = 0,
           showDebug = False):
           
    """
    Simple repeater component that calls a function at regular intervals.
    Optionally, a refresh button can be shown to allow the user to manually refresh the component.
    
    Parameters
    ----------
    periodInMilliseconds : int or solara.Reactive(Int)
        the time between each refresh in milliseconds
    on_refresh : function
        the function to call when the refresh button is clicked or the timer is fired
        this function should take no arguments or varargs (e.g. *args, **kwargs)
    maxRepeat : int
        the maximum number of times to repeat the refresh   
    reset : bool or solara.Reactive(Bool)
        if True, the repeater will reset to the first iteration
    pause : bool or solara.Reactive(Bool)
        if True, the repeater will pause and not refresh
        if False, the repeater will resume refreshing from the current iteration     
    """
    

    
    periodInMilliseconds = solara.use_reactive(periodInMilliseconds)
    reset = solara.use_reactive(reset)
    pause = solara.use_reactive(pause)
    ping = solara.use_reactive(ping)
    showDebug = solara.use_reactive(showDebug)
    
    return _SimpleRepeater(
        periodInMilliseconds = periodInMilliseconds.value,
        maxRepeat = maxRepeat,
        on_refresh = _callback_wrapper(on_refresh),
        reset = reset,
        pause = pause,
        ping=ping,
        showDebug = showDebug)

    