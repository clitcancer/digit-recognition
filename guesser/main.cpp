#include <iostream>
#include <map>
#include <fstream>
#include <string>
#include <stdlib.h>
#include "NN.hpp"
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
					for(start = 0; line[start] == '\t' || line[start] == ' '; start++) {}
					
					int i;
					for(i = start; line[i] != ':'; i++) {}

					currProp = line.substr(start, i - start);

					i += 2;
					start = i;
					for(; line[i] != ' ' && line[i] != '\n' && line[i] != '\t'; i++) {}

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
			for(i = start; line[i] != ' ' && line[i] != '\n' && line[i] != '\t' && line[i] != '\''; i++) {}
			res["activationFunction"] = line.substr(start, i - start);
		}
	}
	f.close();

	return res;
}

int main()
{
	auto a = getNNInfo("../NN_config.yaml");
}
