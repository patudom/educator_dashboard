# educator_dashboard
An educator dashboard for the Hubble Data Story. **Still under development**

The dashboard is built using [solara](solara.dev). 
To run it, you'll need to install solara and several other packages. 


## Set up in a new environment
To create an environment when using `conda` use `conda create --name solara` and then `conda activate solara`
```
# a blank environment needs python
conda install python ipython jupyter
pip install solara
pip install pandas
pip install plotly==5.15.0
```

## Set up in an existing environment

```
pip install solara
pip install pandas
pip install plotly==5.15.0
```


## Run the dashboard

```
cd educator_dashboard
pip install -e .
solara run --dev educator_dashboard.pages
```

`--dev` prevents solara from launching the page in a new tab every time you re-run it.


## Development notes
- If you update a `.vue` file, you should be able to just refresh the browser for the changes to register.
- If you update a `.py` file, you have to **shut down the solara server (`ctrl-c`) and rerun it** for the changes to register.
- If you update `.css`, you have to force refresh your browser (`shift-command-r` on a mac) for the changes to register.

CSS goes in the file `educator_dashboard/assets/custom.css`. 

## API key
Developers need an API key to access the CosmicDS database.

In the root directory, add a file called `.env`, enter
```
CDS_API_KEY="<enter the key you've been given>"
```
and save the file.

If you haven't done this before, install `python-dotenv`
```
pip install python-dotenv
```

Once you've done that, you should be able to connect to the db.