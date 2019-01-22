#pcom#
Metal Sartigan package for PCOM

###Build and release###
Make sure the `setup.py` file is up to date with at least the current version.

Then, in the `src` folder:

```
rm dist/*
python3 setup.py bdist_wheel
twine upload dist/*
```

the package `pcom` can then be installed using `pip install pcom`