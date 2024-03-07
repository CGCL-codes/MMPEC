# Copyright (c) 2020, Ioana Bica

from __future__ import print_function
from sklearn.utils import shuffle

import numpy as np
import pickle
import pandas as pd
from castle.common import GraphDAG
from castle.metrics import MetricsDAG
from castle.datasets import DAG, IIDSimulation
from castle.algorithms import Notears
from sklearn.model_selection import StratifiedShuffleSplit


def softmax(x):
    e_x = np.exp(x)
    return e_x / e_x.sum(axis=0)


def compute_beta(alpha, optimal_dosage):
    if (optimal_dosage <= 0.001 or optimal_dosage >= 1.0):
        beta = 1.0
    else:
        beta = (alpha - 1.0) / float(optimal_dosage) + (2.0 - alpha)

    return beta


def generate_patient(x, v, num_treatments, treatment_selection_bias, dosage_selection_bias,
                     scaling_parameter, noise_std):
    outcomes = []
    dosages = []

    for treatment in range(num_treatments):
        if (treatment == 0):
            b = 0.75 * np.dot(x, v[treatment][1]) / (np.dot(x, v[treatment][2]))

            if (b >= 0.75):
                optimal_dosage = b / 3.0
            else:
                optimal_dosage = 1.0

            alpha = dosage_selection_bias
            dosage = np.random.beta(alpha, compute_beta(alpha, optimal_dosage))

            y = get_patient_outcome(x, v, treatment, dosage, scaling_parameter)

        elif (treatment == 1):
            optimal_dosage = np.dot(x, v[treatment][2]) / (2.0 * np.dot(x, v[treatment][1]))
            alpha = dosage_selection_bias
            dosage = np.random.beta(alpha, compute_beta(alpha, optimal_dosage))
            if (optimal_dosage <= 0.001):
                dosage = 1 - dosage

            y = get_patient_outcome(x, v, treatment, dosage, scaling_parameter)

        elif (treatment == 2):
            optimal_dosage = np.dot(x, v[treatment][1]) / (2.0 * np.dot(x, v[treatment][2]))
            alpha = dosage_selection_bias
            dosage = np.random.beta(alpha, compute_beta(alpha, optimal_dosage))
            if (optimal_dosage <= 0.001):
                dosage = 1 - dosage

            y = get_patient_outcome(x, v, treatment, dosage, scaling_parameter)

        outcomes.append(y)
        dosages.append(dosage)

    treatment_coeff = [treatment_selection_bias * (outcomes[i] / np.max(outcomes)) for i in range(num_treatments)]
    treatment = np.random.choice(num_treatments, p=softmax(treatment_coeff))

    return treatment, dosages[treatment], outcomes[treatment] + np.random.normal(0, noise_std)


#用于生成table1的Dose-Response
def get_patient_outcome(x, v, treatment, dosage, scaling_parameter=10):
    if (treatment == 0):
        y = float(scaling_parameter) * (np.dot(x, v[treatment][0]) + 12.0 * dosage * (dosage - 0.75 * (
                np.dot(x, v[treatment][1]) / np.dot(x, v[treatment][2]))) ** 2)
    elif (treatment == 1):
        y = float(scaling_parameter) * (np.dot(x, v[treatment][0]) + np.sin(
            np.pi * (np.dot(x, v[treatment][1]) / np.dot(x, v[treatment][2])) * dosage))
    elif (treatment == 2):
        y = float(scaling_parameter) * (np.dot(x, v[treatment][0]) + 12.0 * (np.dot(x, v[treatment][
            1]) * dosage - np.dot(x, v[treatment][2]) * dosage ** 2))

    return y

#划分训练、验证、测试集
def get_dataset_splits(dataset):
    dataset_keys = ['x', 't', 'd', 'y', 'y_normalized']

    train_index = dataset['metadata']['train_index']
    val_index = dataset['metadata']['val_index']
    test_index = dataset['metadata']['test_index']

    dataset_train = dict()
    dataset_val = dict()
    dataset_test = dict()
    for key in dataset_keys:
        dataset_train[key] = dataset[key][train_index]
        dataset_val[key] = dataset[key][val_index]
        dataset_test[key] = dataset[key][test_index]

    dataset_train['metadata'] = dataset['metadata']
    dataset_val['metadata'] = dataset['metadata']
    dataset_test['metadata'] = dataset['metadata']

    return dataset_train, dataset_val, dataset_test


def get_split_indices(num_patients, patients, treatments, validation_fraction, test_fraction):
    num_validation_patients = int(np.floor(num_patients * validation_fraction))
    num_test_patients = int(np.floor(num_patients * test_fraction))

    test_sss = StratifiedShuffleSplit(n_splits=1, test_size=num_test_patients, random_state=0)
    rest_indices, test_indices = next(test_sss.split(patients, treatments))

    val_sss = StratifiedShuffleSplit(n_splits=1, test_size=num_validation_patients, random_state=0)
    train_indices, val_indices = next(val_sss.split(patients[rest_indices], treatments[rest_indices]))

    return train_indices, val_indices, test_indices

