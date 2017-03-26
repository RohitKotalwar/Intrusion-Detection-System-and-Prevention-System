#!/usr/bin/python
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections 
from mininet.log import setLogLevel
from mininet.link import TCLink



class fatTreeTopo(Topo):

    "Fat Tree Topology"

    def __init__(self):
        "Create Fat tree Topology"

        Topo.__init__(self)

        #Add hosts
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
        h3 = self.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
        h4 = self.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
        h5 = self.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
        h6 = self.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
        h7 = self.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
        h8 = self.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)

        #Add switches
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch)
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch)
        s3 = self.addSwitch('s3', cls=OVSKernelSwitch)
        s4 = self.addSwitch('s4', cls=OVSKernelSwitch)
        s5 = self.addSwitch('s5', cls=OVSKernelSwitch)
        s6 = self.addSwitch('s6', cls=OVSKernelSwitch)
        s7 = self.addSwitch('s7', cls=OVSKernelSwitch)
        s8 = self.addSwitch('s8', cls=OVSKernelSwitch)
        s9 = self.addSwitch('s9', cls=OVSKernelSwitch)
        s10 = self.addSwitch('s10', cls=OVSKernelSwitch)

        #Add links
        self.addLink(s1, s2, bw=100)
        self.addLink(s1, s3, bw=100)
        self.addLink(s1, s4, bw=100)
        self.addLink(s2, s3, bw=100)
        self.addLink(s2, s4, bw=100)
        self.addLink(s3, s4, bw=100)
        self.addLink(s5, s1, bw=100)
        self.addLink(s5, s2, bw=100)
        self.addLink(s6, s1, bw=100)
        self.addLink(s6, s2, bw=100)
        self.addLink(s7, s3, bw=100)
        self.addLink(s7, s4, bw=100)
        self.addLink(s8, s3, bw=100)
        self.addLink(s8, s4, bw=100)
        self.addLink(s9, s2, bw=100)
        self.addLink(s9, s4, bw=100)
        self.addLink(s10, s2, bw=100)
        self.addLink(s10, s4, bw=100)
        self.addLink(s10, s9, bw=100)
        self.addLink(h1, s5, bw=100)
        self.addLink(h2, s5, bw=100)
        self.addLink(h3, s6, bw=100)
        self.addLink(h4, s6, bw=100)
        self.addLink(h5, s7, bw=100)
        self.addLink(h6, s8, bw=100)
        self.addLink(h7, s9, bw=100)
        self.addLink(h8, s10, bw=100)

topos = { 'mytopo': (lambda: fatTreeTopo() ) }

def runExperiment():
    "Create and test a simple experiment" 
    topo = fatTreeTopo( )
    net = Mininet(topo)
    net.start()
    print "Dumping host connections" 
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity" 
    net.pingAll()
    #net.stop()

def perfTest():
        "Create network and run simple performance test"
        topo = fatTreeTopo( )
        net = Mininet(topo)
        net.start()
        print "Dumping host connections"
        dumpNodeConnections(net.hosts)
        print "Testing network connectivity"
        net.pingAll()
        print "Testing bandwidth between h1 and h8"
        h1, h8 = net.get('h1', 'h8')
        net.iperf((h1, h8))
        net.stop()

if __name__ == '__main__':
# Tell mininet to print useful information 
    setLogLevel('info')
    runExperiment()
    perfTest()