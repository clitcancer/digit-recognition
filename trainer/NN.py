import random
import json
import numpy as np


class NetworkLengths:
    def __init__(self, inputs, outputs, hiddenLayers, thickness):
        self.inputs = inputs
        self.outputs = outputs
        self.hiddenLayers = hiddenLayers
        self.thickness = thickness


class NN:
    def __init__(self, inputsLength, outputsLength, hiddenLayersLength, thicknessLength, activation, learningRate):
        self.lengths = NetworkLengths(
            inputsLength,
            outputsLength,
            hiddenLayersLength,
            thicknessLength
        )

        self.setLearningRate(learningRate)
        
        self.activation = activation.base
        self.activationDerivative = activation.derivative

        self.weights = np.array([
            [[random.random() for x in range(inputsLength)]
             for x in range(thicknessLength)],
            *[[[random.random() for x in range(thicknessLength)]
               for x in range(thicknessLength)] for x in range(hiddenLayersLength-1)],
            [[random.random() for x in range(thicknessLength)]
             for x in range(outputsLength)]
        ])

        self.biases = np.array([
            *[[random.random() for x in range(thicknessLength)]
              for x in range(hiddenLayersLength)],
            [random.random() for x in range(outputsLength)]
        ])

    def feedforward(self, inputs):
        wrong = False
        wrong = len(inputs) != self.lengths.inputs or wrong
        wrong = not all(x <= 1 and x >= 0 for x in inputs) or wrong
        if wrong:
            raise Exception('wrong inputs')

        inputs = np.array(inputs)

        # input
        sums = np.matmul(self.weights[0], inputs) + self.biases[0]
        sums = np.array(list(map(self.activation, sums)))

        # hidden
        for n in range(self.lengths.hiddenLayers-1):
            temp = np.matmul(self.weights[n+1], sums) + self.biases[n+1]
            temp = np.array(list(map(self.activation, temp)))
            sums = np.array(temp)

        # output
        results = np.matmul(self.weights[-1], sums) + self.biases[-1]

        return results

    def guess(self, inputs):
        results = self.feedforward(inputs)
        return np.argmax(results)

    @staticmethod
    def softmax(arr):
        arr -= arr.max()

        e_x = np.exp(arr - np.max(arr))
        return e_x / e_x.sum(axis=0)

    def setLearningRate(self, lr):
        self.learningRate = lr

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
            self.weights = np.array(obj['weights'])
            self.biases = np.array(obj['biases'])
