import solara
import plotly.express as px

from pandas import DataFrame

from collections import Counter

from numpy import nanmin, nanmax, isnan
def matching_cols(df, val, col, count = None):
    """
    Return a dictionary of columns and values for a given value of a column
    """
 
    out = {c:df[c][df[col]==val].to_list() for c in df.columns}
    out.update({'count':count or len(out[col])})
    out.update({col:val})
    return out

def aggregrate(dataframe, col):
    vals = Counter(dataframe[col])
    return {v:matching_cols(dataframe, v, col, count)  for v,count in vals.items()}


@solara.component
def AgeHoHistogram(data, age_col = 'age', h0_col = 'h0', which = 'age'):
    
    # manual aggregation. instead use pandas groupby and agg
    # df_agg = DataFrame(aggregrate(data, which)).T
    # df_agg.sids = df_agg.sids.apply(lambda x:'<br>' + '<br>'.join(x))
    def sids_agg(sids):
        return '<br>'+ '<br>'.join(sids)

    df_agg = data.groupby('age', as_index=False).agg(count=('age','size'), sids = ('sids', sids_agg))

    xmin, xmax = nanmin(df_agg[which]), nanmax(df_agg[which])

    fig = px.bar(data_frame = df_agg, x = 'age', y='count', hover_data='sids', labels = labels)

    fig.update_layout(showlegend=False, title_text='Class Age Distribution')
    # show only integers on y-axis
    fig.update_yaxes(tick0=0, dtick=1)
    # show ticks every 1
    fig.update_xaxes(range=[xmin-1.5, xmax+1.5])

    solara.FigurePlotly(fig)