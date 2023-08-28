import solara


@solara.component
def ClassProgress(dataframe, roster):
    pavg = dataframe.value.percent_story_complete.median()
    pmin = dataframe.value.percent_story_complete.min()
    pmax = dataframe.value.percent_story_complete.max()
    solara.Markdown (f"## Overall Class Progress: {pavg:.0f}% (min: {pmin:.0f}%, max: {pmax:.0f}%)")