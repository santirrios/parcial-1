from flask import Flask, request
from flask_cors import CORS
import random as random
import re

app = Flask(__name__)
cors = CORS(app)

@app.route("/hi")
def hello():
    return "hello"

""" taneto """
@app.route("/getEcuation0", methods=['POST'])
def tanteo():
    data = request.get_json()
    ecuation = data.get('ecuation')

    numero_de_iteraciones = 0
    for i in range(5000):
        X_0 = random.randint(-1000,1000)
        ecuacion_texto_con_valor = ecuation.replace("x", "*" + str(X_0))
        resultado = eval(ecuacion_texto_con_valor)

        if resultado == 0:
            return{'result': X_0, 'iterations': i}
        
    numero_de_iteraciones = numero_de_iteraciones + 1

    return 'No se encontro la solución en '+ str(numero_de_iteraciones) + 'numero de iteraciones.'

""" bisección """
@app.route("/getEcuation1", methods=['POST'])
def biseccion():
    data = request.get_json()
    ecuation = data.get('ecuation')
    decimales = float(data.get('decimales'))

    while True:
        Xa=random.randint(-1000,1000)
        ecuacion_texto_con_valorxa = ecuation.replace("x", "*" + str(Xa))
        resultadoxa = eval(ecuacion_texto_con_valorxa)
        if resultadoxa < 0:
            break

    while True:
        Xb=random.randint(-1000,1000)
        ecuacion_texto_con_valorxb = ecuation.replace("x", "*" + str(Xb))
        resultadoxb = eval(ecuacion_texto_con_valorxb)
        if resultadoxb > 0:
            break

    cont=0
    Xc=(Xb-Xa)/2
    while True:
        cont+=1
        ecuacion_texto_con_valorxc = ecuation.replace("x", "*" + str(Xc))
        ecuacion_texto_con_valorxa = ecuation.replace("x", "*" + str(Xa))
        if abs(eval(ecuacion_texto_con_valorxc))<=decimales:
            break
        elif eval(ecuacion_texto_con_valorxa)*eval(ecuacion_texto_con_valorxc)<0:
            Xb=Xc
            Xc=(Xa+Xb)/2
        else:
            Xa=Xc
            Xc=(Xa+Xb)/2
        
        if cont > 10000:
            return 'no se encontro'

    return {'result': Xc, 'iterations': cont}

""" regla falsa """
@app.route("/getEcuation2", methods=['POST'])
def regla():
    data = request.get_json()
    ecuation = data.get('ecuation')
    decimales = float(data.get('decimales'))
    print(ecuation)

    while True:
        Xa=random.randint(-1000,1000)
        Xb= -Xa

        ecuacion_texto_con_valorxa = ecuation.replace("x", "*" + str(Xa))
        resultadoxa = eval(ecuacion_texto_con_valorxa)

        ecuacion_texto_con_valorxb = ecuation.replace("x", "*" + str(Xb))
        resultadoxb = eval(ecuacion_texto_con_valorxb)

        Xc = (Xa - ((resultadoxa * (Xb-Xa)) / (resultadoxb - resultadoxa)))
        if resultadoxa * resultadoxb < 0:
            break

    cont=0
    while True:
        cont+=1
        ecuacion_texto_con_valorxa = ecuation.replace("x", "*" + str(Xa))
        resultadoxa = eval(ecuacion_texto_con_valorxa)

        ecuacion_texto_con_valorxb = ecuation.replace("x", "*" + str(Xb))
        resultadoxb = eval(ecuacion_texto_con_valorxb)

        ecuacion_texto_con_valorxc = ecuation.replace("x", "*" + str(Xc))
        resultadoxc = eval(ecuacion_texto_con_valorxc)

        if abs(resultadoxc)<= decimales:
            break
        elif resultadoxa * resultadoxc < 0:
            Xb=Xc; Xc=(Xa-((resultadoxa * (Xb-Xa)) / (resultadoxb - resultadoxa)))
        else:
            Xa=Xc; Xc=(Xa-((resultadoxa * (Xb-Xa))/(resultadoxb - resultadoxa)))
        
        if cont > 100000:
            return 'no se encontro'

    return {'result': Xc, 'iterations': cont}


@app.route("/Steffensen", methods=['POST'])
def Steffensen():
    data = request.get_json()
    ecuacion = data.get('ecuation')
    decimales = float(data.get('decimales'))
    print('ECUATIONNN')
    print(ecuacion)

    print('DECIMALES')
    print(decimales)

    Xa=random.randint(0,20)
    print('Xa = ',Xa)
    cont=0
    Xc=Xa
    while True:
        cont+=1
        if abs(pol(Xc, ecuacion))<= decimales:
            break
        else:
            Xc=Xa-((pol(Xa, ecuacion)**2)/(pol(Xa+pol(Xa, ecuacion), ecuacion)-pol(Xa, ecuacion)))
        Xa=Xc
    return {'result': Xc, 'iterations': cont}
    

@app.route("/SteffensenVariasSoluciones", methods=['POST'])
def SteffensenVariasSoluciones():
    data = request.get_json()
    ecuacion = data.get('ecuation')
    decimales = float(data.get('decimales'))
    print('ECUATIONNN')
    print(ecuacion)



    Soluciones=[]
    Max_Seeds=100
    i=0
    while i<=Max_Seeds:
        Xa=random.randrange(10)
        Xc=Xa
        while True:
            if abs(pol(Xc, ecuacion))<=decimales:
                break   
            else:
                Xc=Xa-((pol(Xa, ecuacion)**2)/(pol(Xa+pol(Xa, ecuacion), ecuacion)-pol(Xa, ecuacion)))
            Xa=Xc
        i+=1
        Xa=round(Xa, 2)
        if Xa in Soluciones:
            print('La solución:',Xa,'ya había sido encontrada')
        else:
            Soluciones.append(Xa)
            print('Nueva solución encontrada:',Xa)
                
    return { 'soluciones':Soluciones }


def pol(x, ecuacion):
    resultado = eval(ecuacion.replace("x", "*" + str(x)))
    print('resultado')
    print(resultado)
    return resultado



