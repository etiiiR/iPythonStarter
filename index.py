# %%

# %% [markdown]
# H1 Title

# %% Start Metascripts
import os
import subprocess
# !python -m pip install jupytext

if (".py" in os.path.basename(__file__)):
    file1 = os.path.basename(__file__)  # Replace with the path to your first file
    file2 = os.path.basename(__file__)[:-3] + '.ipynb'  # Replace with the path to your second file
else:
    file2 = os.path.basename(__file__)[:-5]  # Replace with the path to your first file
    file1 = os.path.basename(__file__) + '.py'  # Replace with the path to your second file

ipynb = False
try:
    if os.path.getmtime(file1) > os.path.getmtime(file2):
        print(f"{file1} is newer than {file2}")
    elif os.path.getmtime(file1) < os.path.getmtime(file2):
        print(f"{file2} is newer than {file1}")
        ipynb = True
    else:
        print(f"{file1} and {file2} have the same modification time")
except:
    pass     

if (ipynb):
    command =  f'python -m jupytext --to py:percent {file2}'
else:   
    command = f'python -m jupytext --to notebook {os.path.basename(__file__)}'
subprocess.run(command, shell=True)



# %% Importing Code
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn as nnimport os
import torch.nn as nnimport subprocess



