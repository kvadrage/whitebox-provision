#!/bin/bash

if [ $# -eq 0 ]
then
  echo "Usage: $0 iface"
  exit -1
fi

if [ $# -gt 1 ]
then
  let ref=$2
else
  let ref=100
fi

echo "Generating 256 vlan interfaces for $1 (3rd octet = $ref+)"
for i in `seq 2 4 256`;
do
    let j=i+0-1
    let sub=ref+1
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.$sub.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+256-1
    let sub=ref+2
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.$sub.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+512-1
    let sub=ref+3
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.$sub.$i/30 dev $1.$j
done

for i in `seq 2 4 256`;
do
    let j=i+768-1
    let sub=ref+4
    ip link add link $1 name $1.$j type vlan id $j
    ip link set dev $1.$j up
    ip addr add 10.252.$sub.$i/30 dev $1.$j
done
