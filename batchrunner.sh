#!/bin/bash
for i in {1..300}
do
(python3 Agent.py) >> $1
done
