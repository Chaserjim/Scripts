#!/bin/bash

function generate_templates {
    openstack cbis template generate \
    --platform hp-slg8_fALU \
    --destination /home/stack/templates \
    --user-config /home/stack/user_config.yaml -y
}

function run_hw_scan {
  openstack cbis hwscan \
  -u hp \
  -p password \
  -n 192.168.117.117:controller_nodes,192.168.117.118:controller_nodes,192.168.117.119:controller_nodes,192.168.117.121:compute_nodes \
  -C user_config.yaml
}

function cbis deploy_overcloud {
  openstack overcloud deploy \
  --ntp-server 135.248.16.241 \
  --templates templates/ \
  -e templates/common-environment.yaml \
  -e templates/network-environment.yaml  \
  -e templates/storage-environment.yaml  \
  --control-scale 3 \
  --compute-scale 2 \
  --compute-flavor compute \
  --control-flavor control \
  --neutron-bridge-mappings physnet0:br-physnet0 \
  --neutron-network-vlan-ranges physnet0:600:899
}

#generate_templates
#run_hw_scan
#openstack baremetal import --yaml /home/stack/hosts.yaml
#openstack baremetal configure boot
#openstack baremetal introspection bulk start
deploy_overcloud
