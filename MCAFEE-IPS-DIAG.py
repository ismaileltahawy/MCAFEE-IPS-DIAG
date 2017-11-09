#!/usr/bin/python

import time
import pexpect
import getpass
import ipaddress

hostname=input('Enter IPS hostname: ')
password = getpass.getpass('Enter the admin password: ')
ssh_newkey = 'Are you sure you want to continue connecting'

print("Script is SSHing to the IPS...")
p=pexpect.spawn('ssh admin@{}'.format(hostname))
#p.logfile = open("/root/python/ssh_log", "w")

def split_decode_lines():
	for line in p.after.splitlines():
		line = line.decode('utf-8')
		print(line)

def print_menu():
    print('What would you like to do: ')
    print('Press 1 to view the Power Supply status')
    print('Press 2 to view the Copper SFP Serial Numbers')
    print('Press 3 to view the Pluggable-module attached to IPS')
    print('Press 4 to run Full Diagnostics report')
    print('Press 5 to Exit')


i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==0:
    print("New SSH key !.. Script will send \"Yes\" ")
    p.sendline('yes\r')
    i=p.expect([ssh_newkey,'password:',pexpect.EOF])

if i==1:
    print(" Script is providing admin password to the IPS...")
    p.sendline('{}\r'.format(password))
    p.expect('.*>')
    print("Script is providing root password to the IPS...")
    p.sendline ('private\r')
    p.expect('.*:')
    p.sendline ('ROOTPWD\r')
    p.expect('.*>')
    
    while True:
        print_menu()
        choice = int(input('Enter a number: '))
        if choice == 1:
            print(" -----===== Power Supply status =====----- ")
            p.sendline ('show powersupply\r')
            p.expect('.*>')
            split_decode_lines()
            
        elif choice == 2:
            print(" -----===== Copper SFP Serial Numbers =====----- ")
            p.sendline ('show coppersfpserialnumbers\r')
            p.expect('.*>')
            split_decode_lines()
        
        elif choice == 3:
            print(" -----=====  Pluggable-module attached to IPS =====----- ")
            p.sendline ('show pluggable-module all\r')
            p.expect('.*>')
            split_decode_lines()
            
        elif choice == 4:
            print(" -----===== Full Diagnostics report =====-----")
            p.sendline ('diagnostics\r')
            p.expect('.*#')
            p.sendline ('run diag_show_system_info\r')
            p.expect('.*diagnostics#')
            split_decode_lines()
            
        elif choice == 5:
            print(" -----===== Bye Bye =====----- ")
            break


elif i==2:
    print("Wrong IPS Hostname or Connection Timeout")
    pass

'''
to add in the next version:
- show pluggable-module all
- show coppersfpserialnumbers
- 
'''
'''print(p.before)
print(p.after)
'''
