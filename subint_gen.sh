#!/bin/bash

if [ $# -eq 0 ]
then
  echo "Usage: $0 iface"
  exit -1
fi

echo "Generating 512 vlan interfaces for $1"
for i in `seq 2 4 256`;
do
    let j=i+0-1
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.101.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+256-1
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.102.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+512-1
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.103.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+768-1
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.104.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+1024-1
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.105.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+1280-1
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.106.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+1536-1
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.107.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+1792-1
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.108.$i/30 dev $1.$j
done
