import solara

from .Repeater import Repeater

@solara.component
def RefreshClass(rate_minutes = 5, 
                on_refresh = None, 
                roster = None, 
                student_names = None,
                show_refresh_button = True,
                stop_start_button = True,
                refresh_button_color = 'primary',
                start_button_color = '#777',
                stop_button_color = '#ccc',
                icon_only = True,
                refresh_button_text = "Refresh Data",
                ):
    print("**** refresh class component ****")
    if on_refresh is None:
        def on_refresh():
            print('refreshing class data')
            print(f"refreshing class data class id: {roster.value.class_id}")
            r = roster.value.empty_copy()
            if student_names is not None:
                student_names_dict = {row['student_id']: row['name'] for _, row in student_names.iterrows()}
                r.set_student_names(student_names_dict)
            roster.set(r)

    print("refresh class component")

    refreshRate = int(rate_minutes * 60 * 1000)
    Repeater(periodInMilliseconds=refreshRate, 
            on_refresh=on_refresh, 
            show_refresh_button=show_refresh_button, 
            stop_start_button=stop_start_button, 
            refresh_button_color=refresh_button_color,
            startColor=start_button_color,
            stopColor=stop_button_color,
            refresh_button_text=refresh_button_text,
            icon_only=icon_only,
            _show_debug=False)