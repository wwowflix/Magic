# -*- coding: utf-8 -*-
import os

folders = ['inputs', 'outputs', 'scripts', 'logs']
for folder in folders:
    os.makedirs(folder, exist_ok=True)
print('? Folder structure created.')
