from flask import Flask, jsonify, send_file, request
from anastruct import SystemElements
from matplotlib import pyplot as plt
import io
import requests

app = Flask(__name__)


@app.route('/test', methods=['GET'])
def hellodois():
    return jsonify({"apoio1":1,
                    "apoio2":1,
                    "apoio1p":1,
                    "apoio2p":3,
                    "cargap":2,
                    "cargam":-40})

@app.route('/get_diagram')
def get_diagram():
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
    tipo = int(request.args.get('tipo'))

    r = requests.get('http://0.0.0.0:5000/test')
    
    apoio1tipo, apoio2tipo  = r.json().get('apoio1'), r.json().get('apoio2')
    apoio1pos, apoio2pos = r.json().get('apoio1p'), r.json().get('apoio2p')

    cargapos  = r.json().get('cargap')
    cargamod = r.json().get('cargam')

  
    ss = SystemElements(EI=1900)

    #criação da barra
    ss.add_element(location=[[0, 0], [3, 0]])
    ss.add_element(location=[[3, 0], [8, 0]])
    
    #adição do primeiro apoio
    if apoio1tipo == 0:
        ss.add_support_roll(node_id=apoio1pos)
    elif apoio1tipo == 1:
        ss.add_support_hinged(node_id=apoio1pos)
    else:
        ss.add_support_fixed(node_id=apoio1pos)

    
    #adição do segundo apoio
    if apoio2tipo == 0:
        ss.add_support_roll(node_id=apoio2pos)
    elif apoio2tipo == 1:
        ss.add_support_hinged(node_id=apoio2pos)
    else:
        ss.add_support_fixed(node_id=apoio2pos)

    
    #adição da carga
    ss.q_load(element_id=cargapos, q=cargamod)
    
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)