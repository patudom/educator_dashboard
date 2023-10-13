import solara


from .SimpleRepeater import _callback_wrapper, SimpleRepeater



def ms_to_nice(time_milliseconds):
    time_sec = time_milliseconds / 1000
    if time_sec > 120:
        return f"{time_sec / 60 : .0f} minutes"
    else:
        return f"{time_sec : .0f} seconds"


@solara.component
def Repeater(periodInMilliseconds = 1 * 60 * 1000, # 1 minute
            on_refresh = lambda : None,
            maxRepeat = 0,
            show_refresh_button = True,
            stop_start_button = True,
            refresh_button_color = 'primary',
            startColor = '#777',
            stopColor = '#ccc',
            icon_only = True,
            _show_debug = True,
            refresh_button_text = "Refresh Data",
            **kwargs
            ):
    """    
    Parameters
    ----------
    periodInMilliseconds : int, optional
        The time between refreshes, by default 5 * 60 * 1000 (30 seconds)
    on_refresh : function, optional
        A function that takes no required arguments, by default lambda : None
    maxRepeat : int, optional
        The number of times to repeat, 0 means repeat forever, by default 0
    show_refresh_button : bool, optional
        Whether to show the manual refresh button, by default False
    stop_start_button : bool, optional
        Whether to show the stop/start button, by default False
    refresh_button_color : str, optional
        The color of the manual refresh button button, by default "grey". Use CSS compatible colors.
    icon_only : bool, optional
        Whether to show the manual refresh button as an icon only, by default False
    - startColor: the color of the start button, by default "#777" (light grey)
    
    - stopColor: the color of the stop button, by default "#ccc" (dark grey)
        
    """
    
    reset = solara.use_reactive(False)
    pause = solara.use_reactive(False)
    ping = solara.use_reactive(0)
    t = solara.use_reactive(periodInMilliseconds)
    
    SimpleRepeater(
        periodInMilliseconds = t,
        on_refresh = _callback_wrapper(on_refresh),
        maxRepeat = maxRepeat,
        reset = reset,
        pause = pause,
        ping = ping,
        showDebug = _show_debug
    )
    
    with solara.Row(gap='0.5rem'):
    # manual refresh button
        if show_refresh_button:
            tooltip = f"Refresh student data now. Data automatically refreshes every {t.value / 1000 : .0f} seconds ({t.value / (60 *1000) : 0.1f} minutes)."
            tooltip = solara.Markdown(tooltip, style="max-width: 20ch")
            with solara.Tooltip(tooltip = tooltip):                    
                refresh_button = solara.Button(
                    label = None if icon_only else refresh_button_text,
                    icon_name = "mdi-refresh-circle",
                    on_click = lambda*_: ping.set(ping.value + 1),
                    color = refresh_button_color,
                    **kwargs
                )
            
        # stop/start button
        if stop_start_button:
            tooltip = f"{'Restart' if pause.value else 'Pause'} automatic refreshing of student data. Data refreshes every {t.value / 1000 : .0f} seconds ({t.value / (60 *1000) : 0.1f} minutes)."
            tooltip = solara.Markdown(tooltip, style="max-width: 40ch")
            with solara.Tooltip(tooltip = tooltip):
                stop_start_button = solara.Button(
                    icon_name = "mdi-play-circle" if pause.value else "mdi-pause-circle",
                    on_click = lambda *_: pause.set(not pause.value),
                    color = startColor if pause.value else stopColor,
                    **kwargs
                )
    