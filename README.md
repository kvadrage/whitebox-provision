# whitebox-provision
## Routing-on-host (ROH) demo with ALT Linux Switches and CentOS servers
Ansible playbook to configure end-to-end L3 fabric with ROH, based on Mellanox Spectrum Switches, running ALT Linux with [Bird routing daemon](http://bird.network.cz), and servers running CentOS.
## Overview
This playbook automates network configuration for ROH demo setup, based on 6 Mellanox Spectrum switches with ALT Linux (with [mlxsw switchdev](https://github.com/Mellanox/mlxsw/wiki/Overview) driver) and 2 servers with CentOS.

## Network topology
```
      | |                                                   | |
      | |                                                   | |
    +-5-6---------+   +-------------+   +-------------+   +-5-6---------+
    |   spine01   |   |   spine02   |   |   spine03   |   |   spine04   |
    +-1-2-3-4-----+   +-1-2-3-4-----+   +-1-2-3-4-----+   +-1-2-3-4-----+
      |                 |                 |                 |
      | +---------------+                 |                 |
      | | +-------------------------------+                 |
      | | | +-----------------------------------------------+
      | | | |           | | | |           | | | |            | | | |
      | | | |           | | | |           | | | |            | | | |
    +-1-2-3-4-----+   +-1-2-3-4-----+   +-1-2-3-4-----+   +--1-2-3-4----+
    |   leaf01    |   |   leaf02    |   |   leaf03    |   |   leaf04    |
    +-5s0--5s1----+   +-5s+--5s1----+   +-5s0--5s1----+   +--5s0--5s1---+
      |    |            |    |            |    |            |    |
      |    |            |    |            |    |            |    |
      |    | +--------+ |    |            |    | +--------+ |    |
      |    11|server01|12    |            |    11|server02|12    |
      |      +--------+      |            |      +--------+      |
      |                      |            |                      |
      |      +--------+      |            |      +--------+      |
      +----11|server03|12----+            +----11|server04|12----+
             +--------+                          +--------+

```

## Funtionality
* L3 routing (IPv4/IPv6)
* BGP/OSPF/BFD (Bird)
* VRF support

## Usage
* Install Ansible >= 2.0 on a management server
* Clone this repository
* Set your SSH usernames in `deploy_network.yml`
* Modify config in `group_vars/all` if required
* (Optional) Generate Ansible vars from template `ansible-playbook generate_vars_all.yml`
* Run the play with `ansible-playbook deploy_network.yml`
