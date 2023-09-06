import solara

import reacton.ipyvuetify as rv

@solara.component
def ScrollY(children = [], class_='', style_={}, height='100%'):
    
    css = {'height': height, 'overflow-y': 'auto'}
    if isinstance(style_, dict):
        css.update(style_)
    elif isinstance(style_, str):
        style_dict = {s.split(':')[0]:s.split(':')[1] for s in style_.split(';') if s!=''}
        css.update(style_dict) 
    else:
        raise ValueError(f"style_ must be a dict or a string, not {type(style_)}")
        
    css_string = ';'.join([f"{k}: {v}" for k,v in css.items()])
    
    return rv.Container(children=children, class_='jl-scrollY' + ' ' + class_, style_=css_string)