import solara
import plotly.express as px
import plotly.graph_objects as go

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
def AgeHoHistogram(data, which = 'age', subset = None, subset_label = None, title = None):
    # subset is boolean array which take subset of data
    
    # manual aggregation. instead use pandas groupby and agg
    # df_agg = DataFrame(aggregrate(data, which)).T
    # df_agg.sids = df_agg.sids.apply(lambda x:'<br>' + '<br>'.join(x))
    def sids_agg(sids):
        return '<br>'+ '<br>'.join(sids)
    

    df_agg = data.groupby(which, as_index=False).agg(count=(which,'size'), sids = ('sids', sids_agg))
    # add single valued column
    df_agg['group'] = 'Full Class'

    xmin, xmax = nanmin(df_agg[which]), nanmax(df_agg[which])

    labels = {'age':'Age of Universe (Gyr)', 'sids':'Student ID', 'h0':'Hubble Constant (km/s/Mpc)'}

    fig = px.bar(data_frame = df_agg, x = which, y='count', color='group',hover_data='sids', labels = labels, barmode='overlay', opacity=1, hover_name=['Full Class']*len(df_agg))
    fig.update_traces(hovertemplate = labels[which] + ': %{x}<br>' + 'count=%{y}<br>' + labels['sids'] + ': %{customdata}' + '<extra></extra>')
    # fig.update_traces(marker_color='grey', marker_line_color='grey', marker_line_width=0, opacity=1)
    title = f'Class {which.capitalize()} Distribution' if title is None else title
    fig.update_layout(showlegend=True, title_text=title)
    # show only integers on y-axis
    fig.update_yaxes(tick0=0, dtick=1)
    # show ticks every 1
    fig.update_xaxes(range=[xmin-1.5, xmax+1.5])
    
    if subset is not None:
        data_subset = data[subset]
        df_agg_subset = data_subset.groupby(which, as_index=False).agg(count=(which,'size'), sids = ('sids', sids_agg))
        bar = go.Bar(x=df_agg_subset[which], y=df_agg_subset['count'], name=subset_label, opacity=1, hoverinfo='skip', customdata=df_agg_subset['sids'])
        bar.hovertemplate = labels[which] + ': %{x}<br>' + 'count=%{y}<br>' + labels['sids'] + ': %{customdata}' + '<extra></extra>'
        fig.add_trace(bar)
        # show legend
    # fig.update_layout(showlegend=True)
    

    solara.FigurePlotly(fig)
    
    if subset is None:
        # SIDS of students without good data
        bad_sids = data[isnan(data['h0'])]['sids'].to_list()
        if len(bad_sids) > 0:
            solara.Markdown(f"**Students with bad data**: {', '.join(bad_sids)}")