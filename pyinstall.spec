# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['adoberpc.pyw'],
             pathex=['C:\\Users\\Atulya\\dev\\AdobeRPC'],
             binaries=[],
             datas=[('config.txt', '.'),
                    ('favicon.ico', '.'),
                    ('favicon.png', '.'),
                    ('init.log', 'logging')],
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
          name='adoberpc',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='favicon.ico',
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='adoberpc')
