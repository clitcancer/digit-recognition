import random
import json


class NetworkLengths:
    def __init__(self, inputs, outputs, hiddenLayers, thickness):
        self.inputs = inputs
        self.outputs = outputs
        self.hiddenLayers = hiddenLayers
        self.thickness = thickness


class NN:
    def __init__(self, inputsLength, outputsLength, hiddenLayersLength, thicknessLength, activation):
        self.lengths = NetworkLengths(
            inputsLength,
            outputsLength,
            hiddenLayersLength,
            thicknessLength
        )

        self.activation = activation.base
        self.activationDerivative = activation.derivative

        self.weights = [
            [[random.random() for x in range(inputsLength)]
             for x in range(thicknessLength)],
            *[[[random.random() for x in range(thicknessLength)]
               for x in range(thicknessLength)] for x in range(hiddenLayersLength-1)],
            [[random.random() for x in range(thicknessLength)]
             for x in range(outputsLength)],
        ]

    def guess(self, inputs):
        wrong = False
        wrong = len(inputs) != self.lengths.inputs or wrong
        wrong = not all(x <= 1 and x >= 0 for x in inputs) or wrong
        if wrong:
            raise Exception('wrong inputs')

        # inputs
        sums = [0 for x in range(self.lengths.thickness)]
        for i, node in enumerate(self.weights[0]):
            for j, weight in enumerate(node):
                sums[i] += (inputs[j] * weight)
            sums[i] = self.activation(sums[i])

        # hidden
        for n in range(self.lengths.hiddenLayers-1):
            temp = [0 for x in range(self.lengths.thickness)]
            for i, node in enumerate(self.weights[1+n]):
                for j, weight in enumerate(node):
                    temp[i] += (sums[j] * weight)
                temp[i] = self.activation(temp[i])
            sums = [*temp]

        # output
        results = [0 for x in range(self.lengths.outputs)]
        for i, node in enumerate(self.weights[len(self.weights)-1]):
            for j, weight in enumerate(node):
                results[i] += (sums[j] * weight)

        return results.index(max(*results))

    def nodeCount(self):
        return self.lengths.inputs + self.lengths.outputs + self.lengths.hiddenLayers*self.lengths.thickness

    def weightCount(self):
        sum = self.lengths.inputs * self.lengths.thickness
        for _ in range(self.lengths.hiddenLayers-1):
            sum += (self.lengths.thickness ** 2)
        sum += self.lengths.outputs * self.lengths.thickness
        return sum

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.weights, f, indent=4)

    def load(self, path):
        with open(path) as f:
            self.weights = json.load(f)
