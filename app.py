from flask import Flask, jsonify, send_file, request
from anastruct import SystemElements
from matplotlib import pyplot as plt
import io
import requests

app = Flask(__name__)


@app.route('/test', methods=['GET'])
def hellodois():
    return jsonify({"tipo":0,
                    "apoio1":1,
                    "apoio2":2,
                    "apoio1p":1,
                    "apoio2p":3,
                    "cargap":2,
                    "cargam":-10})



@app.route('/get_diagram')
def get_diagram():

    r = requests.get('http://0.0.0.0:5000/test')
    
    return jsonify(r.json())
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)