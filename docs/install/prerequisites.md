# Prerequisites for reNgine

This document aims to provide detailed instructions on setting up and running the **reNgine**.


!!! info "Attention"
    If you wish to run reNgine on any debian Linux (like Ubuntu), there is a installation script that will ease your docker installation and does required setup for you. Consider using it. [Quick Installation](#quick-installation) You can skip prerequisites **if you are running Ubuntu**

This document is firther divided into 3 parts:

1. [Prerequisites](#prerequisites)

2. [Quick Installation](#quick-installation)

2. [reNgine Installation](#rengine-installation)


## Prerequisites

**reNgine** uses several scripts and tools, those tools or scripts rely on various tools to be installed like Go, Python, etc, and to avoid any dependency issues, we decided to use Docker. Using Docker will not only ease the dependency issues but will also ease the installation steps. As a penetration tester, you need not focus on solving the dependencies, installing required tools, etc. With few installation steps, you should be good to run **reNgine**.

**reNgine** requires 3 tools to be installed before you begin installing rengine. They are, docker, docker-compose and make utility.

### Docker
Docker provides very good documentation on how to install docker based on your Operating System. You can [follow the documentation here.](https://docs.docker.com/get-docker/)

#### Docker installation on Ubuntu/Linux Distributions

!!! warning
    The installation steps have been directly taken from [Docker Guide](https://docs.docker.com/engine/install/ubuntu/) with no modification.

* Update the `apt` package index and install the below packages

```
sudo apt-get update
```

```
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

* Add Docker official GPG key

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

* Use the following commands to setup the stable repository

```
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

* Finally install Docker Engine

```
sudo apt-get update && sudo apt-get install docker-ce docker-ce-cli containerd.io
```

* Test the Docker by running `docker` command on your console/terminal.

#### Docker installation on Windows

Docker requires [Docker Desktop](https://docs.docker.com/docker-for-windows/install/) to be installed on your Windows OS. Installing Docker Desktop is as easy as double clicking the `InstallDocker.msi` installer, [downloaded from here](https://hub.docker.com/editions/community/docker-ce-desktop-windows/).

#### Docker installation on Mac OS

Docker requires [Docker Desktop](https://docs.docker.com/docker-for-mac/install/) to be installed on your Mac OS. Follow the instruction from Docker hub to [install Docker on Mac OS](https://hub.docker.com/editions/community/docker-ce-desktop-mac/).

#### Docker installation on Windows WSL

Nick Janetakis has a well written blog and a Video guide on [how to install Docker on Windows Subsystem Linux](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more). Please follow the video/blog guide on how to install Docker on WSL.

### Docker Compose

If you're running **Docker Desktop** you can skip installing `docker-compose` as `docker-compose` comes along with Docker Desktop. This applies for both Windows and Mac OS users.

If you're using Linux distributions or WSL, you will still need to install `docker-compose` and the [installation steps](https://docs.docker.com/compose/install) are similar.

#### Installing `docker-compose` on Linux systems

* Download the latest stable version of `docker-compose`

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

* Apply executable permission

```
sudo chmod +x /usr/local/bin/docker-compose
```

* Create a symbolic link

```
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

* Verify your installation by running

```
docker-compose --version
```

!!! info
    If `curl` is not working for some reason, there are [alternate installation steps](https://docs.docker.com/compose/install/#alternative-install-options) as well. You can use `pip` or install as a container. Follow the [alternate installation steps](https://docs.docker.com/compose/install/#alternative-install-options).

### make

#### make installation on Linux Distributions

Install the latest version of make using

```
sudo apt install make
```

Although it is optional, `build-essential` package can also be installed which contains `make` utility.

```
sudo apt install build-essential
```


All prerequisites has now been satisfied and you can either continue with [Quick Installation](quick-install.md) or [Detailed Installation Instructions.](install.md)
