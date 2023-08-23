import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_data(filename):
    return pd.read_csv(f"data_cleaning/{filename}.csv")


df = get_data('apples_cleaned')

# Choose relevant columns

df_model = df[
    ['kg_price', 'Variety', 'Class', 'Size', 'Package', 'Unit', 'Total Sales', 'Sales Quantity', 'Closing Stock',
     'Market']]

# Get dummy data
df_dum = pd.get_dummies(df_model)

# Train test split
from sklearn.model_selection import train_test_split

X = df_dum.drop('kg_price', axis=1)
y = df_dum.kg_price.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Multiple linear regression
import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y, X_sm)
# print(model.fit().summary())

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

# print(np.mean(cross_val_score(lm, X_train, y_train,scoring="neg_mean_absolute_error",cv=10)))

# Lasso regression
lm_l = Lasso(alpha=0.19)
lm_l.fit(X_train, y_train)

# print(np.mean(cross_val_score(lm_l, X_train, y_train,scoring="neg_mean_absolute_error",cv=10)))

"""
alpha = []
error = []

for i in range(1,100):
    print(i)
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml, X_train, y_train,scoring="neg_mean_absolute_error",cv=10)))

plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err,columns=['alpha','error'])
print(df_err[df_err.error == max(df_err.error)]) # alpha = 0.19 error = -2.647464
"""

# Random forest
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(criterion='friedman_mse', max_features=None, n_estimators=40)
rf.fit(X_train,y_train)

# print(np.mean(cross_val_score(rf,X_train,y_train,scoring="neg_mean_absolute_error",cv=10)))

# Tune models using GridSearchCV
from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators': range(10, 50, 10), 'criterion': ('absolute_error', 'friedman_mse'),
              'max_features': (None, 'sqrt', 'log2', 0.5)}

# gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3, error_score='raise')
# gs.fit(X_train, y_train)

# print(f"Best Score: f{gs.best_score_}")
# print(f"Best Estimator: f{gs.best_estimator_}")
"""
printed
Best Score: f-0.5265265753873192
Best Estimator: fRandomForestRegressor(criterion='friedman_mse', max_features=None,
                      n_estimators=40)
"""

# Test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = rf.predict(X_test)

from sklearn.metrics import mean_absolute_error

print(mean_absolute_error(y_test, tpred_lm))
print(mean_absolute_error(y_test, tpred_lml))
print(mean_absolute_error(y_test, tpred_rf))

import pickle
pick1 = {'model': rf}
pickle.dump(pick1,open('model_file' + ".p","wb"))

file_name = "model_file.p"
with open(file_name,"rb") as pickled:
    data = pickle.load(pickled)
    model_p = data['model']

print(model_p.predict(X_test.iloc[0,:].values.reshape(1,-1)))
print(y_test)

#print(list(X_test.iloc[0,:]))

