import math


class ActivationFunction:
    def __init__(self, base, prime):
        self.base = base
        self.prime = prime


tanh = ActivationFunction(
    lambda x: math.tanh(x),
    lambda y: 1 - y**2
)

sigmoid = ActivationFunction(
    lambda x: 1 / (1 + math.exp(-x)),
    lambda y: y * (1-y)
)

ReLU = ActivationFunction(
    lambda x: x if x > 0 else 0,
    lambda y: 1 if y > 0 else 0
)

# smoothReLU = ActivationFunction(
#     lambda x: math.log10(1 + math.exp(x)),
#     sigmoid.base
# )
