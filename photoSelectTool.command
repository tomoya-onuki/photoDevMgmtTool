#!/bin/bash
CURRENT=$(cd $(dirname $0);pwd)
cd $CURRENT
echo $CURRENT
. venv/bin/activate
python3 photoSelectTool.py
deactivate