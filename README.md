# teacher_dashboard
A teacher dashboard for the Hubble Data Story. **Still under development**

The teacher dashboard is built using [solara](solara.dev). 
To run you need to install solara and several other packages. 
If you using a new environment you need to have several packages install

To create an environment when using `conda` use `conda create --name solara` and then `conda activate solara`
```
# a blank environment needs python
conda install python ipython jupyter
pip install solara
pip install pandas
pip install plotly==5.15.0
```


To run the dashboard

```
cd educator_dashboard
pip install -e .
solara run educator_dashboard.pages
```


To edit the CSS edit the file `educator_dashboard/assets/custom.css`. You need to force refresh the page to see the changes. If you make changes to components you need to restart the server.


List of custom components

- Look in `Dashboard.py` and `StudentProgress.py` to see the various custom components