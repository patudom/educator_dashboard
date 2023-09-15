import solara
from .Collapsible import Collapsible


@solara.component
def ClassProgress(roster):
    
    dataframe = roster.value.short_report()
    if dataframe is None:
        if len(roster.value.roster) == 0:
            solara.Markdown(f"### Error: There are no students in the class {roster.value.class_id}")
            return
        else:
            with Collapsible(header = "See Class Roster to see what is wrong"):
                solara.Markdown(f"Class roster: {roster.value.roster}")
                return
                
    # pavg = dataframe.percent_story_complete.median()
    pmin = dataframe.percent_story_complete.min()
    pmax = dataframe.percent_story_complete.max()
    solara.Markdown (f"<pre> Least Progress: {pmin:.0f}%      Most Progress: {pmax:.0f}% </pre>")