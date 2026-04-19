---
title: 高效bash脚本
tags:
  - Linux
abbrlink: 6a8b5c38
date: 2024-10-12 08:53:03
---
&emsp;&emsp;转学习到的高效bash脚本。
<!--less-->
# build-in commands
```bash
if [[ "$var" -eq 3 ]];then
   echo "hello"
fi
```

# minimize subshells
```bash
output=$(<input.txt)
```

# array
```bash
color=("red" "yellow" "blue")
for col in "${color[@]}";
do
   echo $col
done
```

# enable noclobber
可以防止overwrite。
```
set -o noclobber
```

# file operation
```
while IFS= read -f line
do
echo $line
done <input.txt
```

# parallel processing
```
cat urls.txt | xargs -n 1 -P 4 curl -O
```

# error handling
脚本一出错就退出来。
```
set -e
```
个性化出错信息。
```
command || { echo "command failded"; exit 1; }
``` 
trap signals 
```
trap 'echo "error occurred"; cleanup; exit1' ERR
function cleanup(){
   #clean up command
}
```
validate inputs
```
if [[ -z "$1" ]];then
   echo "Usage: $0 <argument>"
   exit 1
fi
```
logging
```
logfile="script.log"
exec > >(tee -i $logfile)
exec 2>&1

echo "script started"
```

# 系统任务

系统备份
```
set -e
trap ' echo "Backup failed"; exit 1' ERR
bk_up="/bak_dir"
ts=$(date +%Y%m%d%H%M%S)
bkup_file="${bk_up}/backup_${ts}.tar.gz"
tar czf "$bkup_file" backup_files
```
系统监测
```
threshold=80
partition="/dev/sda1"
usage=$(df -h | grep "$partition" | awk '{print $5}' | sed 's/%//')
if [[ "$usage" -gt "$threshold" ]];then
   echo "disk usage of $partition is above $threshold%"
fi
```
用户管理
```
function add_user() {
    local username=$1
    useradd "$username" && echo "User $username added successfully."
}

function remove_user() {
}
case $1 in 
    add)
       add_user "$2"
       ;;
    remove)
       remove_user "$2"
       ;;
    *)
       echo "Usage : $0 {add|remove} <username>"
       exit 1
       ;;
esac
```
自动更新
```
set -e
trap 'echo "update failed"; exit 1 ' ERR

apt-get update && apt-get upgrade -y
```
网络配置
```
function configure_network(){
     local interface=$1
     local ip_address=$$2
     local gateway=$3
     
     cat <<EOF >/etc/network/interfaces
auto $interface
iface $interface inet static
     address $ip_address
     gateway $gateway
EOF
     systemctl restart networking
     echo "network configured on $interface"
}
```
