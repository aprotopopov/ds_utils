import numpy as np

# MAPE for sklearn should be done 
# MAPE = make_scorer(MAPE_raw, greater_is_better=False)
def MAPE_raw(y_true, y_pred): 
    y_true = np.array(y_true)
    y_pred = np.array(y_pred).reshape(-1)
    return np.mean(np.abs((y_true - y_pred) / y_true))

def MAPE_XGB(y_true, dtrain): 
    y_true = np.array(y_true)
    y_pred = dtrain.get_label()
    return ('MAPE', np.mean(np.abs((y_true - y_pred) / y_true)))
