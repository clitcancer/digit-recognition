import math

from utils import dotDict


reLu = dotDict()
reLu.base = lambda x: x if x > 0 else 0
reLu.derivative = lambda x: 1 if x > 0 else 0

tanh = dotDict()
tanh.base = lambda x: math.tanh(x)
tanh.derivative = lambda x: 1 - math.tanh(x)**2

sigmoid = dotDict()
sigmoid.base = lambda x: 1 / (1 + math.exp(-x))
sigmoid.derivative = lambda x: sigmoid.base(x)*(1-sigmoid.base(x))
