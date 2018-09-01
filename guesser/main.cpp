#include <iostream>
#include <map>
#include <fstream>
#include <string>
#include "NN.hpp"
#include "json/json.h"

using namespace std;

bool startsWith(string what, string with)
{
	return !what.compare(0, with.size(), with);
}

map<string, string> getNNInfo(string path)
{
	// yes, thats a lot of hardcoding, coudnt be bothered
	map<string, string> res;

	ifstream f;
	f.open(path);
	string line;
	while (getline(f, line))
	{
		if (startsWith(line, "lengths:"))
		{
			while (getline(f, line))
			{
				if (startsWith(line, string(1, '\t')) || startsWith(line, "  "))
				{
					string currProp("");
					string currVal("");

					int start;
					for (start = 0; line[start] == '\t' || line[start] == ' '; start++) {}

					int i;
					for (i = start; line[i] != ':'; i++) {}

					currProp = line.substr(start, i - start);

					i += 2;
					start = i;
					for (; line[i] != ' ' && line[i] != '\n' && line[i] != '\t'; i++) {}

					currVal = line.substr(start, i - start);

					res[currProp] = currVal;
				}
				else
				{
					break;
				}
			}
		}
		if (startsWith(line, "activationFunction:"))
		{
			int start = 21;
			int i;
			for (i = start; line[i] != ' ' && line[i] != '\n' && line[i] != '\t' && line[i] != '\''; i++){}
			res["activationFunction"] = line.substr(start, i - start);
		}
	}
	f.close();

	return res;
}

Json::Value loadJson(string path)
{
	Json::Value obj;
	ifstream config_doc(path, ifstream::binary);
	config_doc >> obj;
	return obj;
}

Json::Value parseJson(string json)
{
	Json::CharReaderBuilder builder;
	Json::CharReader *reader = builder.newCharReader();

	Json::Value obj;
	string errors;

	bool parsingSuccessful = reader->parse(
			json.c_str(),
			json.c_str() + json.size(),
			&obj,
			&errors);
	delete reader;

	if (!parsingSuccessful)
		cout << "Failed to parse the JSON, errors:" << endl << errors << endl;
	else
		return obj;
}

int main(int argc, char *argv[])
{
	auto brain = loadJson("../brain.json");

	auto inputs = parseJson(argv[1]);
	
	auto NN_config = getNNInfo("../NN_config.yaml");

	int guess = NNGuess(brain["weights"], brain["biases"], inputs, NN_config);

	cout << guess;
}
