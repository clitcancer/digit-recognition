import itertools
import yaml
import sys
import random
import aiohttp
import asyncio
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
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                digits.append(await response.json())

    urls = [
        asyncio.ensure_future(httpJsonGet(f'{base_url}/{dataset}/{random.randint(1, maxs[dataset])}')) for x in range(amount)
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(urls))

    return digits
            


def from2dto1d(arr):
    return list(itertools.chain(*arr))


def normalize(inputs, to):
    return list(map(lambda x: x/to, inputs))


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
        activation=getattr(af, NN_config['activationFunction'])
    )
    nn.load('../brain.json')

    print('Fetching digits data...')
    nDigits = int(sys.argv[1])
    digits = {
        'train': getDigits(nDigits, 'train'),
        'test': getDigits(10, 'test')
    }
    print('Done fetching! Time for training.')

    print('Training...')
    for n, dig in enumerate(digits['train']):
        inputs = from2dto1d(dig['pixels'])
        inputs = normalize(inputs, 255)
        nn.guess(inputs)

        printProgress((n+1)/len(digits['train']))
    print('Done training! Time for tests.')

    print('Testing...')
    correctAmount = 0
    for n, dig in enumerate(digits['test']):
        inputs = from2dto1d(dig['pixels'])
        inputs = normalize(inputs, 255)
        correctAmount += int(int(nn.guess(inputs)) == int(dig['label']))

        printProgress((n+1)/len(digits['test']))
    print('Done testing! {accuracy}% accuracy.'.format(accuracy=round(correctAmount/len(digits['test'])*100, 1)))
