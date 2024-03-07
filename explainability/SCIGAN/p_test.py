import os
import pandas as pd
import numpy as np





from scipy.stats import ttest_ind
from scipy import stats


import scipy.stats as stats


# additional packages
from statsmodels.formula.api import ols
# ANOVA table for one or more fitted linear models.
# anova_lm用于一个或多个因素的方差分析,analysis of variance_linear models
from statsmodels.stats.anova import anova_lm

# rvs_1 = stats.norm.rvs(loc=1.5, scale=1, size=(50))
# dir = 'output_test.xlsx'
dir = 'C:/Users/46773/Desktop/causl/causal_test/Taiwan/treatment_effect2/TW_2_death_increase[case_increase].xlsx'
data = pd.read_excel(dir)
# ADRF = (data.tail(1)).values.tolist()  # 每个dose的平均outcome
# ADRF = ADRF[0]
dosage = list(data.columns)
p_test = []

for i in range(len(dosage)-1):
    dose_t1 = dosage[i]
    dose_t2 = dosage[i+1]

    v1 = np.array((list(data[dose_t1]))[:-1])
    v2 = np.array((list(data[dose_t2]))[:-1])

    t1, p1 = stats.ttest_1samp(v2 - v1, 0)  # 单样本T检验
    # t2, p2 = stats.ttest_rel(v1,v2)
    p_test.append(p1)
    if p1 > 0.05:
        print("p值>0.05的dose是{}".format(i))

print(p_test)
    # df = pd.DataFrame()
    # df.insert(df.shape[1], 'v1', v1)
    # df.insert(df.shape[1], 'v2', v2)



# v1 = np.array((list(data[0]))[:-1])
# v2 = np.array((list(data[1]))[:-1])
# v3 = np.array((list(data[2]))[:-1])
# df = pd.DataFrame()
# df.insert(df.shape[1],'v1',v1)
# df.insert(df.shape[1],'v2',v2)

# model = ols('v1~C(v2)', data=df).fit()
# anovat = anova_lm(model)
# print(anovat)

# levene = stats.levene(v1, v2)          # 进行 levene 检验
# t1, p1 = stats.ttest_1samp(v2 - v1, 0) # 单样本T检验
# t2, p2 = stats.ttest_rel(v1,v2)
# #
# #
# #
# print("levene 检验P值: %f"%levene.pvalue,'\n')
# #
# print("单样本T检验")
# print(" T-test: %f\n"%t1,"P-vlaue: %f"%p1)
# #
# print("\n配对样本t检验")
# print(" T-test: %f\n"%t2,"P-vlaue: %f"%p2)


# res = ttest_ind(v1, v2)
# print(res)

# F_statistic, pVal = stats.f_oneway(v1, v2, v3)
# print((F_statistic, pVal))