# altdemo-provision
## Routing-on-host (ROH) demo with ALT Linux Switches and CentOS servers
Ansible playbook to configure end-to-end L3 fabric with ROH, based on Mellanox Spectrum Switches, running ALT Linux with [Bird routing daemon](http://bird.network.cz), and servers running CentOS and [Quagga routing daemon](http://www.nongnu.org/quagga/).
## Overview
This playbook automates network configuration for ROH demo setup, based on 6 Mellanox Spectrum switches with ALT Linux (with [mlxsw switchdev](https://github.com/Mellanox/mlxsw/wiki/Overview) driver) and 2 servers with CentOS.

## Network topology
ToDo

## Funtionality
ToDo

## Usage
* Install Ansible >= 2.0 on a management server
* Clone this repository
* Set your SSH usernames in `deploy_network.yml`
* Modify config in `group_vars/all` if required
* Run the play with `ansible-playbook deploy_network.yml`
