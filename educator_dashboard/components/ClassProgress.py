import solara
from .Collapsable import Collapsable


@solara.component
def ClassProgress(roster):
    
    dataframe = roster.value.short_report()
    if dataframe is None:
        solara.Markdown("This class has a problem")
        if len(roster.value.roster) == 0:
            solara.Markdown(f"There are no students in the class {roster.value.class_id}")
            return
        else:
            with Collapsable(header = "See Class Roster to see what is wrong"):
                solara.Markdown(f"Class roster: {roster.value.roster}")
                return
                
    pavg = dataframe.percent_story_complete.median()
    pmin = dataframe.percent_story_complete.min()
    pmax = dataframe.percent_story_complete.max()
    solara.Markdown (f"## Overall Class Progress: {pavg:.0f}% (min: {pmin:.0f}%, max: {pmax:.0f}%)")