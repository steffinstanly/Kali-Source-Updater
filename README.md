# Kali-Source-Updater v1
Python Script to change official Kali repository based on the lowest latency, there by helping in speeding up the update and upgrades of kali packages. 

## Installation

```
pip3 install kali-source-updater
```

## Requirements
```
Python3, Kali Linux, pip3
```

## Usage
```
# kali-source-updater -h
usage: kali-source-updater [-h] [-v] [-https] [-src]

Kali ource updater selects the best kali mirror
server and apply the configuration

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  enable verbose output
  -https         use HTTPS in apt transport (default HTTP)
  -src           enable sources packages (default disable)
```
