import FuentesClass as FuentesClass
import pandas as pd
import sys

def read_data(filepath):
    generators_df = pd.read_csv(filepath, sep=',', header=None)
    return generators_df

def create_generators(generators_df):
    generators_dict = {}
    for i in generators_df.columns:
        aux_list = [j for j in generators_df[i] if str(j) != 'nan']
        if generators_df[i][0] == '0':
            print(aux_list[1:])
            obj_aux = FuentesClass.Solar(*aux_list[1:])
        elif generators_df[i][0] == '1':
            obj_aux = FuentesClass.Eolica(*aux_list[1:])
        elif generators_df[i][0] == '2':
            obj_aux = FuentesClass.Hidraulica(*aux_list[1:])
        elif generators_df[i][0] == '3':
            obj_aux = FuentesClass.Diesel(*aux_list[1:])
        
        generators_dict[generators_df[i][1]] = obj_aux
    return generators_dict



if __name__ == "__main__":
    filepath = 'data/parametros.csv'
    generators_df = read_data(filepath)
    generators_dict = create_generators(generators_df)
    #li = generators_df[3].to_list()
    #li_aux = [i for i in li if str(i) != 'nan']
    