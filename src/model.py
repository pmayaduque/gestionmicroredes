import pyomo.environ as pyo
import pandas as pd
import sys

def make_model(I=None, times=None, param=None, MUT=None, va_op=None, ):
    """
    Crea el modelo.
    
    Args:
        I (list) generadores instalados en la microred.
        times (int) numero de periodos de tiempo sobre los cuales se va a ejecutar el modelo.
        param (array) parametros propios para los generadores I.
        
    Returns:
        model (Pyomo ConcreteModel)
    """
    
    model = pyo.ConcreteModel(name="Gestion de Micro Redes")
    
    model.I = pyo.Set(initialize=I)
    model.CalT = pyo.Set(initialize=[i for i in range(times)])

    return model

if __name__ == "__main__":
    filepath = 'parametros.csv'
    parametros = pd.read_csv(filepath, sep=',', header=None)#.sort_index(ascending=False)

    for i in parametros:
        print(parametros[i])

    # with open(filepath, 'r') as thecsv:
    #     for row in thecsv:
    #         print(row)


    I = [1, 3, 2]
    times = 24
    # model = make_model(I=I, times=times)
    # model.pprint()
