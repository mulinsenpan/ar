# -*- encoding:"utf-8"-*-
# coding=utf-8

"""
序列分割，得到候选边界点
"""
import tools
import copy

SENSORLIST = []
K = 3


def seg(sequences, frame_size, sim_theta):
    """
    :param sequences: 传感器序列
    :param frame_size: 窗口长度
    :param sim_theta: 相似度阈值
    :return: 候选边界集合（经过剪枝的边界）
    """
    print frame_size, sim_theta
    length = len(sequences)
    borders = []
    sims_list = []
    for i in range(frame_size, length - frame_size):

        seq_left = sequences[i - frame_size:i+1]
        seq_right = sequences[i+1:i + frame_size+1]
        shared_sensors = set(seq_left).intersection(set(seq_right))
        if len(shared_sensors) == 0:
            borders.append(i)
            sims_list.append(0)
        else:
            vector_left, matrix_left = convert2vector(seq_left)
            vector_right, matrix_right = convert2vector(seq_right)
            sim = float(sim_cos(vector_left, vector_right))
            if sim <= sim_theta:
                borders.append(i)
                sims_list.append(sim)
    borders.append(length-1)
    new_borders = prunborders(borders, sims_list)
    new_borders.append(length - 1)
    return new_borders


def convert2vector(seq):
    vector = []
    matrix = []
    for gap in range(K):
        index = 0
        sensor_matrix = [[0 for i in range(len(SENSORLIST))] for j in range(len(SENSORLIST))]
        while index < len(seq) - gap - 1:
            sensor_matrix[seq[index]][seq[index + gap + 1]] += 1
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
            sum_none_zero += (float(vector1[index] - vector2[index]) ** 2)
        if vector1[index] == 0 or vector2[index] == 0:
            sum_zero += (float(vector1[index] - vector2[index]) ** 2)
        index += 1
    ed = (sum_none_zero ** 0.5) + (sum_zero ** 0.5)
    return ed


def sim_cos(vector1, vector2):
    """
    :param vector1: left
    :param vector2: right
    :return: 余弦相似度
    """
    numerator = sum((vector1[i] * vector2[i]) for i in range(len(vector1))) + 0.0
    denominator = ((sum(value1 ** 2 for value1 in vector1)) ** 0.5) * ((sum(value1 ** 2 for value1 in vector1)) ** 0.5)
    return numerator / float(denominator)


def prunborders(border_list, sim_list):
    new_borders = []
    index = 0
    while index < len(border_list) - 1:
        continue_borders = isContinue(border_list, index)
        if len(continue_borders) > 1:
            min_border = continue_borders[0]
            for border in continue_borders:
                if sim_list[border] < sim_list[min_border]:
                    min_border = border
            # min_index = sim_list.index(min(sim_list[continue_borders[0]:continue_borders[-1]]))
            new_borders.append(border_list[min_border])
            # index = border_list.index(continue_borders[-1]) + 1
            index += len(continue_borders)
        if len(continue_borders) == 1:
            new_borders.append(border_list[index])
            index += 1
    return new_borders


def isContinue(border_list, current_index):
    continue_list = [current_index]
    for ind in range(current_index, len(border_list) - 1):
        later = ind + 1
        if border_list[later] - border_list[ind] < 10:
            continue_list.append(later)
        if border_list[later] - border_list[ind] >= 10:
            return continue_list


# if __name__ == "__main__":
#
#     filename = "/home/chi/PycharmProjects/Seg_AR/data/example"
#     SENSORLIST = tools.getSensorList(filename)
#     seq_index = []
#     with open(filename, 'r') as fr:
#         for line in fr:
#             row = line.split()
#             seq_index.append(SENSORLIST.index(row[2]))
#     sizes=[10,20,30,40,50]
#     thetas = [0.01,0.05,0.1,0.15,0.2,0.25,0.3]
#     for size in sizes:
#         for theta in thetas:
#             border_1 = seg(seq_index, size, theta)
#             print border_1
