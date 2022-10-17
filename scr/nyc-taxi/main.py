from flask import Flask
from api import getStatistiksForDay, getStatistiksForHour, calculate, getEngine, prepareOutput
from load_data import upload_data


def createApp():
    app = Flask('NYC-Taxi')
    engine = getEngine()

    @app.route('/')
    def index():
        return "App started"

    @app.route("/init")
    def init():
        upload_data(engine)

    @app.route("/week/<string:day>", methods=["GET"])
    def getTotal(day):
        value = getStatistiksForDay(day, engine)
        return prepareOutput(day, value)

    @app.route("/time/<string:hour>", methods=["GET"])
    def getPerContry(hour):
        value = getStatistiksForDay(hour, engine)
        return prepareOutput(hour, value)

    @app.route("/calculate/<tripDistance>/<string:day>/<string:hour>/<string:minute>", methods=["GET"])
    def calculateTime(tripDistance, day, hour, minute, engine):
        return calculate(tripDistance, day, hour, minute, engine)

    return app


def main():
    app = createApp()
    app.run(debug=True, host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()