#!/bin/bash

mkdir -p example
cd code
python3 stylotool.py --input ../datasets/tests/chiasmustest.txt --output ../example/chiasmus_results.json --config ../example_config.json
