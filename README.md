<p align="left">
  <a href="https://github.com/steffinstanly/Kali-Source-Updater/releases">
    <img src="https://img.shields.io/badge/Release-v1.1-blue">
  </a>
  <a href="https://pypi.org/project/kali-source-updater/">
    <img src="https://img.shields.io/badge/pypi-%40kali--source--updater-red"
         alt="pypi">
  </a>
</p>

# Kali-Source-Updater v1
Python Script to change official Kali repository based on the lowest latency, there by helping in speeding up the update and upgrades of kali packages. 

## Installation

```
pip3 install kali-source-updater
```

## For upgrading to the latest version

```
pip3 install --upgrade kali-source-updater
```

## Requirements
```
Python3, Kali Linux, pip3
```

## Usage
```
# kali-source-updater -h
usage: kali-source-updater [-h] [-v] [-https] [-src] [-u]

Kali ource updater selects the best kali mirror
server and apply the configuration

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  enable verbose output
  -u, --update   for updating the system alone completely
  -https         use HTTPS in apt transport (default HTTP)
  -src           enable sources packages (default disable)
```
