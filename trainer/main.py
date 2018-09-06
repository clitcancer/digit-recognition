import yaml
import sys
import random
import aiohttp
import asyncio
import numpy as np
from math import floor

from NN import NN
import activation_functions as af


def getDigits(amount, dataset):
    digits = []
    base_url = 'http://localhost:214/api/getDigit'

    maxs = {
        'train': 60000,
        'test': 10000
    }

    async def httpJsonGet(url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=60)) as session:
            async with session.get(url, timeout=None) as response:
                digits.append(await response.json())

    fetchesPerBatch = 62
    fetched = 0
    while fetched <= amount - fetchesPerBatch:
        printProgress(fetched/amount)

        urls = [
            asyncio.ensure_future(httpJsonGet(f'{base_url}/{dataset}/{random.randint(1, maxs[dataset])}')) for x in range(fetchesPerBatch)
        ]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(urls))
        fetched += fetchesPerBatch


    printProgress(fetched/amount)
    urls = [
        asyncio.ensure_future(httpJsonGet(f'{base_url}/{dataset}/{random.randint(1, maxs[dataset])}')) for x in range(amount - fetched)
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(urls))


    return digits
            

def printProgress(progress):
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
    nn.load('../brain.json')

    print('Fetching digits data...')
    epoches = int(sys.argv[1])
    digits = {
        'train': getDigits(epoches, 'train'),
        'test': getDigits(1000, 'test')
    }
    print('Done fetching! Time for training.')

    print('Training...')
    for n, dig in enumerate(digits['train']):
        inputs = np.array(dig['pixels']).flatten() * 1.0
        inputs /= 255.0
        target = np.arange(10)*0.0
        target[int(dig['label'])] = 1.0
        nn.train(inputs, target)

        printProgress((n+1)/len(digits['train']))
    print('Done training! Time for tests.')

    nn.save('../brain.json')

    print('Testing...')
    correctAmount = 0
    for n, dig in enumerate(digits['test']):
        inputs = np.array(dig['pixels']).flatten() * 1.0
        inputs /= 255.0
        correctAmount += int(int(nn.guess(inputs)) == int(dig['label']))

        printProgress((n+1)/len(digits['test']))
    print('Done testing! {accuracy}% accuracy.'.format(accuracy=round(correctAmount/len(digits['test'])*100, 1)))
