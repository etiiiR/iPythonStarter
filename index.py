
#%% [markdown]
# H1 Title

#%% Start Metascripts
import os
!python -m pip install jupytext

file1 = os.path.basename(__file__)  # Replace with the path to your first file
file2 = os.path.basename(__file__)[0] + '.ipynb'  # Replace with the path to your second file

if os.path.getmtime(file1) > os.path.getmtime(file2):
    print(f"{file1} is newer than {file2}")
elif os.path.getmtime(file1) < os.path.getmtime(file2):
    print(f"{file2} is newer than {file1}")
else:
    print(f"{file1} and {file2} have the same modification time")

command = f'python -m jupytext --to notebook {os.path.basename(__file__)}'
turnout = f'!python -m jupytext --to notebook {os.path.basename(__file__)}'


#%% Importing Code
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn as nnimport os
import torch.nn as nnimport subprocess



