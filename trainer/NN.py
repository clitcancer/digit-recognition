import random
import json
import numpy as np


class NetworkLengths:
    def __init__(self, inputs, outputs, hiddenLayers, thickness):
        self.inputs = inputs
        self.outputs = outputs
        self.hiddenLayers = hiddenLayers
        self.thickness = thickness

class Biases:
    def __init__(self, hidden, output):
        self.hidden = hidden
        self.output = output

class Weights:
    def __init__(self, inputs, hidden, output):
        self.inputs = inputs
        self.hidden = hidden
        self.output = output


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

        self.weights = Weights(
            inputs=np.random.rand(thicknessLength, inputsLength),
            hidden=np.random.rand(hiddenLayersLength-1, thicknessLength, thicknessLength),
            output=np.random.rand(outputsLength, thicknessLength)
        )
        
        self.biases = Biases(
            hidden=np.random.rand(hiddenLayersLength, thicknessLength),
            output=np.random.rand(outputsLength)
        )

    def feedforward(self, inputs):
        wrong = False
        wrong = len(inputs) != self.lengths.inputs or wrong
        wrong = not all(x <= 1 and x >= 0 for x in inputs) or wrong
        if wrong:
            raise Exception('wrong inputs')

        inputs = np.array(inputs)

        # input
        sums = np.matmul(self.weights.inputs, inputs) + self.biases.hidden[0]
        sums = np.array(list(map(self.activation, sums)))

        # hidden
        for n in range(self.lengths.hiddenLayers-1):
            temp = np.matmul(self.weights.hidden[n], sums) + self.biases.hidden[n+1]
            temp = np.array(list(map(self.activation, temp)))
            sums = np.array(temp)
        
        # output
        results = np.matmul(self.weights.output, sums) + self.biases.output

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
                'weights': [
                    self.weights.inputs.tolist(),
                    *self.weights.hidden.tolist(),
                    self.weights.output.tolist()
                ],
                'biases': [
                    *self.biases.hidden.tolist(), 
                    self.biases.output.tolist()
                ]
            }
            json.dump(obj, f, indent=4)

    def load(self, path):
        with open(path) as f:
            obj = json.load(f)
            self.weights = Weights(
                inputs=np.array(obj['weights'][0]),
                hidden=np.array(obj['weights'][1:-1]),
                output=np.array(obj['weights'][-1])
            )
            self.biases = Biases(
                hidden=np.array(obj['biases'][:-1]),
                output=np.array(obj['biases'][-1])
            )
