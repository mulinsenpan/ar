# -*- encoding:"utf-8"-*-
# coding=utf-8

"""
序列分割，得到候选边界点
"""
import tools
import copy

SENSORLIST=[]
K = 3
FRAME_SIZE = 10
SIM_THETA = 0.1


def seg(sequences, frame_size=FRAME_SIZE, sim_theta=SIM_THETA):
    """
    :param sequences: 传感器序列
    :param frame_size: 窗口长度
    :param sim_theta: 相似度阈值
    :return: 候选边界集合（经过剪枝的边界）
    """
    length = len(sequences)
    borders = []
    sim_list = []
    for i in range(frame_size, length-frame_size + 1):
        seq_left = sequences[i-frame_size:i]
        seq_right = sequences[i:i+frame_size]
        shared_sensors = set(seq_left).intersection(set(seq_right))
        if len(shared_sensors) == 0:
            borders.append(i)
            sim_list.append(0)
        else:
            vector_left, matrix_left = convert2vector(seq_left)
            vector_right, matrix_right = convert2vector(seq_right)
            sim = float(sim_cos(vector_left,vector_right))
            if sim <= sim_theta:
                borders.append(i)
                sim_list.append(sim)
    new_borders = prunborders(borders,sim_list)
    new_borders.append(length-1)
    return new_borders


def convert2vector(seq):
    vector = []
    matrix = []
    for gap in range(K):
        index = 0
        sensor_matrix = [[0 for i in range(len(SENSORLIST))] for j in range(len(SENSORLIST))]
        while index < len(seq)-gap-1:
            sensor_matrix[seq[index]][seq[index+gap+1]] += 1
            index += 1
        matrix.append(sensor_matrix)
        for front in range(len(SENSORLIST)):
            for later in range(len(SENSORLIST)):
                vector.append(sensor_matrix[front][later])
    return vector, matrix


def distance_ed(vector1, vector2):
    """
    计算两个向量之间的长度——欧式距离
    两者均非零的模式权重为w1，一个为零另一个不为零的权重为w2,w1和w2为全局变量。
    :param vector1:
    :param vector2:
    :return:
    """
    index = 0
    sum_zero = 0
    sum_none_zero = 0
    while index < len(vector1):
        if vector1[index] != 0 and vector2[index] != 0:
            sum_none_zero += (float(vector1[index]-vector2[index])**2)
        if vector1[index] == 0 or vector2[index] == 0:
            sum_zero += (float(vector1[index]-vector2[index])**2)
        index += 1
    ed =  (sum_none_zero ** 0.5) +  (sum_zero ** 0.5)
    return ed


def sim_cos(vector1,vector2):
    """
    :param vector1: left
    :param vector2: right
    :return: 余弦相似度
    """
    numerator = sum((vector1[i] * vector2[i]) for i in range(len(vector1))) + 0.0
    denominator = ((sum(value1 ** 2 for value1 in vector1))**0.5) * ((sum(value1 ** 2 for value1 in vector1))**0.5)

    return numerator/float(denominator)


def prunborders(borders,sim_list):
    new_borders = []
    index = 0
    while index < len(borders)-2:
        continue_borders = isContinue(borders,index)
        if len(continue_borders) > 0:
            min_index = continue_borders[0]
            for value in continue_borders:
                if sim_list[value] < sim_list[min_index]:
                    min_index = value
            # min_index = sim_list.index(min(sim_list[continue_borders[0]:continue_borders[-1]]))
            new_borders.append(borders[min_index])
            index = continue_borders[-1]+2
        else:
            new_borders.append(borders[index])
            index += 1
    return new_borders


def isContinue(borders, current):
    continue_index = []
    for index in range(current,len(borders)):
        later = index + 1
        try:
            if borders[later] - borders[index] < 10:
                continue_index.append(index)
            else:
                return continue_index
        except:
            print index, later


# if __name__ == "__main__":
#     borders =[10,11,13,16,19,35,49,80,112,113,114,158,190,200,250]
#
#     sim_list =[0.1,0.2,0.3,0.1,0.5,0.6,0.4,0.3,0.6,0.2,0.4,0.6,0.7,0.2,0.1]
#     new_borders= prunborders(borders,sim_list)
#     print new_borders

