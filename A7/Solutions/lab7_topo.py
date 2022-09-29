"""
Topology Class
"""

# Modules needed to get the absolute path to this file for quagga configuration
import inspect
import os

# You can show useful information during script execution
from mininet.log import info

# Class in mininext which includes PID namespaces, log and run isolation. 
from mininext.topo import Topo

# Class in mininext to setup the quagga service on router nodes
from mininext.services.quagga import QuaggaService

# A container in python
from collections import namedtuple

# Variable initialization
NetworkHosts = namedtuple("NetworkHosts", "name IP DG")
net = None


class LabTopo(Topo):

    "Creates Lab Topology"

    def __init__(self):
        """Initialize a Quagga topology with 2 hosts, 5 routers, 7 switches, quagga service, in a topology"""
        Topo.__init__(self)
        
        info( '*** Creating Quagga Routers\n' )
        # Absolute path to this python script
        selfPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        # Initialize the Quagga Service
        # autoStart=True (default) --> starts automatically quagga on the host
        # autoStop=True (default) --> stops automatically quagga (we don't want this)
        quaggaSvc = QuaggaService(autoStart=False, autoStop=False) 

        # Configuration file path for quagga routers
        # We require a "config" folder in the same path of the lab7_topo file, and within
        # the config folder, we require one folder for each host, named as the host itself.
        # with the corresponding daemons, zebra.conf, ripd.conf and ripngd.conf files
        quaggaBaseConfigPath = selfPath + '/configs/'

        # Initializing local variables
        netHosts = []
        NodeList = []
        
        # List of all hosts in the network.
        # Note that each node requires at least one IP address to avoid
        # Mininet's automatic IP address assignment
        netHosts.append(NetworkHosts(name='h1', IP='10.10.11.10/24', DG='via 10.10.11.1'))
        netHosts.append(NetworkHosts(name='h2', IP='10.10.12.20/24', DG='via 10.10.12.2'))
        netHosts.append(NetworkHosts(name='r1', IP='10.10.11.1/24', DG=''))
        netHosts.append(NetworkHosts(name='r2', IP='10.10.12.2/24', DG=''))
        netHosts.append(NetworkHosts(name='r3', IP='10.10.23.3/24', DG=''))
        netHosts.append(NetworkHosts(name='r4', IP='10.10.14.4/24', DG=''))
        netHosts.append(NetworkHosts(name='r5', IP='10.10.25.5/24', DG=''))
	
        for host in netHosts:
	        # We create a list of node names
	        NodeList.append(host.name)
	        if host.name in ['h1','h2']: 
	            # We configure PCs with default gateway and without quagga service
	    	    AddPCHost = self.addHost(name=host.name, ip=host.IP, defaultRoute=host.DG, hostname=host.name,  privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
	    	else :
	    	    # We configure routers with quagga service without default gateway
	    	    AddQuaggaHost = self.addHost(name=host.name, ip=host.IP, hostname=host.name,  privateLogDir=True, privateRunDir=True, inMountNamespace=True, inPIDNamespace=True, inUTSNamespace=True)
	    	    # We setup Quagga service and path to config files
	    	    # Note that we require one folder for each host, named as the host itself
	    	    quaggaSvcConfig = {'quaggaConfigPath': quaggaBaseConfigPath + host.name}
	    	    self.addNodeService(node=host.name, service=quaggaSvc, nodeConfig=quaggaSvcConfig)
	    	   	
        # Adding switches to the network
        SW1 = self.addSwitch('SW1', protocols='OpenFlow13')
        SW2 = self.addSwitch('SW2', protocols='OpenFlow13')
        SW3 = self.addSwitch('SW3', protocols='OpenFlow13')
        SW4 = self.addSwitch('SW4', protocols='OpenFlow13')
        SW5 = self.addSwitch('SW5', protocols='OpenFlow13')
        SW6 = self.addSwitch('SW6', protocols='OpenFlow13')
        SW7 = self.addSwitch('SW7', protocols='OpenFlow13')
        # We add links between switches and routers 
        info( '*** Creating links\n' )
        self.addLink( SW1, NodeList[0], intfName2='h1-eth1'  )
        self.addLink( SW1, NodeList[2], intfName2='r1-eth3'  )
        self.addLink( SW2, NodeList[1], intfName2='h2-eth1'  )
    	self.addLink( SW2, NodeList[2], intfName2='r1-eth1'  )
    	self.addLink( SW2, NodeList[3], intfName2='r2-eth1'  )
    	self.addLink( SW3, NodeList[3], intfName2='r2-eth2'  )
    	self.addLink( SW3, NodeList[4], intfName2='r3-eth1'  )
    	self.addLink( SW4, NodeList[2], intfName2='r1-eth2'  )
    	self.addLink( SW4, NodeList[5], intfName2='r4-eth1'  )
    	self.addLink( SW5, NodeList[3], intfName2='r2-eth3'  )
    	self.addLink( SW5, NodeList[6], intfName2='r5-eth1'  )
    	self.addLink( SW7, NodeList[4], intfName2='r3-eth2'  )
    	self.addLink( SW7, NodeList[6], intfName2='r5-eth2'  )
    	self.addLink( SW6, NodeList[5], intfName2='r4-eth2'  )
    	self.addLink( SW6, NodeList[6], intfName2='r5-eth3'  )
