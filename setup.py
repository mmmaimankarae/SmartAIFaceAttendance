from setuptools import setup
import os

APP=['main.py']
DATA_FILES = [
    ('Interface/modes', [
        'already.png',
        'default.png',
        'late.png',
        'mark.png',
        'notFound.png',
        'onTime.png',
        'background.png',
    ]),
    ('.', ['EncodeFace.p', 'serviceAccountKey.json']),
]
OPTIONS = {
    'argv_emulation':True
}

setup(
    app=APP,
    options={'py2app':OPTIONS},
    setup_requires=['py2app']
)