# reNgine installation for Hackers

If you are a developer and willing to reNgine for contributing or developing new features follow the [Getting Started Guidelines](dev/getting-started) for developers.

This section aims to answer some of the most frequently asked questions on installing reNgine.

!!! danger "Attention"
    It is highly recommended that you follow each steps to avoid encountering any errors/issues during the setup.

This guide is divided into several sections based on the frequently asked questions:

- [Running reNgine on local machine](#running-rengine-on-local-machine)
- [Running reNgine on VPS](#running-rengine-on-vps)
- [Running reNgine with your own managed database](#running-rengine-with-your-own-managed-database)

## ⚡ Quick Installation

If you are on Ubuntu/VPS/Linux, install script is provided for quick installation.

Follow [⚡ Quick Installation instructions](install/quick.md).

## Running reNgine on local machine

While you can run reNgine locally, it is recommended that you run it on VPS like digitalocean.
Running reNgine on local machine is a very straight forward process. You'll neeed `docker`, `docker-compose` and `make` to build and run reNgine on local machine.

!!! info "Quick Installation for Linux Debian like Ubuntu"
    If you are using Ubuntu or Kali as your base OS and wish to run reNgine on it, you may skip the prerequisites section, installation script is provided with this project that takes care of installing docker and its dependencies. [Quick Installation](quick-install)

[Quick Install reNgine on Ubuntu or Kali](install/quick.md)

[Installing reNgine on Windows or Mac](install/detailed.md)


## Running reNgine on VPS

While the installation step should be very similar across all VPS providers, an example of running reNgine on DigitalOcean is provided.

[How to Install reNgine on DigitalOcean or any VPS](install/vps.md)


## Running reNgine with your own managed database

This is related to a [Github Issue](https://github.com/yogeshojha/rengine/issues/180)

It is a good idea to run reNgine using managed database, or remote database.

Find [how to use reNgine with managed/remote database](install/remotedb.md)
