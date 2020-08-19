import FuentesClass as FuentesClass
import opt as opt
import pandas as pd
import json
import sys
import pyomo.environ as pyo

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



if __name__ == "__main__":
    param_filepath = '../data/parameters.json'
    forecast_filepath = '../data/forecast.csv'
    demand_filepath = '../data/demand.csv'
    generators, battery, forecast_df, demand = read_data(param_filepath, forecast_filepath, demand_filepath)
    generators_dict = create_generators(generators)
    
    
    
    
    model = opt.make_model(generators_dict, forecast_df, battery, demand)
    opt = pyo.SolverFactory('gurobi')
    results = opt.solve(model)
    term_cond = results.solver.termination_condition
    if term_cond != pyo.TerminationCondition.optimal:
        print ("Termination condition={}".format(term_cond))
        raise RuntimeError("Optimization failed.")
    print(results)
    #model.x.pprint()
    #model.G.pprint()
    #model.B_rule.pprint()
    #li = generators[3].to_list()
    #li_aux = [i for i in li if str(i) != 'nan']
    