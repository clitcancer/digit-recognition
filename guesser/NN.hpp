#include <iostream>
#include <map>
#include <fstream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <math.h>
#include "json/json.h"
using namespace std;

vector<double> emptyVector(int length)
{
  vector<double> res;
  for (int i = 0; i < length; i++)
  {
    res.push_back(0);
  }
  return res;
}

typedef void (*func)(double *);

func getActivationFunction(string name)
{
  if (name == "ReLU")
    return [](double *x) { *x = *x > 0 ? *x : 0; };
  else if (name == "smoothReLU")
    return [](double *x) { *x = log10(1 + exp(*x)); };
  else if (name == "tanh")
    return [](double *x) { *x = tanh(*x); };
  else if (name == "sigmoid")
    return [](double *x) { *x = 1.0 / (1.0 + exp(-*x)); };
};

int NNGuess(Json::Value weights, Json::Value inputs, map<string, string> NN_config)
{
  auto activation = getActivationFunction(NN_config["activationFunction"]);

  // inputs
  auto sums = emptyVector(atoi(NN_config["neuronsPerHiddenLayer"].c_str()));
  for (int i = 0; i < sums.size(); i++)
  {
    for (int j = 0; j < atoi(NN_config["inputs"].c_str()); j++)
      sums[i] += (inputs[j].asDouble() * weights[0][i][j].asDouble());
    activation(&sums[i]);
  }

  //       # hidden
  //       for n in range(self.lengths.hiddenLayers-1):
  //           temp = [0 for x in range(self.lengths.thickness)]
  //           for i, node in enumerate(self.weights[1+n]):
  //               for j, weight in enumerate(node):
  //                   temp[i] += (sums[j] * weight)
  //               temp[i] = self.activation(temp[i])
  //           sums = [*temp]

  //       # output
  //       results = [0 for x in range(self.lengths.outputs)]
  //       for i, node in enumerate(self.weights[len(self.weights)-1]):
  //           for j, weight in enumerate(node):
  //               results[i] += (sums[j] * weight)

  //       return results.index(max(*results))
  return 1;
}
