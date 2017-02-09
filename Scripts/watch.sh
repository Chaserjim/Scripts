#!/bin/bash
watch -n5 'nova list && ironic node-list && heat stack-list && heat resource-list -n5 overcloud | grep -iv complete'
