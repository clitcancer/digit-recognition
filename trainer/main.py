import requests
import itertools

from NN import NN
from activation_functions import reLu
from utils import dotDict


def getDigit(n, setType):
    URL = "http://localhost:214/api/getDigit/{setType}/{n}".format(
        setType=setType,
        n=str(n)
    )
    r = requests.get(url=URL)
    return dotDict(r.json())

def from2dto1d(arr):
	return list(itertools.chain(*arr))


nn = NN(
    inputsLength=784,
    outputsLength=10,
    hiddenLayersLength=2,
    thicknessLength=16,
    activation=reLu
)
dig = getDigit(123, "test")

print(nn.guess(from2dto1d(dig.pixels)), dig.label)
