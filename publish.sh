#!/bin/bash
rm -rf ./dist/*
python3 setup.py sdist bdist_wheel
twine upload --config-file ./.pypirc ./dist/*
