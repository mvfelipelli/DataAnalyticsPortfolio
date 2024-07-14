# -*- coding: utf-8 -*-
"""playground-kaggle.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DxGESAGhUqZu9li5MefyWBvHpJ5Rflf2
"""



# from google.colab import drive
# drive.mount('/content/drive')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from imblearn.over_sampling import SMOTE

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.max_columns', None)

df = pd.DataFrame(pd.read_csv('files/playground-series-s4e6/train.csv'))
df.head()

import plotly.express as px

df.drop('id',axis=1, inplace=True)

df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.replace('(', '')
df.columns = df.columns.str.replace(')', '')

df.columns = df.columns.str.replace('/', '_')
df.columns = df.columns.str.replace('-', '_')
df.columns = df.columns.str.replace("'", '_')

df.head()

df.info(verbose=True)

df.columns

# prompt: Gerar codigo usando plottly para gerar um boxplot e um histograma das variaveis do dataframe df, destacando a coluna Target. Colocar em um loop para testar todas as variaveis
'''
for col in df.columns:
  print(df[col].describe())
  print(df[col].value_counts())
  X = df[[col,'Target']]
  fig1 = px.box(X, x = col, color = 'Target')
  fig2 = px.histogram(df, x = col, text_auto = True, color = 'Target', barmode = 'group')
  fig1.show()
  fig2.show()
'''

x = df.drop('Target', axis = 1)
y = df['Target']

from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder

colunas = x.columns

one_hot = make_column_transformer((
    OneHotEncoder(drop = 'if_binary'),
    ['Marital_status', 'Application_mode', 'Application_order', 'Course',
       'Daytime_evening_attendance', 'Previous_qualification',
       'Previous_qualification_grade', 'Nacionality', 'Mother_s_qualification',
       'Father_s_qualification', 'Mother_s_occupation', 'Father_s_occupation',
       'Admission_grade', 'Displaced', 'Educational_special_needs', 'Debtor',
       'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder',
       'Age_at_enrollment', 'International',
       'Curricular_units_1st_sem_credited',
       'Curricular_units_1st_sem_enrolled',
       'Curricular_units_1st_sem_evaluations',
       'Curricular_units_1st_sem_approved', 'Curricular_units_1st_sem_grade',
       'Curricular_units_1st_sem_without_evaluations',
       'Curricular_units_2nd_sem_credited',
       'Curricular_units_2nd_sem_enrolled',
       'Curricular_units_2nd_sem_evaluations',
       'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_grade',
       'Curricular_units_2nd_sem_without_evaluations', 'Unemployment_rate',
       'Inflation_rate', 'GDP']
),
    remainder = 'passthrough',
    sparse_threshold=0)

x = one_hot.fit_transform(x)

one_hot.get_feature_names_out(colunas)

from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)

y

colums = [ 'Marital status' ,'Application mode' ,'Application order' ,'Course'
        ,'Previous qualification' , 'Debtor',
        'Tuition fees up to date', 'Gender', 'Scholarship holder',
        'Age at enrollment', 'International','Inflation rate', 'GDP',
        "Mother's qualification", "Father's qualification",'Displaced',
        'Educational special needs', 'Debtor']



"""numerical_features = ['Previous qualification (grade)',"Admission grade","Displaced","Educational special needs","Debtor"
 ,"Gender","Tuition fees up to date","Scholarship holder","International"
 ,"Curricular units 1st sem (credited)", "Curricular units 1st sem (enrolled)"
 ,"Curricular units 1st sem (evaluations)", "Curricular units 1st sem (approved)"
 ,"Curricular units 1st sem (grade)", "Curricular units 1st sem (without evaluations)"
 ,"Curricular units 2nd sem (credited)", "Curricular units 2nd sem (enrolled)"
 ,"Curricular units 2nd sem (evaluations)", "Curricular units 2nd sem (approved)"
 ,"Curricular units 2nd sem (grade)", "Curricular units 2nd sem (without evaluations)"
 ,"Unemployment rate", "Inflation rate","GDP"]

categorical_features = ['Marital status'
 ,'Application mode'
 ,'Application order'
 ,'Course'
 ,'Previous qualification'
 ,'Nacionality'
 ,"Mother's qualification"
 ,"Father's qualification"
 ,"Mother's occupation"
 ,"Father's occupation"
 ,"Age at enrollment"
 ]

print(numerical_features)
print(categorical_features)

"""

