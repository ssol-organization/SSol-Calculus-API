from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_diagram():

    return jsonify({"Teste":teste})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)