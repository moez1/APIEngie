from flask import Flask
import json

app = Flask(__name__)


def compute_loads(powerplants: list, load: int, fuels: dict):
    type_to_cost = {
        "gasfired": float(fuels['gas(euro/MWh)']),
        "turbojet": float(fuels['kerosine(euro/MWh)']),
    }

    wind_pp = []
    other_pp = []
    for p in powerplants:
        if p.type == "windturbine":
            wind_pp.append(p)
        else:
            p['cost_per_mwh'] = p['efficiency'] * type_to_cost[p['type']]
            other_pp.append(p)

    for p in wind_pp:
        max_produced = p['pmax'] * p['efficiency'] * float(fuels['wind(%)']) / 100
        if max_produced <= load:
            p['p'] = max_produced
            load -= max_produced

    

def compute_loads_from_request(data: dict):
    load = int(data['load'])
    fuels = data['fuels']
    powerplants = data['powerplants']

    compute_loads(powerplants, load, fuels)

    return json.dumps(powerplants)


@app.route('/productionplant', methods = ['POST'])
def energie(payload):
    return compute_loads_from_request(payload)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port='8888')