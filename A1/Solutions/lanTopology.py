#!/usr/bin/python

"""
This example shows how to create a Mininet object and add nodes to it manually.
"""
"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

#Function definition: This is called from the main function
def firstNetwork():

    "Create an empty network and add nodes to it."
    net = Mininet()
    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1')
    h2 = net.addHost( 'h2')
    h3 = net.addHost( 'h3')
    h4 = net.addHost( 'h4')
    
    
    info( '*** Adding switch\n' )
    s14 = net.addSwitch( 's14' )
    s24 = net.addSwitch( 's24' )
    s34 = net.addSwitch( 's34' )
    
    info( '*** Creating links\n' )
    net.addLink( h1, s14 )
    net.addLink( h2, s24 )
    net.addLink( h3, s34 )
    net.addLink( h4, s14 )
    net.addLink( h4, s24 )
    net.addLink( h4, s34 )
    
    info( '*** Starting network\n')
    net.start()

    #This is used to run commands on the hosts
    info( '*** Starting terminals on hosts\n' )
    h1.cmd('xterm -xrm "XTerm.vt100.allowTitleOps: false" -T h1 &')
    h2.cmd('xterm -xrm "XTerm.vt100.allowTitleOps: false" -T h2 &')
    h3.cmd('xterm -xrm "XTerm.vt100.allowTitleOps: false" -T h3 &')
    h4.cmd('xterm -xrm "XTerm.vt100.allowTitleOps: false" -T h4 &')

    info( '*** Running the command line interface\n' )
    CLI( net )
	
    info( '*** Closing the terminals on the hosts\n' )
    h1.cmd("killall xterm")
    h2.cmd("killall xterm")
    h3.cmd("killall xterm")
    h4.cmd("killall xterm")
    
    info( '*** Stopping network' )
    net.stop()

#main Function: This is called when the Python file is run
if __name__ == '__main__':
    setLogLevel( 'info' )
    firstNetwork()
