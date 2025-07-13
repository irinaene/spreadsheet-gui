# spreadsheet-gui

A simple Python GUI to select certain lines from `csv` files found inside the folder `input_dir`.
Can also change the value of certain fields.
The selected data can be exported to an output `csv` file.

## Installation

The simplest way to get started with this project is to use the `pixi` package manager.
Follow the instructions provided [here](https://pixi.sh/dev/installation/) to install `pixi` on your platform.
(Optionally, one can also use `pixi` to install `git`, if needed, via `pixi global install --expose git git`.)

```bash
# clone the git repo
git clone https://github.com/irinaene/spreadsheet-gui.git
# move to the repo dir
cd spreadsheet-gui
# install the pixi environment
pixi install
# "activate" the environment
pixi shell
```

## Usage

Assuming the `csv` files live inside `input_dir`, the GUI can be started with
```bash
python gui.py input_dir
```
