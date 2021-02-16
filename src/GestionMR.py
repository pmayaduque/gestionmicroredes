import FuentesClass as FuentesClass
import opt as opt
import pandas as pd
import json
import sys
import pyomo.environ as pyo
from pyomo.core import value

import sys

def read_data(param_filepath, forecast_filepath, demand_filepath):#, filepath_bat):
    #generators = pd.read_csv(param_filepath, sep=',', header=0)

    with open(param_filepath) as parameters:
        data = json.load(parameters)
    
    generators = data['generators']
    forecast_df = pd.read_csv(forecast_filepath, sep=',', header=0)
    battery = data['battery']

    demand = pd.read_csv(demand_filepath, squeeze=True, sep=',', header=None).to_dict()
    
    return generators, battery, forecast_df, demand

def create_generators(generators):
    generators_dict = {}
    for i in generators:
        if i['tec'] == 'S':
            obj_aux = FuentesClass.Solar(*i.values())
        elif i['tec'] == 'W':
            obj_aux = FuentesClass.Eolica(*i.values())
        elif i['tec'] == 'H':
            obj_aux = FuentesClass.Hidraulica(*i.values())
        elif i['tec'] == 'D':
            obj_aux = FuentesClass.Diesel(*i.values())
        # else:
        #     raise RuntimeError('Generator ({}) with unknow tecnology ({}).'.format(i['id_gen'], i['tec'])

        generators_dict[i['id_gen']] = obj_aux
        
    return generators_dict

def export_results(model):
    #results = {}
    G_data = {i: [0]*len(model.T) for i in model.calI}
    for (i,t), v in model.G.items():
        G_data[i][t] = value(v)
    
    G_df = pd.DataFrame(G_data, columns=[*G_data.keys()])

    x_data = {i: [0]*len(model.T) for i in model.I}
    for (i,t), v in model.x.items():
        x_data[i][t] = value(v)
    
    x_df = pd.DataFrame(x_data, columns=[*x_data.keys()])
    return G_df, x_df


if __name__ == "__main__":
    param_filepath = '../data/parameters.json'
    forecast_filepath = '../data/forecast.csv'
    demand_filepath = '../data/demand.csv'
    generators, battery, forecast_df, demand = read_data(param_filepath, forecast_filepath, demand_filepath)
    generators_dict = create_generators(generators)
    
    
    model = opt.make_model(generators_dict, forecast_df, battery, demand)

    #model.EW.pprint()
    #model.maxG_diesel_rule.pprint()
    sys.exit()
    opt = pyo.SolverFactory('gurobi')
    results = opt.solve(model)
    term_cond = results.solver.termination_condition
    if term_cond != pyo.TerminationCondition.optimal:
        print ("Termination condition={}".format(term_cond))
        raise RuntimeError("Optimization failed.")
    model.G.pprint()
    G_df = export_results(model)
    print(G_df)
    #model.EL.pprint()
    #model.EB.pprint()
    #model.temp.pprint()
    
    
    