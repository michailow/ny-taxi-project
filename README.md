# NYC Taxi project
 DE and ML project with NYC taxi data.</br>
 Using NYC data for yellow cabbin taxi done analysis and ML project.<br>
 On given data was built API to provide result.
 
# Project structure
Data analysis, preparation and modeling presented in `/notebooks/NY_taxi_analysis.ipynb`
 
# Start the API
To start the app launc command `docker compose up`</br>
After that we have 3 endpoint:
1. Get avegare time at certain day time:<br>
`time/<string:hour>`<br>
Example: `http://localhost:80/week/Friday`<br>

2. Get average time at certain week day:<br>
`/week/<string:day>`<br>
`http://localhost:80/time/11`

3. Using pre-trained ML model calculate time for specific day and distance:<br>
`/calculate/<int:tripDistance>/<string:day>/<int:hour>/<string:minute><br>`
Example: `http://localhost:80/calculate/6/Monday/17/50`
