#! /bin/bash
#
# setup_fedora_addrs.sh
# My computer is named "fedora".  You may use whatever name you wish so long as
# the names are consistent between /etc/hosts,  I used "fedora"
#
#
# This script assumes that the host names and corresponding addresses have
# already been set up in /etc/hosts.
#
# Step 1: Modify your /etc/hosts file on this machine to suit.
#
# Step 2: Run this script as root.

LINK="enp2s0"
HOSTNAME="fedora"
NETMASK_4="/32"
NETMASK_6="/64"
PING_TEST="jeffs-latitudee7240"
REMOTE_PING_TEST="google.com"
# uncomment this if you have a wide terminal
ONE="-o"
alias fgrep='grep -F --color=auto'

# Assuming that that the network was configured from the WiFi with
# the default gateway going through that router, which might be on a
# different network.

# Set up the ethernet
ip link change dev $LINK
ip link list
ip -4 addr show dev $LINK
ip -4 route list
sudo ip addr change dev $LINK $( host -t a $HOSTNAME | awk '{ print $4 }' )${NETMASK_4}
ip -4 addr show dev $LINK
ip -4 route list
sudo ip addr change dev $LINK $( host -t a $HOSTNAME | awk '{ print $4 }' )${NETMASK_4}
if ping -4 -c 4 $PING_TEST; then
	echo "$PING_TEST is pingable"
else
	echo "$PING_TEST is **not pingable**  FAIL"
	host -4 $PING_TEST
	exit 1
fi
if ping -4 -c 4 $REMOTE_PING_TEST; then
	echo "$REMOTE_PING_TEST is pingable"
else
	echo "$REMOTE_PING_TEST is **NOT** pingable EPIC FAIL"
fi


 
# for demonstrating multiple names for the same IPv4 address
# ip -4 addr change dev $LINK addr ${HOSTNAME}
ADDR_A_4=$( host ${HOSTNAME}-A | fgrep "has address" | awk '{print $4}' )
ADDR_B_4=$( host ${HOSTNAME}-B | fgrep "has address" | awk '{print $4}' )
ADDR_C_4=$( host ${HOSTNAME}-C | fgrep "has address" | awk '{print $4}' )

ADDR_A_6=$( host ${HOSTNAME}-A | fgrep "IPv6" | awk '{print $5}' )
ADDR_B_6=$( host ${HOSTNAME}-B | fgrep "IPv6" | awk '{print $5}' )
ADDR_C_6=$( host ${HOSTNAME}-C | fgrep "IPv6" | awk '{print $5}' )

echo "ADDR_A_6 is $ADDR_A_6 .  ADDR_B_6 is $ADDR_B_6 ADDR_C_6 is $ADDR_C_6"

# for demonstrating multiple IPv4 addresses and multiple names
ip -4 addr add dev $LINK ${ADDR_A_4}${NETMASK_4}
ip -4 addr add dev $LINK ${ADDR_B_4}${NETMASK_4}
ip -4 addr add dev $LINK ${ADDR_C_4}${NETMASK_4}


ip -6 addr add dev $LINK ${ADDR_A_6}${NETMASK_6}
ip -6 addr add dev $LINK ${ADDR_B_6}${NETMASK_6}
ip -6 addr add dev $LINK ${ADDR_C_6}${NETMASK_6}
#
#
#
#
echo "-------------------------------"
ip -4 $ONE addr show dev $LINK
echo "-"
ip -6 $ONE addr show dev $LINK
echo "================================"
#
#
echo "Run the following commands to clean up"
echo "ip -4 $ONE addr del dev $LINK ${ADDR_A_4}${NETMASK_4}"
echo "ip -4 $ONE addr del dev $LINK ${ADDR_B_4}${NETMASK_4}"
echo "ip -4 $ONE addr del dev $LINK ${ADDR_C_4}${NETMASK_4}"
#
#

echo "ip -6 $ONE addr del dev $LINK ${ADDR_A_6}${NETMASK_6}"
echo "ip -6 $ONE addr del dev $LINK ${ADDR_B_6}${NETMASK_6}"
echo "ip -6 $ONE addr del dev $LINK ${ADDR_C_6}${NETMASK_6}"
#
#
#
echo "Show that the redundant addresses are gone"
ip -4 addr show dev $LINK
echo "IPv6"
ip -6 addr show dev $LINK

