import sys
import pickle
import re
from collections import Counter

def TagWord(line, feature_list, class_list, weight):
        tag = class_list.get(1)
        list = line.split()
        prod = [0] *len(class_list)
        count = Counter(list)
        for key,  value in count.items():
            if key in feature_list:
                for i in range(0, len(weight)):
                     prod[i] = prod[i] + value * weight[i][feature_list[key]]
        z = prod.index(max(prod))
        for key,  value in class_list.items():
            if value == z:
                tag = key
        return tag

def main(argv):
    model_file = open(argv[0], 'rb')
    model = pickle.load(model_file)
    feature_list = model['features']
    class_list = model['class']
    weight = model['weight']
    feature = {}
    #lines = sys.stdin.readlines()
    for line in sys.stdin:
        list = line.split()
        i = 0
        for item in list:
            current = item
            wshape = re.sub(r'[A-Z]', 'A', current)
            wshape = re.sub(r'[a-z]', 'a', wshape)
            wshape = re.sub(r'[0-9]', '9', wshape)
            wshape = re.sub(r'[^A-Za-z0-9]', '-', wshape)
            wshape = re.sub(r'A+', 'A', wshape)
            wshape = re.sub(r'a+', 'a', wshape)
            wshape = re.sub(r'9+', '9', wshape)
            wshape = re.sub(r'-+', '-', wshape)
            if i == 0:
                feature[0] = 'PREV_BOS'
            else:
                feature[0] = 'PREV_'+list[i-1]
            feature[1] = 'CURR_'+current
            if len(current) < 3:
                feature[3] = 'SUFFIX3_'
            else:
                feature[3] = 'SUFFIX3_'+current[-3:]
            if len(current) < 2:
                feature[4] = 'SUFFIX2_'
            else:
                feature[4] = 'SUFFIX2_'+current[-2:]
            if i == len(list) - 1:
                feature[2] = 'NEXT_EOS'
            else:
                feature[2] = 'NEXT_'+list[i+1]
            feature[5] = 'WSHAPE_'+wshape
            feature_line = feature[0] + ' '+ feature[1] + ' '+ feature[2]+' '+ feature[3] + ' '+ feature[4]+ ' '+feature[5]
            tag= TagWord(feature_line, feature_list, class_list, weight)
            if i == len(list) - 1:
                 print(current+'/'+tag+'\n', end='')
            else:
                 print(current+'/'+tag+' ', end='')
            i=i+1
if __name__ == "__main__":
    main(sys.argv[1:])
