import asyncio
import builtins
import json
from math import floor
import random
import sys

import aiohttp
import numpy as np
import yaml

import activation_functions as af
from NN import NN


def print(*args, **kwargs):
    if '--verbose' in sys.argv:
        builtins.print(*args, **kwargs)


def get_digits(amount, dataset):
    digits = []
    base_url = 'http://localhost:214/api/getDigit'

    maxs = {
        'train': 60000,
        'test': 10000
    }

    async def http_json_get(url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=60)) as session:
            async with session.get(url, timeout=None) as response:
                digits.append(await response.json())

    fetches_per_batch = 62
    fetched = 0
    while fetched <= amount - fetches_per_batch:
        print_progress(fetched/amount)

        urls = [
            asyncio.ensure_future(http_json_get(f'{base_url}/{dataset}/{random.randint(0, maxs[dataset]-1)}')) for x in range(fetches_per_batch)
        ]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(urls))
        fetched += fetches_per_batch

    print_progress(fetched/amount)
    urls = [
        asyncio.ensure_future(http_json_get(f'{base_url}/{dataset}/{random.randint(0, maxs[dataset]-1)}')) for x in range(amount - fetched)
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(urls))

    return digits


def print_progress(progress):
    print(' [' + '█'*(floor(progress*10)) + ' '*(floor(10 - progress*10)) + ']',
          str(round(progress*100, 1)) + '%', end='\r')


if __name__ == '__main__':
    with open('../NN_config.yaml') as f:
        NN_config = yaml.load(f)

    nn = NN(
        inputsLength=NN_config['lengths']['inputs'],
        outputsLength=NN_config['lengths']['outputs'],
        hiddenLayersLength=NN_config['lengths']['hiddenLayers'],
        thicknessLength=NN_config['lengths']['neuronsPerHiddenLayer'],
        activation=getattr(af, NN_config['activationFunction']),
        learningRate=NN_config['learningRate']
    )
    if not '--reset' in sys.argv:
        nn.load('../brain.json')

    print('Fetching digits data...')
    epoches = int(sys.argv[1])
    digits = {
        'train': get_digits(epoches, 'train'),
        'test': get_digits(1000, 'test')
    }
    print('Done fetching! Time for training.')

    print('Training...')
    losses = np.array([], dtype='float64')
    for n, dig in enumerate(digits['train']):
        inputs = np.array(dig['pixels']).flatten() * 1.0
        inputs /= 255.0
        target = np.arange(10)*0.0
        target[int(dig['label'])] = 1.0
        losses = np.append(losses, nn.train(inputs, target))

        print_progress((n+1)/len(digits['train']))
    print('Done training! Time for tests.')

    nn.save('../brain.json')

    print('Testing...')
    correct_amount = 0
    for n, dig in enumerate(digits['test']):
        inputs = np.array(dig['pixels']).flatten() * 1.0
        inputs /= 255.0
        correct_amount += int(int(nn.guess(inputs)) == int(dig['label']))

        print_progress((n+1)/len(digits['test']))
    accuracy = correct_amount/len(digits['test'])
    print('Done testing! {accuracy}% accuracy.'.format(
        accuracy=round(accuracy*100, 1)))

    if '--stats' in sys.argv:
        builtins.print(json.dumps({
            'accuracy': accuracy,
            'avrgLoss': np.average(losses),
            'activationFunc': NN_config['activationFunction'],
            'epoches': epoches,
            'learningRate': NN_config['learningRate']
        }))
