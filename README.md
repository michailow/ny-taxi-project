# NYC Taxi project

 DE and ML project with NYC taxi data.</br>
 The project is divided into two parts.</br>
 The first part is to do the data analysis, visualization and ML in Jypyter Notebook.</br>
 In first part Jupyter Notebook is being used to analize data and visualize results. After that ML algorithm is being used to create predication model.  
 Second part is creating of API and DB that is capable of providing results with API packaged in Docker Container.
 
 
# Data & Licence
For this project I used data from [TLC Trip Record](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).</br>
Analysis was made with Yellow Taxi Trip Records data for May.<br>
The written code could fit data for other months.</br>
The data used in the used datasets were collected and provided to the NYC Taxi and Limousine Commission (TLC) by technology providers authorized under the Taxicab & Livery Passenger Enhancement Programs (TPEP/LPEP).


# Project structure.
1. Data analysis, visualization, preparation and modeling presented in `/notebooks/NY_taxi_analysis.ipynb` notebook.</br>
2. API code `src/nyc-taxi`.<br>
3. Docker and DB in `Dockerfile` and `docker-compose.yaml` files.
 

# Run code
In current version to see results you will need:
1. Dowload yellow taxi data for period you are interested.
2. Run Juputer Notebook to create `model.joblib` file. Later put that file in `scr/nyc-taxi/` folder.
3. To start the app launch command `docker-compose up`</br>


# Endpoint
After that we have 3 endpoint:
1. Get avegare time at certain day time:<br>
`/time/<string:hour>`<br>
Example: `http://localhost:80/week/Friday`<br>

2. Get average time at certain week day:<br>
`/week/<string:day>`<br>
Example: `http://localhost:80/time/11`

3. Using pre-trained ML model calculate time for specific day and distance:<br>
`/calculate/<int:tripDistance>/<string:day>/<int:hour>/<string:minute>`<br>
Example: `http://localhost:80/calculate/6/Monday/17/50`


# TBD
1. Reduce size of `pickle` model. Current object is about 500 MB.<br>
2. Add dependency management like poetry.<br>
3. Make data initiazilation during Docker building. Currently it Data uploading to DB as separate route.
