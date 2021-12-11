#!/bin/bash
for i in {1..300}
do
(python3 Agent.py || echo "Crash") >> batchrun.txt
done
