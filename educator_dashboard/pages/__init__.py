
import solara

from ..educator_dashboard import EducatorDashboard

@solara.component
def Page():
    router = solara.use_router()
    if router.search is not None:
        url_params = {x.split("=")[0]: x.split("=")[1] for x in router.search.split("&")}
    else:
        url_params = {}
    
    edu_id = int(url_params["edu"]) if "edu" in url_params else None
    EducatorDashboard(edu_id)  # Call the EducatorDashboard component to render it


# The following line is required only when running the code in a Jupyter notebook:
Page()