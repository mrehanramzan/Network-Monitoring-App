## Installation:

To install our fyp:

```bash
  sudo pip install nfstream pytest
```

to install libraries: psycopg2 and flask_mysqldb
```bash
  sudo apt install libpq-dev pkg-config libmysqlclient-dev
```
then
```bash
  pip install psycopg2 flask_mysqldb
```

then
```bash
  pip uninstall-r requirements.txt
```
then
```bash
  sudo pip install -r requirements.txt
```

### For bcc:

```bash
sudo gedit /etc/apt/sources.list
```
and add these two lines at the end of file

``` bash
deb http://deb.debian.org/debian sid main contrib non-free
deb-src http://deb.debian.org/debian sid main contrib non-free
```

```bash
# Before you begin
apt-get update
# According to https://packages.debian.org/source/sid/bpfcc,
# BCC build dependencies:
sudo apt-get install arping libdebuginfod-dev bison clang-format cmake dh-python \
  dpkg-dev pkg-kde-tools ethtool flex inetutils-ping iperf \
  libbpf-dev libclang-dev libclang-cpp-dev libedit-dev libelf-dev \
  libfl-dev libzip-dev linux-libc-dev llvm-dev libluajit-5.1-dev \
  luajit python3-netaddr python3-pyroute2 python3-setuptools python3
```


### Install this version of bcc


```bash
git clone https://github.com/iovisor/bcc/
```
### Directory Setup:
cd bcc
mkdir build; cd /build
cmake ..
<!-- check if any library not installed in output -->
make
sudo make install
cmake -DPYTHON_CMD=python3
pushd src/python/
make
sudo make install
popd 

source: https://github.com/iovisor/bcc/blob/master/INSTALL.md#debian---source 
/usr/lib/python3/dist-packages