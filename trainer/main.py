import requests
import itertools
import yaml

from NN import NN
import activation_functions as af


def getDigit(n, setType):
    URL = "http://localhost:214/api/getDigit/{setType}/{n}".format(
        setType=setType,
        n=str(n)
    )
    r = requests.get(url=URL)
    return r.json()

def from2dto1d(arr):
	return list(itertools.chain(*arr))

def normalize(inputs, to):
    return list(map(lambda x: x/to, inputs))


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
    dig = getDigit(123, "test")
    inputs = from2dto1d(dig['pixels'])
    inputs = normalize(inputs, 255)

    print(nn.guess(inputs), dig['label'])
