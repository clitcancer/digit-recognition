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

int NNGuess(Json::Value weights, Json::Value biases, Json::Value inputs, map<string, string> NN_config)
{
  auto activation = getActivationFunction(NN_config["activationFunction"]);

  // inputs
  auto sums = emptyVector(atoi(NN_config["neuronsPerHiddenLayer"].c_str()));
  for (int i = 0; i < sums.size(); i++)
  {
    for (int j = 0; j < atoi(NN_config["inputs"].c_str()); j++)
      sums[i] += (inputs[j].asDouble() * weights[0][i][j].asDouble());
    sums[i] += biases[0][i].asDouble();
    activation(&sums[i]);
  }

  // hidden
  for (int n = 1; n < atoi(NN_config["hiddenLayers"].c_str()); n++)
  {
    auto temp = emptyVector(atoi(NN_config["neuronsPerHiddenLayer"].c_str()));
    for (int i = 0; i < temp.size(); i++)
    {
      for (int j = 0; j < atoi(NN_config["neuronsPerHiddenLayer"].c_str()); j++)
        temp[i] += (sums[j] * weights[n][i][j].asDouble());
      temp[i] += biases[n][i].asDouble();
      activation(&temp[i]);
    }
    for(int a = 0; a < temp.size(); a++)
      sums[a] = temp[a];
  }

  // output
  auto results = emptyVector(atoi(NN_config["outputs"].c_str()));
  for (int i = 0; i < results.size(); i++)
  {
    for (int j = 0; j < sums.size(); j++)
      results[i] += sums[j] * weights[atoi(NN_config["hiddenLayers"].c_str())][i][j].asDouble();
    results[i] += biases[atoi(NN_config["hiddenLayers"].c_str())][i].asDouble();
  }

  // result
  double best = -100000.0;
  int hisIndex = -1;
  for(int i = 0; i < results.size(); i++) {
    if(results[i] > best) {
      best = results[i];
      hisIndex = i;
    }
  }

  return hisIndex;
}