#从这开始执行半合成数据生成的函数
class TCGA_Data():
    def __init__(self, args):
        np.random.seed(3)

        self.num_treatments = args['num_treatments']
        self.treatment_selection_bias = args['treatment_selection_bias']
        self.dosage_selection_bias = args['dosage_selection_bias']

        self.validation_fraction = args['validation_fraction']
        self.test_fraction = args['test_fraction']

        # self.tcga_data = pickle.load(open('datasets/tcga.p', 'rb'))
        # self.patients = self.normalize_data(self.tcga_data['rnaseq'])
        # self.patients = self.tcga_data['rnaseq']

        temp = pd.read_csv('datasets/India.csv')  #读取自己的本地数据
        nt = Notears()
        temp = nt.learn(temp) #notears筛选混淆

        # self.data = pd.read_csv('datasets/US.csv')  #读取自己的本地数据
        self.data = shuffle(temp)  #随机打乱源数据排列
        # data2 = shuffle(data)





        # self.scaling_parameteter = 10
        # self.noise_std = 0.2
        #
        # self.num_weights = 3
        # self.v = np.zeros(shape=(self.num_treatments, self.num_weights, self.patients.shape[1]))

        # for i in range(self.num_treatments):
        #     for j in range(self.num_weights):
        #         self.v[i][j] = np.random.uniform(0, 10, size=(self.patients.shape[1]))
        #         self.v[i][j] = self.v[i][j] / np.linalg.norm(self.v[i][j])

        self.dataset = self.generate_dataset(self.data)

    def normalize_data(self, patient_features):
        x = (patient_features - np.min(patient_features, axis=0)) / (
                np.max(patient_features, axis=0) - np.min(patient_features, axis=0))

        for i in range(x.shape[0]):
            x[i] = x[i] / np.linalg.norm(x[i])

        return x

    def generate_dataset(self, data):
        dataset = dict()

        data_length = len(data)
        dataset['x'] = []
        dataset['t'] = [0] * data_length
        dataset['y'] = data['emotion']
        dataset['d'] = data['policy_vaccine']

        dataset['metadata'] = dict()
        # dataset['metadata']['v'] = self.v
        # dataset['metadata']['treatment_selection_bias'] = self.treatment_selection_bias
        # dataset['metadata']['dosage_selection_bias'] = self.dosage_selection_bias
        # dataset['metadata']['noise_std'] = self.noise_std
        # dataset['metadata']['scaling_parameter'] = self.scaling_parameteter


        for i in range(data_length):
            x = []
            x.append(data['brand'][i])
            # x.append(data['kid_education'][i])
            # x.append(data['economy'][i])
            # x.append(data['policy_restrict'][i])
            x.append(data['supply_demand_shortage'][i])
            x.append(data['supply_demand_adequate'][i])



            dataset['x'].append(x)


        for key in ['x', 't', 'd', 'y']:
            dataset[key] = np.array(dataset[key])

        # dataset['x'] = self.normalize_data(dataset['x']) # 对特征进行标准化

        dataset['metadata']['y_min'] = np.min(dataset['y'])
        dataset['metadata']['y_max'] = np.max(dataset['y'])
        dataset['metadata']['d_min'] = np.min(dataset['d'])
        dataset['metadata']['d_max'] = np.max(dataset['d'])
        dataset['metadata']['y_mean'] = np.mean(dataset['y'])

        #Min-Max归一化使得值域控制在[0,1]
        # dataset['y_normalized'] = (dataset['y'] - np.min(dataset['y'])) / (
        #         np.max(dataset['y']) - np.min(dataset['y']))

        #均值标准化y使得值域控制在[-1,1]
        # dataset['y_normalized'] = (dataset['y'] - dataset['metadata']['y_mean'])/(dataset['metadata']['y_max'] - dataset['metadata']['y_min'])

        #原本y的值域在[-6,6],除以6使得值域控制在[-1,1]
        dataset['y_normalized'] = (dataset['y']/6)
        train_indices, validation_indices, test_indices = get_split_indices(num_patients=dataset['x'].shape[0],
                                                                            patients=dataset['x'],
                                                                            treatments=dataset['t'],
                                                                            validation_fraction=self.validation_fraction,
                                                                            test_fraction=self.test_fraction)

        dataset['metadata']['train_index'] = train_indices
        dataset['metadata']['val_index'] = validation_indices
        dataset['metadata']['test_index'] = test_indices

        return dataset
