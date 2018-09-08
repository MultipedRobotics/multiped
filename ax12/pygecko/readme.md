# pygecko

This uses [`pygecko`](https://github.com/MomsFriendlyRobotCompany/pygecko)

## Install

```bash
pip3 install -U pygecko
pip3 install -U Adafruit_GPIO
pip3 install -U pyservo
```

## Usage

Running `geckolaunch.py` with a launch file, allows you to quickly setup a
complex web of nodes with one command. Your launch file can be `.yml` or `.json`.

Remember, you still need to run `geckocore.py` so the published messages reach
the subscribers!

```bash
./run.sh
```
