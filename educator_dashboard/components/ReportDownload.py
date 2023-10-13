import solara

@solara.component
def DownloadReport(roster):
    roster = solara.use_reactive(roster)
    # if len(roster.value.roster) == 0:
    #     return
    # dialog = rv.Dialog(
    #     v_slots = [{
    #         'name': 'activator',
    #         'variable': 'x',
    #         'children': rv.Btn(v_on='x.on', color='primary', dark=True, children=['Show Table'])
            
    #     }]
    # )
    # with dialog:
    #     solara.DataFrame(roster.value.report())
    
    
    df = roster.value.report()
    if df is None:
        return

    # file_obj = BytesIO()
    # df.to_excel(file_obj, index=False)
    with solara.FileDownload(df.to_csv(index=False), "Class Report.csv", mime_type="application/vnd.ms-excel"):
        solara.Button("Report", icon_name="mdi-download", classes=["my-buttons"], text=True, outlined=True)
