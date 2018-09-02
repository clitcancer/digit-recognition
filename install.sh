set -x

cd server
go build
cd ..

cd guesser
g++ *.cpp -o main.exe
cd ..

python -m pip install pyyaml aiohttp
