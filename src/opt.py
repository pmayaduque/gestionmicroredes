import pyomo.environ as pyo
import pandas as pd
import sys

def make_model(generators_dict=None, forecast_df=None, battery=None, demand=None):
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
    
    model.I = pyo.Set(initialize=[i for i in generators_dict.keys()])
    model.bat = pyo.Set(initialize=[battery['id_bat']])
    model.calI = model.I | model.bat
    model.T = pyo.Set(initialize=[i for i in range(len(forecast_df))])

    model.D = pyo.Param(model.T, initialize=demand)

    model.x = pyo.Var(model.I, model.T, within=pyo.Binary, initialize=0)

    model.G = pyo.Var(model.calI, model.T, within=pyo.NonNegativeReals, initialize=0)

    model.EB = pyo.Var(model.T, within=pyo.NonNegativeReals, initialize=0) #Power intended for charging the storage unit in time interval t.

    model.B = pyo.Var(model.T, within=pyo.NonNegativeReals) #Power level in battery unit over time period t.

    def B_rule(model, t):
        if t == 0:
            return model.B[t] == battery['eb_zero']
        else:
            expr = model.B[t-1] * (1-battery['o'])
            expr += model.EB[t] * battery['ef']
            expr -= (model.G[battery['id_bat'], t]/battery['ef_inv'])
            return model.B[t] == expr

    model.B_rule = pyo.Constraint(model.T, rule=B_rule)

    model.EL = pyo.Var(model.T, initialize=0) #Power generated at t time from S and W technologies to satisfying the demand.
    
    model.EW = pyo.Var(model.T, initialize=0) #Electric power discarded due to over generation in time interval t.

    def Bconstraint_rule(model, t):
        return (0.2*battery['zb'], model.B[t], battery['zb'])

    model.Bconstraint = pyo.Constraint(model.T, rule=Bconstraint_rule)
    
    def G_rule(model, i, t):
        gen = generators_dict[i]
        if gen.tec == 'S':
            return model.G[i,t] == (gen.ef**2) * gen.A * forecast_df['Rt'][t] * model.x[i,t]
        if gen.tec == 'W':
            if forecast_df['Wt'][t] < gen.w_min:
                return model.G[i,t] == 0
            elif forecast_df['Wt'][t] < gen.w_a:
                return model.G[i,t] == (1/2) * gen.p * gen.s * (forecast_df['Wt'][t]**3) * gen.ef * model.x[i,t]
            elif forecast_df['Wt'][t] <= gen.w_max:
                return model.G[i,t] == (1/2) * gen.p * gen.s * (gen.w_a**3) * gen.ef * model.x[i,t]
            else:
                return model.G[i,t] == 0
        if gen.tec == 'H':
            return model.G[i,t] == gen.p * 9.8 * gen.ht * gen.ef * forecast_df['Qt'][t] * model.x[i,t]
        if gen.tec == 'D':
            # return pyo.inequality(model.x[i,t]*gen.g_min, model.G[i,t], model.x[i,t]*gen.g_max)
            return (0, model.G[i,t] - model.x[i,t]*gen.g_min)
    
    model.G_rule = pyo.Constraint(model.I, model.T, rule=G_rule)

    def maxG_diesel_rule(model, i, t):
        gen = generators_dict[i]
        if gen.tec == 'D':
            return (0, model.x[i,t]*gen.g_max - model.G[i,t])
        else:
            return pyo.Constraint.Skip
        
    model.maxG_diesel_rule = pyo.Constraint(model.I, model.T, rule=maxG_diesel_rule)

    def Gconstraint_rule(model, t):
        ls = sum(model.G[i,t] for i in model.I if generators_dict[i].tec == 'S' or generators_dict[i].tec == 'W')
        # ls += sum(model.G[i,t] for i in model.I if generators_dict[i].tec == 'W')

        rs = model.EL[t] + model.EB[t] + model.EW[t]
        return ls == rs

    model.Gconstraint = pyo.Constraint(model.T, rule=Gconstraint_rule)

    
    def Dconstraint_rule(model, t):
        
        rs = model.EL[t]
        rs += sum(model.G[b,t] for b in model.bat)
        rs += sum(model.G[i,t] for i in model.I if generators_dict[i].tec == 'H')
        rs += sum(model.G[i,t] for i in model.I if generators_dict[i].tec == 'D')
        
        return model.D[t] == rs #(model.D[t], rs)
    model.Dconstraint = pyo.Constraint(model.T, rule=Dconstraint_rule)
    

    def obj_rule(model):
        return sum(sum(generators_dict[i].va_op * model.G[i,t] for t in model.T)for i in model.I)

    model.generation_cost = pyo.Objective(rule=obj_rule)

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
