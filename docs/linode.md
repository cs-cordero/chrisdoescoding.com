# Linode Instructions/Notes

```
$ ssh root@<ip_address>
@remote # sudo apt update
@remote # sudo apt upgrade
@remote # echo "name-of-hostname" > /etc/hostname
@remote # hostname -F /etc/hostname
@remote # vi /etc/hosts
>>  add <ip_address> <uri> <hostname> to this file
@remote # dpkg-reconfigure tzdata
@remote # adduser <username>
@remote # adduser <username> sudo  # adds the user to the `sudo` group
@remote # exit
$ ssh <username>@<ip_address>
@remote $ mkdir -p ~/.ssh && sudo chmod 700 ~/.ssh
@remote $ exit
$ scp ~/.ssh/id_rsa.pub <username>@<ip_address>:~/.ssh/authorized_keys
$ ssh <username>@<ip_address>  # it should NOT prompt for a password
@remote $ vi /etc/ssh/sshd_config
>>  PermitRootLogin no
$ sudo service ssh restart

```

### Deployment
1. Run `deploy.sh`, passing the SCP destination using <user>@<ipaddress>
1. Run `build.sh`, passing in the SCP'd file from ~/mounting_point
1. Start the pipenv environment and source start_prod

### Other Notes:
```
>> Change a Password
# passwd <user>    # (as root) changes password for user
# passwd           # (as root) changes password for current user

>> Transfer a File
@localcomputer $ scp <file_to_transfer> <username>@<ip_address>:</path/to/destination>

>> See every process that is listening on a port
@remote $ sudo netstat -tulpn

>> View Current IP Tables Rules
$ sudo iptables -L -nv

>> Setup IP Tables
>> Copy the iptables rules to /tmp/v4
$ sudo iptables-restore < /tmp/v4
```
