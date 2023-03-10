import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt

pitch_data = pd.read_csv('2019_pitches.csv')
np.random.seed(54321)

train = pitch_data.sample(n = 10000, replace = False)
pitch_data = pitch_data.drop(train.index)
test = pitch_data.sample(n = 2000, replace = False)
pitch_data['on_1b'] = pd.to_numeric(pitch_data.on_1b)

#train = 

#train['Result'] = train['code'].map({'S':1, 'C':1, 'F':1, 'T':1,'L':1, 'W':1, 'M':1, 'Q':1, 'R':1, 'X':1, 'D':1, 'E':1, 'B':0, '*B':0, 'I':0, 'P':0, 'H':0})
#test['Result'] = test['code'].map({'S':1, 'C':1, 'F':1, 'T':1,'L':1, 'W':1, 'M':1, 'Q':1, 'R':1, 'X':1, 'D':1, 'E':1, 'B':0, '*B':0, 'I':0, 'P':0, 'H':0})

def jitter(values,j):
    return values + np.random.normal(j,0.02,values.shape)

def confusion_matrix_data(data, actual_values, model, cutoff=0.5):
    pred_values = model.predict(data)
    # Specify the bins
    bins = np.array([0,cutoff,1])
    # Confusion matrix
    cm = np.histogram2d(actual_values, pred_values, bins=bins)[0]
    cm_df = pd.DataFrame(cm)
    cm_df.columns = ['Predicted 0','Predicted 1']
    cm_df = cm_df.rename(index={0: 'Actual 0',1:'Actual 1'})
    
    accuracy = (cm[0,0]+cm[1,1])/cm.sum()
    fnr = (cm[1,0])/(cm[1,0] + cm[1,1])
    fpr = (cm[0,1])/(cm[0,0] + cm[0,1])
    precision = (cm[1,1])/(cm[1,1] + cm[0,1])
    tpr = (cm[1,1])/(cm[1,0] + cm[1,1]) # Recall
    
    sns.heatmap(cm_df, annot=True, cmap='Blues', fmt='g')
    plt.ylabel("Actual Values")
    plt.xlabel("Predicted Values")
    plt.show()
    print("Classification accuracy = {:.1%}".format(accuracy))
    print("Precision = {:.1%}".format(precision))
    print("TPR or Recall = {:.1%}".format(tpr))
    print("FNR = {:.1%}".format(fnr))
    print("FPR = {:.1%}".format(fpr))

# train = train[['start_speed', 'break_angle','break_length','code','pitch_type','b_count','s_count','outs','Result']]
# train = train.dropna()
# print(train.corr())

# from statsmodels.stats.outliers_influence import variance_inflation_factor
# from statsmodels.tools.tools import add_constant
# X = train[['start_speed', 'break_angle','break_length','b_count','s_count','outs']]
# X = add_constant(X)
# vif_data = pd.DataFrame()
# vif_data["feature"] = X.columns

# for i in range(len(X.columns)):
#     vif_data.loc[i,'VIF'] = variance_inflation_factor(X.values, i)

# #print(vif_data)


# #sns.scatterplot(x = train.break_length, y = train.Result, data = train, color = 'orange')
# logit_model = sm.logit(formula = 'Result~start_speed*break_angle+start_speed*break_length+break_length*break_angle', data = train).fit()
# # sns.lineplot(x = 'end_speed', y= logit_model.predict(train), data = train, color = 'blue') 
# # plt.show()

# print(logit_model.summary())
# confusion_matrix_data(train, train.Result, logit_model)

# #train.loc[train['b_count'] == 2, :].Result.value_counts()

# #train.loc[train['Result'] == 1, :].shape

train = train[-train['code'].isin(['X','D','E'])]
train['Result'] = train['code'].map({'S':1, 'C':1, 'F':1, 'T':1,'L':1, 'W':1, 'M':1, 'Q':1, 'R':1, 'B':0, '*B':0, 'I':0, 'P':0, 'H':0})
train = train[['start_speed', 'break_angle','break_length','code','pitch_type','b_count','s_count','outs', 'Result', 'px', 'pz']]
train = train.dropna()

train.corr()

logit_model = sm.logit(formula = 'Result~px*pz+b_count', data = train).fit()
print(logit_model.summary())
confusion_matrix_data(train, train.Result, logit_model, cutoff = 0.5)