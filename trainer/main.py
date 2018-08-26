import requests
import itertools
import yaml
import sys
import random
from math import floor

from NN import NN
import activation_functions as af


def getDigit(n, setType):
    URL = 'http://localhost:214/api/getDigit/{setType}/{n}'.format(
        setType=setType,
        n=str(n)
    )
    res = requests.get(url=URL)
    return res.json()


def from2dto1d(arr):
    return list(itertools.chain(*arr))


def normalize(inputs, to):
    return list(map(lambda x: x/to, inputs))


def printProgress(progress):
    print(' [' + '█'*(floor(progress*10)) + ' '*(floor(10 - progress*10)) + ']',
          str(round(progress*100, 1)) + '%', end='\r')


if __name__ == '__main__':
    with open('../NN_config.yaml') as f:
        NN_config = yaml.load(f)

    nn = NN(
        inputsLength=NN_config['lengths']['inputs'],
        outputsLength=NN_config['lengths']['outputs'],
        hiddenLayersLength=NN_config['lengths']['hiddenLayers'],
        thicknessLength=NN_config['lengths']['neuronsPerHiddenLayer'],
        activation=getattr(af, NN_config['activationFunction'])
    )
    nn.load('../brain.json')

    print('Training...')
    epoches = int(sys.argv[1])
    for n in range(epoches):
        dig = getDigit(random.randint(1, 60000), 'train')
        inputs = from2dto1d(dig['pixels'])
        inputs = normalize(inputs, 255)
        nn.guess(inputs)

        printProgress((n+1)/epoches)
    print('Done training! Time for tests.')

    print('Testing...')
    testAmount = 1000
    correctAmount = 0
    for n in range(testAmount):
        dig = getDigit(random.randint(1, 10000), 'test')
        inputs = from2dto1d(dig['pixels'])
        inputs = normalize(inputs, 255)
        correctAmount += int(int(nn.guess(inputs)) == int(dig['label']))

        printProgress((n+1)/testAmount)
    print('Done testing! {accuracy}% accuracy.'.format(accuracy=round(correctAmount/testAmount*100, 1)))
