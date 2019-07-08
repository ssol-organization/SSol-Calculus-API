from flask import Flask, jsonify, send_file, request
from anastruct import SystemElements
from matplotlib import pyplot as plt
from os import environ  
import io
import requests
import json
from PIL import Image

app = Flask(__name__)


parametros = ""


def f(x, eq):
    return eval(eq)

def solveq(eq):

    A = -1
    B = 7
    # Definir condições de parada
    x_tol = 0.01
    y_tol = 0.01
    x_anterior = B
    # Definir variável auxiliar para contagem de iterações
    counter = 1
    while True:
        # Encontrar a próxima aproximação da raíz da função
        xi = (B + A) / 2                           # Método da Bisseção
        # Visualizar o gráfico
        counter += 1
        # Definir o novo intervalo
        if f(A,eq) * f(xi,eq) < 0:
            B = xi
        elif f(A,eq) * f(xi,eq) == 0:
            return xi
        else:
            A = xi
        # Checar as condições de parada
        # Eixo Y
        if abs(f(xi,eq)) < y_tol:
            break
        # Eixo X
        if abs(x_anterior - xi) < x_tol:
            break
        x_anterior = xi

def addap(ss,tipo,pos):
    if tipo == 0:
        ss.add_support_roll(node_id=pos)
    elif tipo == 1:
        ss.add_support_hinged(node_id=pos)
    else:
        ss.add_support_fixed(node_id=pos)

def addloadD(ss,posi,posf,mod):
    mod = round(mod/(posf-posi))
    ss.q_load(element_id=list(range(posi,posf)),q=mod)


def addloadP(ss,pos,mod):
    ss.point_load(node_id=pos, Fy=mod)

def addloadT(ss,posi,posf,mod):
    
    eqstring = ""
    for i in range(1,posf-posi+1):
        eqstring += (str(i)+"*x + ")    
    eqstring += ("-"+str(mod))
    
    imod = int(solveq(eqstring))
      
    c = 1
    for i in range(posi,posf):
        ss.q_load(element_id=i,q=-imod*c)
        c += 1


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
           {"posicao":2, "modulo":10}
 
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
    

    if not 'parametros' in globals() or parametros == "":
        return "Erro, falta gerar informações, use /generate_new"


    tipo = int(request.args.get('tipo'))

    ss = SystemElements(EI=1900)

    #criação da barra
    ss.add_multiple_elements([[0, 0], [10, 0]], 10)

    
    #adição do primeiro apoio
    addap(ss,parametros['apoios'][0][0],round(int(parametros['apoios'][0][1]['posicao'])/10))
    
    #adição do segundo apoio
    if(round(int(parametros['apoios'][1][1]['posicao'])/10)<11):
        newpos = round(int(parametros['apoios'][1][1]['posicao'])/10)+1
    else:
        newpos = round(int(parametros['apoios'][1][1]['posicao'])/10)
    addap(ss,parametros['apoios'][1][0],newpos)
    
    #adição das cargas pontuais
    if('cargasP' in parametros and parametros['cargasP'] and parametros['cargasP']!=" "):
        
        for cargaP in parametros['cargasP'][0]:
            addloadP(ss,round(int(cargaP['posicao'])/10),-int(cargaP['modulo']))
   

    #adição das cargas distribuidas
    if('cargasD' in parametros and parametros['cargasD'] and parametros['cargasD']!=" "):
        
        for cargaD in parametros['cargasD'][0]:
            addloadD(ss,round(int(cargaD['posicao_i'])/10),round(int(cargaD['posicao_f'])/10),-int(cargaD['modulo']))    


    #adição das cargas triangulares
    if('cargasT' in parametros and parametros['cargasT'] and parametros['cargasT']!=" "):
        
        for cargaT in parametros['cargasT'][0]:
            addloadT(ss,round(int(cargaT['posicao_i'])/10),round(int(cargaT['posicao_f'])/10),int(cargaT['modulo']))    
    
    
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
    return send_file(img, mimetype='image/jpg')


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
    
    try:
        imageObject  = Image.open(io.BytesIO(response.content))
    
    except Exception as e:
        return send_file("error.jpg", mimetype='image/jpg')     


    #left - upper - right - lower
    cropped = imageObject.crop((220,280,1000,530))

    mimg = io.BytesIO()
    cropped.save(mimg, 'PNG')
    mimg.seek(0)    

    return send_file(mimg, mimetype='image/png')    


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
