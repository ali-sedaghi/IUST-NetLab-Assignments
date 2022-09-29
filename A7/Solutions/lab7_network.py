#!/usr/bin/python

"""
This script creates the network environment for our Lab:
- 5 routers, 7 switches and 2 hosts
- Quagga service enabled in all routers
- IPv4 addressing given via zebra
- XTerm window launched for all devices.
"""
# Needed to patch Mininet's isShellBuiltin module
import sys

# Run commands when you exit the python script
import atexit

# patch isShellBuiltin (suggested by MiniNExT's authors)
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

# Loads the default controller for the switches
# We load the OVSSwitch to use openflow v1.3
from mininet.node import Controller, OVSSwitch

# Needed to set logging level and show useful information during script execution.
from mininet.log import setLogLevel, info

# To launch xterm for each node
from mininet.term import makeTerms

# Provides the mininext> prompt
from mininext.cli import CLI

# Primary constructor for the virtual environment.
from mininext.net import MiniNExT

# We import the topology class for our Lab
from lab7_topo import LabTopo

# Variable initialization
net = None
hosts = None


def run():
    " Creates the virtual environment, by starting the network and configuring debug information "
    info('** Creating an instance of Lab7 network topology\n')
    topo = LabTopo()

    info('** Starting the network\n')
    global net
    global hosts
    # We use mininext constructor with the instance of the network, the default controller and the openvswitch
    net = MiniNExT(topo, controller=Controller, switch=OVSSwitch)
    net.start()
    
    info('** Executing custom commands\n')
    ##############################################
    # Space to add any customize command before prompting command line
    
    # We gather only the hosts created in the topology (no switches nor controller)
    hosts = [ net.getNodeByName( h ) for h in topo.hosts() ]

    info('** Enabling xterm for all hosts\n')
    makeTerms( hosts, 'node' )
 

    ##############################################    
	# Enable the mininext> prompt 
    info('** Running CLI\n')
    CLI(net)

# Cleanup function to be called when you quit the script
def stopNetwork():
    "stops the network, cleans logs"

    if net is not None:
        info('** Tearing down Quagga network\n')
        # For sanity, when leaving the python script, we clean the logs again
        info('** Deleting logs and closing terminals for hosts\n')
        for host in hosts:
            if host.name in ['h1','h2']:
                pass
            else :
                host.cmd( "sh configs/%s/clean.sh" ) % host.name
        
        # This command stops the simulation
        net.stop()

if __name__ == '__main__':
    # Execute the cleanup function
    atexit.register(stopNetwork)
    # Set the log level on terminal
    setLogLevel('info')
    
    # Execute the script
    run()
