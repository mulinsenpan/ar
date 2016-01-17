# -*- encoding:"utf-8"-*-
# coding=utf-8

"""
1、根据多数投票原则，得到每个序列片段的类标号
2、为每个传感器事件标记所属片段的类标号
3、构造混淆矩阵，初步评估划分效果
4、使用不同的阈值和窗口长度，得到最佳的阈值和窗口长度。
"""

import annotation
import segment
import tools
from sklearn.metrics import confusion_matrix


def confusionmatrix():
    filename = "/home/chi/PycharmProjects/Seg_AR/data/example"
    origin_labels = annotation.origin_annotation(filename)
    segment.SENSORLIST = tools.getSensorList(filename)
    seq_index = []
    with open(filename, 'r') as fr:
        for line in fr:
            row = line.split()
            seq_index.append(segment.SENSORLIST.index(row[2]))
    borders = segment.seg(seq_index)
    segment_labels = annotation.seg_labels(origin_labels, borders)
    cm = confusion_matrix(origin_labels,segment_labels)

    return cm

def accuracy(cm):
    row_num = len(cm)
    right_num = 0
    for i in range(row_num):
        right_num += cm[i][i]
    total_num = sum(cm.sum(0))

    return float(right_num)/float(total_num)

if __name__ == "__main__":

    result =[]

    frame_sizes = range(10,150,5)
    sim_thetas = [0,0.05,0.1,0.15,0.2,0.25,0.5]
    for size in frame_sizes:
        for sim in sim_thetas:
            for gap in frame_sizes:
                segment.FRAME_SIZE = size
                segment.SIM_THETA = sim
                segment.GAP = gap
                a = confusionmatrix()
                accu = accuracy(a)
                print size,sim,gap,accu
                result.append([size,sim,gap,accu])





