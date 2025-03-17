import solara
from .Collapsible import Collapsible
from ..class_report import Roster
from solara.reactive import Reactive

@solara.component
def ClassProgress(roster: Reactive[Roster]):
    

    # if dataframe is None:
    if len(roster.value.roster) == 0:
        solara.Markdown(f"### Error: There are no students in the class {roster.value.class_id}")
        return
        # else:
        #     with Collapsible(header = "See Class Roster to see what is wrong"):
        #         solara.Markdown(f"Class roster: {roster.value.roster}")
        #         return
                
    # pavg = dataframe.percent_story_complete.median()
    num_students = len(roster.value.roster)
    if roster.value.progress_summary is not None:
        percent_complete = roster.value.progress_summary['percent_story_complete']
        pmin =min(percent_complete)
        pmax = max(percent_complete)
        solara.Markdown (f"<pre>Least Progress: {pmin:.0f}%\nMost Progress: {pmax:.0f}%\n# of students:  {num_students:2d} </pre>")
    else:
        solara.Markdown(f"### Error: There are no students in the class {roster.value.class_id}")