import os
import pandas as pd

# dir = 'C:/Users/46773/Desktop/causl/causal_test/Singapore/treatment_effect2/output_test.xlsx'
dir = 'output_test.xlsx'
data = pd.read_excel(dir)

dosage = list(data.columns)
# print(dosage)
# print(type(dosage))
ADRF = (data.tail(1)).values.tolist()  # 每个dose的平均outcome
ADRF = ADRF[0]
# print(ADRF)

sum = 0
num = 0
# length = len(dosage)
# sum = ADRF[length-1] - ADRF[0]
# dose = dosage[length-1]-dosage[0]
# MTEF = sum/dose
for i in range(len(dosage)-1):
# for i in range(41):
    if (i!=29) & (i!=30):
    # if (i!=8):
        MTEF_i = (ADRF[i+1] - ADRF[i])/(dosage[i+1]-dosage[i])
        sum += MTEF_i
        num += 1

MTEF = sum/num
print(MTEF)

