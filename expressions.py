"""Expressions used to construct model constraints. They perform a logical test
that must be satisfied and return bool. There are both vector and scalar
constraints, with scalar constraints only providing model object as an input,
while vector ones also requiring the current time stamp (t).
"""


def objective(model):
    """implements con1"""
    return model.profit == sum(
        model.c[t] * (model.power_out[t] * model.eff_out - model.power_in[t] /
                      model.eff_in) for t in model.samples)


def charge_limit(model, t):
    """implements con2"""
    return model.power_in[t] <= model.is_charging[t] * model.mcp


def discharge_limit(model, t):
    """implements con3"""
    return model.power_out[t] <= model.is_discharging[t] * model.mdp


def daily_discharge_limit(model):
    """implements con4"""
    return sum(model.power_out[t] * model.res for t in model.samples
               ) <= model.mdd


def energy_balance(model, t):
    """implements con5"""
    soc_change = (model.power_in[t] - model.power_out[t]
                  ) * model.res / model.dec
    if t == 0:
        return model.state_of_charge[t] == model.soc_init + soc_change
    else:
        return model.state_of_charge[t] == model.state_of_charge[
            t - 1] + soc_change


def only_one_op(model, t):
    """implements con6"""
    return (model.is_charging[t] + model.is_discharging[t]) <= 1
