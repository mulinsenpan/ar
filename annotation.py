# -*- encoding:"utf-8"-*-
# coding=utf-8

"""
为每个传感器事件分类所属类别
"""
import segment
import tools


def origin_annotation(filename):
    """
    获取源数据文件中每个传感器对应的行为
    :param filename:
    :return:
    """
    origin_labels = []
    with open(filename, 'r') as fr:
        temp_label = []    # temp_label 中保证仅有一个行为标签
        for line in fr:
            row = line.split()
            if len(row) > 4:
                if row[-1] == 'begin':
                    temp_label.append(row[-2])
                if row[-1] == 'end':
                    origin_labels.append(row[-2])
                    continue
            if len(temp_label) > 0:
                origin_labels.append(temp_label[-1])
            if len(temp_label) == 0:
                origin_labels.append("other")
    return origin_labels


def seg_labels(o_labels, borders):
    """

    :param o_labels:
    :param borders:
    :return:
    """
    segment_labels = []
    for index in range(0, len(borders)):
        if index == 0:
            start = 0
            finish = borders[index]
            vote_label = vote(start, finish, borders, origin_labels)
            for i in range(start,finish+1):
                segment_labels.append(vote_label)
        if index > 0:
            start = borders[index-1] + 1
            finish = borders[index]
            vote_label = vote(start, finish, borders, origin_labels)
            for i in range(start,finish+1):
                segment_labels.append(vote_label)
    return segment_labels


def vote(start, finish, borders, o_labels):
    label_dic = {}
    max_num = 0
    max_label = o_labels[start]

    for event in o_labels[start:finish]:
        if event not in label_dic.keys():
            label_dic[event] = 0
        label_dic[event] += 1

    for key, value in label_dic.items():
        if value > max_num:
            max_label = key
            max_num = value
    return max_label


if __name__ == "__main__":
    filename = "G:/Seg_AR/data/example"
    origin_labels = origin_annotation(filename)
    segment.SENSORLIST = tools.getSensorList(filename)
    seq_index = []
    with open(filename, 'r') as fr:
        for line in fr:
            row = line.split()
            seq_index.append(segment.SENSORLIST.index(row[2]))
    borders = segment.seg(seq_index)
    segment_labels = seg_labels(origin_labels, borders)
