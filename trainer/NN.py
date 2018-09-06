import json
import numpy as np
from functools import reduce


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
        self.activationPrime = activation.prime

        self.weights = Weights(
            inputs=np.random.randn(thicknessLength, inputsLength),
            hidden=np.random.randn(hiddenLayersLength-1, thicknessLength, thicknessLength),
            output=np.random.randn(outputsLength, thicknessLength)
        )
        
        self.biases = Biases(
            hidden=np.random.randn(hiddenLayersLength, thicknessLength),
            output=np.random.randn(outputsLength)
        )

    def feedforward(self, inputs):
        wrong = False
        wrong = len(inputs) != self.lengths.inputs or wrong
        wrong = not all(x <= 1 and x >= 0 for x in inputs) or wrong
        if wrong:
            raise Exception('wrong inputs')

        self.nodeSave = []

        inputs = np.array(inputs, 'float64')
        self.nodeSave.append(np.array(inputs, 'float64'))


        # input
        sums = np.matmul(self.weights.inputs, inputs) + self.biases.hidden[0]
        sums = np.array(list(map(self.activation, sums)), 'float64')
        self.nodeSave.append(np.array(sums, 'float64'))
        
        # hidden
        for n in range(self.lengths.hiddenLayers-1):
            temp = np.matmul(self.weights.hidden[n], sums) + self.biases.hidden[n+1]
            temp = np.array(list(map(self.activation, temp)), 'float64')
            sums = np.array(temp, 'float64')
            self.nodeSave.append(np.array(sums, 'float64'))
        
        # output
        results = np.matmul(self.weights.output, sums) + self.biases.output
        results = NN.softmax(results)

        return results

    def guess(self, inputs):
        results = self.feedforward(inputs)
        return np.argmax(results)

    def backpropagate(self, inputs, targets, outputs):
        inputs = np.array(inputs, 'float64')
        targets = np.array(targets, 'float64')
        outputs = np.array(outputs, 'float64')

        network_loss = np.sum(((targets - outputs)**2) / 2)

        # output adjustment data
        outputError = targets - outputs

        outputGradients = np.array(list(map(self.activationPrime, outputs)), 'float64')
        outputGradients *= self.learningRate
        outputGradients *= outputError

        outputDeltas = np.dot(outputGradients[:,None], self.nodeSave[-1][None])


        # hidden adjustment data
        hiddenDeltas = []
        hiddenGradients = []
        for n in range(self.lengths.hiddenLayers):
            if n is 0:
                hiddenError = outputGradients.dot(self.weights.output)
            else:
                hiddenError = hiddenGradient.dot(self.weights.hidden[-n])

            hiddenGradient = np.array(list(map(self.activationPrime, self.nodeSave[-n-1])), 'float64')
            hiddenGradient *= self.learningRate
            hiddenGradient *= hiddenError
            hiddenGradients.append(hiddenGradient)

            hiddenDeltas.append(np.dot(hiddenGradient[:,None], self.nodeSave[-n-2][None]))

        # adjust weights
        self.weights.output += outputDeltas
        for n in range(self.lengths.hiddenLayers-1):
            self.weights.hidden[-n-1] += hiddenDeltas[n]
        self.weights.inputs += hiddenDeltas[-1]

        # adjust biases
        self.biases.output += outputGradients
        self.biases.hidden += np.flip(hiddenGradients, axis=0)


        return network_loss

    def train(self, inputs, targets):
        outputs = self.feedforward(inputs)
        loss = self.backpropagate(inputs, targets, outputs)
        return loss
        

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
        def multAll(tpl):
            return reduce(lambda prev, curr: prev*curr, tpl)

        total = multAll(self.weights.inputs.shape)
        total += multAll(self.weights.hidden.shape)
        total += multAll(self.weights.output.shape)

        total += multAll(self.biases.hidden.shape)
        total += multAll(self.biases.output.shape)
        return total

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
