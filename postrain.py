import sys
import re
import perceplearn
import os

def createtempfile(input, output):
    feature = {}
    for line in input:
        list = line.split()
        i = 0
        for item in list:
            cls = item.split('/')[1]
            current = item.split('/')[0]
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
                feature[0] = 'PREV_'+list[i-1].split('/')[0]
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
                feature[2] = 'NEXT_'+list[i+1].split('/')[0]
            feature[5] = 'WSHAPE_'+wshape
            output.write(cls + ' ' + feature[0] + ' '+ feature[1] + ' '+ feature[2]+' '+ feature[3] + ' '+ feature[4]+ ' '+feature[5]+'\n')
            i=i+1

def main(argv):
    if len(argv) == 2:
        if not os.path.exists(argv[0]) :
            print(argv[0] + ' does not exist')
            sys.exit()
        if not os.path.isfile(argv[0]):
            print(argv[0] + ' not a file')
            sys.exit()
        args = ['trainposfile4'] + [argv[1]]
        train = open(argv[0], 'r')
        train_temp = open('trainposfile4', 'w')
        createtempfile(train, train_temp)
        perceplearn.main(args)
        os.remove('trainposfile4')
    elif len(argv) == 4 and argv[2]  == '-h':
        if not os.path.exists(argv[0]) :
            print(argv[0] + ' does not exist')
            sys.exit()
        if not os.path.isfile(argv[0]):
            print(argv[0] + ' not a file')
            sys.exit()
        if not os.path.exists(argv[3]) :
            print(argv[3] + ' does not exist')
            sys.exit()
        if not os.path.isfile(argv[3]):
            print(argv[3] + ' not a file')
            sys.exit()
        train = open(argv[0], 'r')
        dev = open(argv[3], 'r')
        train_temp = open('trainposfile4', 'w')
        dev_temp = open('devposfile4', 'w')
        createtempfile(train, train_temp)
        createtempfile(dev, dev_temp)
        args = ['trainposfile4'] + [argv[1]] + [argv[2]] + ['devposfile4']
        perceplearn.main(args)
        os.remove('trainposfile4')
        os.remove('devposfile4')
    else:
        print("Usage: python3 postrain.py TRAININGFILE MODELFILE [-h DEVFILE]")
        sys.exit()
    
if __name__=="__main__":
    main(sys.argv[1:])
