import os
import torch
import torchvision

base_path = os.path.abspath(os.path.dirname(__file__)).replace("\\", '\\\\')
torch_path = os.path.dirname(torch.__file__).replace("\\", '\\\\')
torchvision_path = os.path.dirname(torchvision.__file__).replace("\\", '\\\\')
models_path = os.path.join(base_path, 'models').replace("\\", '\\\\')
arch_path = os.path.join(base_path, 'arch').replace("\\", '\\\\')
face_alignment_path = os.path.join(base_path, 'face_alignment').replace("\\", '\\\\')
lib_path = os.path.join(base_path, 'lib').replace("\\", '\\\\')
icons_path = os.path.join(base_path, 'icons', '*.jpg').replace("\\", '\\\\')
uis_path = os.path.join(base_path, 'uis', '*.ui').replace("\\", '\\\\')
metrics_path = os.path.join(base_path, 'Metrics', '*.jpg').replace("\\", '\\\\')

spec = f"""
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
a = Analysis(['Home.py'],
             pathex=['{base_path}'],
             binaries=[],
             datas=[
                ('{icons_path}', 'icons'),
                ('{uis_path}', 'uis'),
                ('{metrics_path}', 'Metrics'),
                ('{models_path}', 'models'),
                ('{arch_path}', 'arch'),   
                ('{face_alignment_path}', 'face_alignment'),  
                ('{lib_path}', 'lib'),                
                ('{torch_path}', 'torch'),
                ('{torchvision_path}', 'torchvision')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
"""
with open("main.spec", "w") as file:
    file.write(spec)