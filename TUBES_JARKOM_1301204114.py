#!/usr/bin/env python
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from mininet.log import setLogLevel
import time
import os

'''
Nama	: Albertus Ivan Martino
NIM		: 1301204114
Kelas	: IF-44-05
'''

if'__main__'==__name__:

	os.system('mn -c')
	os.system( 'clear' )
	setLogLevel( 'info' )
	net = Mininet(link=TCLink)
	
	#CLO 1
	ha = net.addHost('ha')
	hb = net.addHost('hb')
	r1 = net.addHost('r1')
	r2 = net.addHost('r2')
	r3 = net.addHost('r3')
	r4 = net.addHost('r4')

	bandwidth1={'bw':1}
	bandwidth2={'bw':0.5}

	net.addLink(ha,r1,cls=TCLink, intfName1='ha-eth0', intfName2='r1-eth0',**bandwidth1) #ha-eth0 r1-eth0 
	net.addLink(ha,r2,cls=TCLink, intfName1='ha-eth1', intfName2='r2-eth0',**bandwidth1) #ha-eth1 r2-eth0

	net.addLink(hb,r3,cls=TCLink, intfName1='hb-eth0', intfName2='r3-eth0',**bandwidth1) #hb-eth0 r3-eth0
	net.addLink(hb,r4,cls=TCLink, intfName1='hb-eth1', intfName2='r4-eth0',**bandwidth1) #hb-eth1 r4-eth0

	net.addLink(r1,r3,cls=TCLink, intfName1='r1-eth1', intfName2='r3-eth1',**bandwidth2) #r1-eth1 r3-eth1
	net.addLink(r1,r4,cls=TCLink, intfName1='r1-eth2', intfName2='r4-eth1',**bandwidth1) #r1-eth2 r4-eth1

	net.addLink(r2,r3,cls=TCLink, intfName1='r2-eth1', intfName2='r3-eth2',**bandwidth1) #r2-eth1 r3-eth2
	net.addLink(r2,r4,cls=TCLink, intfName1='r2-eth2', intfName2='r4-eth2',**bandwidth2) #r2-eth2 r4-eth2

	net.build()

	ha.cmd("ifconfig ha-eth0 0")
	ha.cmd("ifconfig ha-eth1 0")
	ha.cmd("ifconfig ha-eth0 192.168.1.1 netmask 255.255.255.0")
	ha.cmd("ifconfig ha-eth1 192.168.2.1 netmask 255.255.255.0")
		
	hb.cmd("ifconfig hb-eth0 0")
	hb.cmd("ifconfig hb-eth1 0")
	hb.cmd("ifconfig hb-eth0 192.168.3.1 netmask 255.255.255.0")
	hb.cmd("ifconfig hb-eth1 192.168.4.1 netmask 255.255.255.0")
		
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	r1.cmd("ifconfig r1-eth0 192.168.1.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.5.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.7.1 netmask 255.255.255.0")
		
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	r2.cmd("ifconfig r2-eth0 192.168.2.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.8.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.6.1 netmask 255.255.255.0")
		
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	r3.cmd("ifconfig r3-eth0 192.168.3.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.5.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.8.2 netmask 255.255.255.0")
		
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	r4.cmd("ifconfig r4-eth0 192.168.4.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.7.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.6.2 netmask 255.255.255.0")
		
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")


	#CLO 2
	ha.cmd("ip rule add from 192.168.1.1 table 1")
	ha.cmd("ip rule add from 192.168.2.1 table 2")
	ha.cmd("ip route add 192.168.1.0/24 dev ha-eth0 scope link table 1")
	ha.cmd("ip route add default via 192.168.1.2 dev ha-eth0 table 1")
	ha.cmd("ip route add 192.168.2.0/24 dev ha-eth1 scope link table 2")
	ha.cmd("ip route add default via 192.168.2.2 dev ha-eth1 table 2")
	ha.cmd("ip route add default scope global nexthop via 192.168.1.2 dev ha-eth0")
	
	hb.cmd("ip rule add from 192.168.3.1 table 1")
	hb.cmd("ip rule add from 192.168.4.1 table 2")
	hb.cmd("ip route add 192.168.3.0/24 dev hb-eth0 scope link table 1")
	hb.cmd("ip route add default via 192.168.3.2 dev hb-eth0 table 1")
	hb.cmd("ip route add 192.168.4.0/24 dev hb-eth1 scope link table 2")
	hb.cmd("ip route add default via 192.168.4.2 dev hb-eth1 table 2")
	hb.cmd("ip route add default scope global nexthop via 192.168.3.2 dev hb-eth0")

	r1.cmd("route add -net 192.168.3.0/24 gw 192.168.5.2")
	r1.cmd("route add -net 192.168.8.0/24 gw 192.168.5.2")
	r1.cmd("route add -net 192.168.4.0/24 gw 192.168.7.2")
	r1.cmd("route add -net 192.168.6.0/24 gw 192.168.7.2")
	r1.cmd("route add -net 192.168.2.0/24 gw 192.168.7.2")
	
	r2.cmd("route add -net 192.168.3.0/24 gw 192.168.8.2")
	r2.cmd("route add -net 192.168.4.0/24 gw 192.168.6.2")
	r2.cmd("route add -net 192.168.5.0/24 gw 192.168.8.2")
	r2.cmd("route add -net 192.168.7.0/24 gw 192.168.6.2")
	r2.cmd("route add -net 192.168.1.0/24 gw 192.168.8.2")
	
	r3.cmd("route add -net 192.168.1.0/24 gw 192.168.5.1")
	r3.cmd("route add -net 192.168.2.0/24 gw 192.168.8.1")
	r3.cmd("route add -net 192.168.6.0/24 gw 192.168.8.1")
	r3.cmd("route add -net 192.168.7.0/24 gw 192.168.5.1")
	r3.cmd("route add -net 192.168.4.0/24 gw 192.168.8.1")
	
	r4.cmd("route add -net 192.168.1.0/24 gw 192.168.7.1")
	r4.cmd("route add -net 192.168.2.0/24 gw 192.168.6.1")
	r4.cmd("route add -net 192.168.5.0/24 gw 192.168.7.1")
	r4.cmd("route add -net 192.168.8.0/24 gw 192.168.6.1")
	r4.cmd("route add -net 192.168.3.0/24 gw 192.168.7.1")
	
	#CLO 4
	'''
	r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 20ms")
	
	r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 40ms")
	
	r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 60ms")
	
	r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 100ms")
	'''
	
	time.sleep(2)
	hb.cmd("iperf -s &")
	time.sleep(2)
	ha.cmd("iperf -c 192.168.3.1 -t 10 &") 
	
	CLI(net)
	
	net.stop()
