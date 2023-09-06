import solara
import plotly.express as px

from math import ceil, floor

@solara.component
def AgeHoHistogram(data, age_col = 'age', h0_col = 'h0', which = 'age'):
    
    def sids_agg(sids):
        return '<br>'+ '<br>'.join(sids)

    df_agg = data.groupby('age', as_index=False).agg(count=('age','size'), sids = ('sids', sids_agg))

    labels = {'age':'Age of Universe (Gyr)', 'sids':'Student ID'}

    fig = px.bar(data_frame = df_agg, x = 'age', y='count', hover_data='sids', labels = labels)

    fig.update_layout(showlegend=False, title_text='Class Age Distribution')
    # show only integers on y-axis
    fig.update_yaxes(tick0=0, dtick=1)
    # show ticks every 1
    # fig.update_xaxes(dtick=1)

    solara.FigurePlotly(fig)