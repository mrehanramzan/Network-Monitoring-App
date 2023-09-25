
# Network Flow Control Using Packet Header Information

Due to rapid rise in the use of internet technology, there is an increase in number of cyber attacks. This project successfully provides monitioring and blocking facilities through a simplicit GUI. 


## Features

- Monitoring the network traffic flow
- Providing fine-grained access control
- Interactive and user-friendly GUI


## Installation:

To install our fyp:

```bash
  sudo pip install nfstream
```
```bash
  sudo pip install pytest
```
### For bcc:
```bash
  sudo apt install -y bison build-essential cmake flex git libedit-dev libllvm11 llvm-11-dev libclang-11-dev python zlib1g-dev libelf-dev libfl-dev libluajit-5.1-dev 
```
### Install this version of bcc

https://github.com/iovisor/bcc/releases/tag/v0.21.0

### Directory Setup:
mkdir bcc/build;\
cd bcc/build\
cmake ..\
make\
sudo make install\
cmake -DPYTHON_CMD=python3 ..\
pushd src/python/\
make\
sudo make install\
popd 


## Authors

- [Rehan Ramzan](https://github.com/mrehanramzan/Network-Monitoring-App)

- [Muhammad Farooq](https://github.com/farooquememon385)