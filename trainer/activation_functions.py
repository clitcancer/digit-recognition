import math


class ActivationFunction:
    def __init__(self, base, derivative):
        self.base = base
        self.derivative = derivative


tanh = ActivationFunction(
    lambda x: math.tanh(x),
    lambda x: 1 - math.tanh(x)**2
)

sigmoid = ActivationFunction(
    lambda x: 1 / (1 + math.exp(-x)),
    lambda x: sigmoid.base(x)*(1-sigmoid.base(x))
)

ReLU = ActivationFunction(
    lambda x: x if x > 0 else 0,
    lambda x: 1 if x > 0 else 0
)

smoothReLU = ActivationFunction(
    lambda x: math.log10(1 + math.exp(x)),
    lambda x: sigmoid.base
)
