#!/usr/bin/bash

/usr/bin/time -f "Time: %e seconds, CPU: %P, Memory: %MkB" $@ | ./draw.py
