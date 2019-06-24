from flask import Flask, jsonify, send_file, request
from anastruct import SystemElements
from matplotlib import pyplot as plt
from os import environ  
import io
import requests
import json
from PIL import Image

app = Flask(__name__)



def addap(ss,tipo,pos):
    if tipo == 0:
        ss.add_support_roll(node_id=pos)
    elif tipo == 1:
        ss.add_support_hinged(node_id=pos)
    else:
        ss.add_support_fixed(node_id=pos)

def addloadD(ss,posi,posf,mod):

    ss.q_load(element_id=list(range(posi,posf)),q=mod)


def addloadP(ss,pos,mod):

    ss.point_load(node_id=pos, Fy=mod)



@app.route('/', methods=['GET'])
def homep():

    return "URL inválida. Por favor utilize /generate_new para requisitar nova foto e /get_diagram?tipo= para requisitar um diagrama"


@app.route('/current_variables', methods=['GET'])
def getVariables():

    return jsonify(parametros);


@app.route('/test', methods=['GET'])
def jsonTest():

    return jsonify({
        "apoios":[
           {"tipo":1,"posicao":1},
           {"tipo":0,"posicao":11}
        ],
        "CargasP":[
           {"posicao":2, "modulo":2}
 
        ],
        "CargasD": [
            {"posicaoi":5, "posicaof":7, "modulo":40}        
        ]
    })



@app.route('/generate_new')
def gennew():
    '''
    Protocolo de comunicação

    "apoios":[
        {"tipo":,"posicao":},
        {"tipo":,"posicao":},
          .
          .
          .
    ],
    "CargasP": [
        {"posicao":, "modulo":},
        {"posicao":, "modulo":},
           .
           .
           .
    ]
    "CargasD": [
        {"posicaoi":,"posicaof":,"modulo":},
        {"posicaoi":,"posicaof":,"modulo":},
           .
           .
           .
    ]

    Exemplo:

    {
        "apoios":[
                {"tipo":1,"posicao":1},
                {"tipo":1,"posicao":11},
        ],
        "CargasP": [
                {"posicao":5, "modulo":40},
        ]
    }
    '''
    
    if environ.get("ssolimurl"):
        URL = environ.get("ssolimurl")
    
    elif environ.get("localurl"):
        URL = environ.get("localurl")
        URL += "/test" 

    else:
        URL = "http://0.0.0.0:5000/test"

    r = requests.get(URL)
    
    global parametros 

    parametros = r.json()

    return "Sucesso"
 
@app.route('/temporary_diagram')
def temporary_diagram():
    '''
    Recebe um parâmetro numerico que identifica o tipo de diagrama a ser retornado
        0 = Estrutural
        1 = Forças de reação
        2 = Axial
        3 = Cortante
        4 = Fletor
        5 = Displacement ?
    Requisita os parâmetros, via json:
        apoio1 e apoio2, que são os tipos dos apoios
        apoio1pos e apoio2pos, que são as posições dos dois apoios
        cargap, que é a posição da carga
        cargam, que é o módulo da carga
    Tipo dos apoios:
        0 = Primeiro gênerio (roll)
        1 = Segundo gênero (hinged)
        2 = Tercêiro Gênero (fixed)
    '''
    if not request.args.get('tipo'):
        return "Erro, falta o parametro 'tipo', ex: /get_diagram?tipo=0 "
    
    tipo = int(request.args.get('tipo'))

    ss = SystemElements(EI=1900)

    #criação da barra
    ss.add_multiple_elements([[0, 0], [10, 0]], 10)

    
    #adição do primeiro apoio
    addap(ss,parametros['apoios'][0]['tipo'],parametros['apoios'][0]['posicao'])
    
    #adição do segundo apoio
    addap(ss,parametros['apoios'][1]['tipo'],parametros['apoios'][1]['posicao'])
    
    #adição das cargas pontuais
    if('CargasP' in parametros and parametros['CargasP'] and parametros['CargasP']!=" "):
        
        for cargaP in parametros['CargasP']:
            addloadP(ss,cargaP['posicao'],-cargaP['modulo'])
   

    #adição das cargas distribuidas
    if('CargasD' in parametros and parametros['CargasD'] and parametros['CargasD']!=" "):
        
        for cargaD in parametros['CargasD']:
            addloadD(ss,cargaD['posicaoi'],cargaD['posicaof'],-cargaD['modulo'])    


    
    #geração dos diagramas
    ss.solve()
    img = io.BytesIO()
    if tipo == 0:
        ss.show_structure(show=False).savefig(img)
    elif tipo == 1:
    	ss.show_reaction_force(show=False).savefig(img)
    elif tipo == 2:
    	ss.show_axial_force(show=False).savefig(img)
    elif tipo == 3:
    	ss.show_shear_force(show=False).savefig(img)
    elif tipo == 4:
    	ss.show_bending_moment(show=False).savefig(img)
    elif tipo == 5:
    	ss.show_displacement(show=False).savefig(img) 	
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route('/get_diagram', methods=['GET'])
def get_diagram():

    if not request.args.get('tipo'):
        return "Erro, falta o parametro 'tipo', ex: /get_diagram?tipo=0 "
    
    tipo = request.args.get('tipo')

    if environ.get("localurl"):
        URL = environ.get("localurl")
    else: 
        URL = "http://0.0.0.0:5000"

    URL += "/temporary_diagram?tipo="+tipo

    response = requests.get(URL)

    imageObject  = Image.open(io.BytesIO(response.content))
    
    #left - upper - right - lower
    cropped = imageObject.crop((220,280,1000,530))

    mimg = io.BytesIO()
    cropped.save(mimg, 'PNG')
    mimg.seek(0)    

    return send_file(mimg, mimetype='image/png')    


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
