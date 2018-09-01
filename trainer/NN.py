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
             for x in range(outputsLength)]
        ]

        self.biases = [
            *[[random.random() for x in range(thicknessLength)]
              for x in range(hiddenLayersLength)],
            [random.random() for x in range(outputsLength)]
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
            sums[i] = sum(input*weight for input, weight in zip(inputs, node))
            sums[i] = self.activation(sums[i] + self.biases[0][i])

        # hidden
        for n in range(self.lengths.hiddenLayers-1):
            temp = [0 for x in range(self.lengths.thickness)]
            for i, node in enumerate(self.weights[n+1]):
                temp[i] = sum(sum_*weight for sum_, weight in zip(sums, node))
                temp[i] = self.activation(temp[i] + self.biases[n+1][i])
            sums = [*temp]

        # output
        results = [0 for x in range(self.lengths.outputs)]
        for i, node in enumerate(self.weights[len(self.weights)-1]):
            results[i] = sum(sum_*weight for sum_, weight in zip(sums, node)) + self.biases[len(self.biases)-1][i]

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
            obj = {
                'weights': self.weights,
                'biases': self.biases
            }
            json.dump(obj, f, indent=4)

    def load(self, path):
        with open(path) as f:
            obj = json.load(f)
            self.weights = obj['weights']
            self.biases = obj['biases']
