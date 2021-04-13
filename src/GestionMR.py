import FuentesClass as FuentesClass
import opt as opt
import pyomo.environ as pyo
from pyomo.core import value

import pandas as pd
import string
import random
import csv

import json
import sys
import os
import time


def read_data(forecast_filepath, demand_filepath):#, filepath_bat):
    #generators = pd.read_csv(param_filepath, sep=',', header=0)


    forecast_df = pd.read_csv(forecast_filepath, sep=',', header=0)
    

    demand = pd.read_csv(demand_filepath, squeeze=True, sep=',', header=None).to_dict()
    
    return forecast_df, demand

def create_generators(param_filepath):
    with open(param_filepath) as parameters:
        data = json.load(parameters)
    
    generators = data['generators']
    battery = data['battery']

    battery = FuentesClass.Bateria(*battery.values())

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
        
    return generators_dict, battery

def create_results(model):
    #results = {}
    G_data = {i: [0]*len(model.T) for i in model.calI}
    for (i,t), v in model.G.items():
        G_data[i][t] = value(v)
    
    G_df = pd.DataFrame(G_data, columns=[*G_data.keys()])

    x_data = {i: [0]*len(model.T) for i in model.I}
    for (i,t), v in model.x.items():
        x_data[i][t] = value(v)
    
    x_df = pd.DataFrame(x_data, columns=[*x_data.keys()])

    b_data = {i: [0]*len(model.T) for i in model.I}
    for t, v in model.B.items():
        b_data[t] = value(v)
    
    b_df = pd.DataFrame(b_data, columns=[*b_data.keys()])

    return G_df, x_df, b_df

def export_results(model, location, day, x_df, G_df, b_df, execution_time,
    down_limit, up_limit, l_max, l_min, term_cond):
    
    #current_path = os.getcwd()
    y = False
    while not(y):
        folder_name = location+'_'+day+'_'+str(random.choice(string.ascii_letters))+str(random.randint(0, 10))
        new_path = '../results/'+folder_name
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            y = True
    x_df.to_csv(new_path+'/x.csv')
    G_df.to_csv(new_path+'/G.csv')
    b_df.to_csv(new_path+'/b.csv')

    with open('../results/results.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([folder_name, down_limit, up_limit, l_min, l_max, 
            execution_time, pyo.value(model.generation_cost), term_cond])
    

    return folder_name


if __name__ == "__main__":
    param_filepath = '../data/parameters.json'
    locations = ['P', 'SA', 'PN']
    days = ['01', '02', '03', '04', '05', '06', '07']
    
    # Just Test conditions
    location = 'ME'
    day = '01'
    forecast_filepath = '../data/forecast.csv'
    demand_filepath = '../data/demand.csv'

    # forecast_filepath = os.path.join('../data/instances', str(location+day+'FORECAST.csv'))
    # demand_filepath = os.path.join('../data/instances', str(location+day+'DEMAND.csv'))
    
    forecast_df, demand = read_data(forecast_filepath, demand_filepath)
    generators_dict, battery = create_generators(param_filepath)

    down_limit, up_limit, l_min, l_max = 0.2, 0.8, 4, 4

    
    
    model = opt.make_model(generators_dict, forecast_df, battery, demand,
                            down_limit, up_limit, l_min, l_max)

    opt = pyo.SolverFactory('gurobi')

    timea = time.time()
    results = opt.solve(model)
    execution_time = time.time() - timea

    term_cond = results.solver.termination_condition
    if term_cond != pyo.TerminationCondition.optimal:
        print ("Termination condition={}".format(term_cond))
        raise RuntimeError("Optimization failed.")
    

    G_df, x_df, b_df = create_results(model)
    folder_name = export_results(model, location, day, x_df, G_df, b_df,
        execution_time, down_limit, up_limit, l_max, l_min, term_cond)
    
    print("Resultados en la carpeta: "+folder_name)
    #model.EL.pprint()
    #model.EB.pprint()
    #model.temp.pprint()
    
    
    