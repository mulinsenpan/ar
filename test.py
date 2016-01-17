# -*- encoding:"utf-8"-*-
# coding=utf-8

import tools
import segment

filename = "G:/Seg_AR/data/annotated"
segment.SENSORLIST = tools.getSensorList(filename)

seq_index = []
with open(filename, 'r') as fr:
    for line in fr:
        row = line.split()
        seq_index.append(segment.SENSORLIST.index(row[2]))
print len(seq_index)

borders = segment.seg(seq_index)
print len(borders)
print borders

