#!/bin/bash

python3 image_input_and_circuit_test.py
python3 hash_circuit_build.py 
gnome-terminal -e ./libraries/libscapi/samples/libscapi_example yao 1 Yao/Yao.Config.txt &
sleep 4
gnome-terminal -e ./libraries/libscapi/samples/libscapi_example yao 2 Yao/Yao.Config.txt