# Normalização
# scaler = StandardScaler()
# X = scaler.fit_transform(X)

# Amostragem
# smote = SMOTE()
# X, y = smote.fit_resample(X, y)

# Adicionar características polinomiais
# poly = PolynomialFeatures(degree=2)
# X = poly.fit_transform(X)

# Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42)

# prompt: Gerar codigo para treinamento utilizando o gridsearch baseado em LogisticRegressionCV, buscando melhor acurácia

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegressionCV

# Define the LogisticRegressionCV model
clf = LogisticRegressionCV(cv=5, random_state=42)

# Define the parameter grid
param_grid = {
    'penalty': ['l1', 'l2', 'elasticnet', 'none'],
    'Cs': [0.001, 0.01, 0.1, 1, 10, 100],
    'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
    'max_iter': [100, 200, 300]
}

# Perform GridSearchCV
grid_search = GridSearchCV(clf, param_grid, scoring='accuracy', cv=5)
grid_search.fit(X_train, y_train)

# Print the best parameters and best score
print("Best parameters:", grid_search.best_params_)
print("Best score:", grid_search.best_score_)

# Train the model with the best parameters
clf = LogisticRegressionCV(cv=5, **grid_search.best_params_)
clf.fit(X_train, y_train)
'''
# Evaluate the model on the test set
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Test accuracy:", accuracy)

from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.svm import LinearSVC, NuSVC, SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression, SGDClassifier
from sklearn.ensemble import BaggingClassifier, ExtraTreesClassifier, RandomForestClassifier

# prompt: Gerar codigo para treinamento utilizando o GridSearch baseado em DecisionTreeClassifier. buscar a melhor acurácia

from sklearn.tree import DecisionTreeClassifier

# Define o modelo de árvore de decisão
dt_model = DecisionTreeClassifier()

# Define os parâmetros a serem testados
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 3, 5, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Define a busca em grade
grid_search = GridSearchCV(dt_model, param_grid, cv=5)

# Treina o modelo
grid_search.fit(X_train, y_train)

# Obtém o melhor modelo
best_model = grid_search.best_estimator_

# Avalia o modelo
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Imprime a acurácia
print("Acurácia:", accuracy)
print("Melhores parâmetros:", grid_search.best_params_)

print(best_model)

arvore = DecisionTreeClassifier(max_depth =7)
arvore.fit(X_train, y_train)

arvore.score(X_train, y_train)

from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize = (25, 26))
plot_tree(arvore, filled = True, fontsize = 2);

models = {
   # "SVC":SVC(gamma='auto'),
    "NuSVC":NuSVC(gamma='auto'),
    "LinearSVC":LinearSVC(),
    "SGDClassifier":SGDClassifier(max_iter=100, tol=1e-3),
    "KNeighborsClassifier":KNeighborsClassifier(),
    "LogisticRegression":LogisticRegression(solver='liblinear'),
    "LogisticRegressionCV":LogisticRegressionCV(cv=3),
    "BaggingClassifier":BaggingClassifier(),
    "ExtraTreesClassifie":ExtraTreesClassifier(n_estimators=300),
    "RandomForestClassifier":RandomForestClassifier(n_estimators=300),
    "DecisionTreeClassifier":DecisionTreeClassifier(),
    "RandomForestRegressor":RandomForestRegressor(),
    "LinearRegression":LinearRegression()
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    if "Classifier" in name or "Logistic" in name or "SVM" in name:
      accuracy = accuracy_score(y_test, y_pred)
    else:
      accuracy = mean_squared_error(y_test, y_pred)

    print(f'{name} - Acurácia: {accuracy}')
    print(classification_report(y_test, y_pred))



import joblib

joblib.dump(model, 'model_logistic.joblib')

# Exemplo de novos dados para previsão
df_test = pd.read_csv('/content/test.csv')

df_test.head()

df_test.isnull().sum()

df_test.fillna(df_test.median(), inplace=True)

X = df_test.copy()



# Carregar o modelo salvo
model = joblib.load('model_logistic.joblib')

X['Ind_Target'] = None

# Fazer previsões com o modelo carregado
X['Ind_Target'] = model.predict(X)

'''