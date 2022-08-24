# PM1970-Xarray

[![Build Status](https://github.com/willirath/pm1970_xarray/workflows/Tests/badge.svg)](https://github.com/willirath/pm1970_xarray/actions)
[![codecov](https://codecov.io/gh/willirath/pm1970_xarray/branch/main/graph/badge.svg)](https://codecov.io/gh/willirath/pm1970_xarray)
[![License:MIT](https://img.shields.io/badge/License-MIT-lightgray.svg?style=flt-square)](https://opensource.org/licenses/MIT)
[![Docker Image Version (latest by date)](https://img.shields.io/docker/v/willirath/pm1970_xarray?label=DockerHub)](https://hub.docker.com/r/willirath/pm1970_xarray/tags)


Xarray compatible implementation of the Pollard and Millard (1970) slab-ocean model.

_See [notebooks/Tutorial.ipynb](notebooks/Tutorial.ipynb) for details._


## Development

For now, we're developing in the Pangeo notebook containter. More details: https://github.com/pangeo-data/pangeo-docker-images

To start a JupyterLab within this container, run
```shell
$ docker pull pangeo/pangeo-notebook:2022.07.27
$ docker run -p 8888:8888 --rm -it -v $PWD:/work -w /work pangeo/pangeo-notebook:2022.07.27 jupyter lab --ip=0.0.0.0
```
and open the URL starting on `http://127.0.0.1...`.

Then, open a Terminal within JupyterLab and run
```shell
$ python -m pip install -e .
```
to have a local editable installation of the package.

## Container Image

There's a container image: https://hub.docker.com/r/willirath/pm1970_xarray

--------

<p><small>Project based on the <a target="_blank" href="https://github.com/jbusecke/cookiecutter-science-project">cookiecutter science project template</a>.</small></p>
