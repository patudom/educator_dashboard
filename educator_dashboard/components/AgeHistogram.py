import solara
import plotly.express as px

from math import ceil, floor

@solara.component
def AgeHoHistogram(data, age_col = 'age', h0_col = 'h0', which = 'age'):
    
    col_data = data[age_col]; 
    col_data = col_data[col_data>0]; 
    xmin, xmax = floor(col_data.min()), ceil(col_data.max())
    categories = list(range(xmin, xmax+1))
    fig = px.histogram(data_frame = data, x = which, labels={age_col:'Age of Universe (Gyr)'}, category_orders={age_col: categories})
    fig.update_xaxes(type='category')
    fig.update_layout(showlegend=False, title_text='Class Age Distribution')
    # show only integers on y-axis
    fig.update_yaxes(tick0=0, dtick=1)
    # show ticks every 1
    # fig.update_xaxes(dtick=1)

    solara.FigurePlotly(fig)