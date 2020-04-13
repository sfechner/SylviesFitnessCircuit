# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['SFCircuit.py'],
             pathex=['/Users/Fechner/Dropbox/HealthDataAnalysis/SylviesFitnessCircuit'],
             binaries=[],
             datas=[('Sounds', 'Sounds')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SFCircuit',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='LogoSFC/Icon.icns')
app = BUNDLE(exe,
             name='SFCircuit.app',
             icon='LogoSFC/Icon.icns',
             bundle_identifier=None)
