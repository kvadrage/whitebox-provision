import sys
import struct
import socket
import subprocess

IP_ADDR_ADD = "ip addr add dev {} {}/32"
IP_ADDR_DEL = "ip addr del dev {} {}/32"

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

def execute_command(command, print_error=True):
    try:
        out = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except (OSError, subprocess.CalledProcessError) as e:
        if print_error: print('Error: {}'.format(e))
        return None
    out_text = out.decode('utf-8')
    return out_text

def gen_ip_addrs(start_ip, n):
    start = ip2int(start_ip)
    return [int2ip(i) for i in range(start, start+n)]

def add_ip_addrs(iface, addrs):
    for addr in addrs:
        execute_command(IP_ADDR_ADD.format(iface, addr))

def del_ip_addrs(iface, addrs):
    for addr in addrs:
        execute_command(IP_ADDR_DEL.format(iface, addr))

def run_add_action(args):
    addrs = gen_ip_addrs(args.i, args.n)
    add_ip_addrs(args.iface=)

def parse_args():
    parser = argparse.ArgumentParser(prog='ipgen', description='generate multiple ip addresses',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser('add', help='add ip seq to an interface')
    parser_rename.add_argument('-i', dest='IFACE', type=str, help='interface')
    parser_rename.add_argument('-s', dest='START_IP', type=str, help='start ip address (/32 mask)')
    parser_rename.add_argument('-n', dest='NUMBER', type=int, help='total number of IP addresses to generate')
    parser_del = subparsers.add_parser('add', help='del ip seq from an interface')
    parser_del.add_argument('-i', dest='IFACE', type=str, help='interface')
    parser_del.add_argument('-s', dest='START_IP', type=str, help='start ip address (/32 mask)')
    parser_del.add_argument('-n', dest='NUMBER', type=int, help='total number of IP addresses to generate')
    parser_add.set_defaults(func=run_add_action)
    parser_del.set_defaults(func=run_del_action)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    args.func(args)
