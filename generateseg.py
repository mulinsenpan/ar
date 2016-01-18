# -*- encoding:"utf-8"-*-
# coding=utf-8

"""
1、根据获得的边界点集合，生成序列片段
2、根据多数投票原则，为每个序列片段标记相应的活动标号
"""
import annotation
import segment
import featureext
import tools

#
# def trainingdata(filename):
#     X = []
#     origin_labels = annotation.origin_annotation(filename)
#     segment.SENSORLIST = tools.getSensorList(filename)
#     origin_data = []
#     seq_index = []
#
#     with open(filename, 'r') as fr:
#         for line in fr:
#             row = line.split()
#             seq_index.append(segment.SENSORLIST.index(row[2]))
#             origin_data.append(row)
#     borders = segment.seg(seq_index)
#
#     """
#     trainingdata---featurevector---segment_data
#     """
#
#     for index in range(0, len(borders)):
#         segment_data = []
#         if index == 0:
#             start = 0
#             finish = borders[index]
#
#         if index > 0:
#             start = borders[index-1] + 1
#             finish = borders[index]
#             # segment_data.append(origin_data[start:finish])
#         segment_data.append(origin_data[start:finish])
#         fea_vector = featureext.feature(segment_data)
#         X.append(fea_vector)
#         print segment_data
#     y_true = annotation.seg_labels(origin_labels,borders)[1]
#     return X,y_true
#
#
# if __name__ == "__main__":
#     filename = "/home/chi/PycharmProjects/Seg_AR/data/example"
