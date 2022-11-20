wg genkey | tee /etc/wireguard/{title_private_key} | wg pubkey | tee /etc/wireguard/{title_pub_key}
Restart service: wg-quick@wg0.service
Status service: systemctl restart wg-quick@wg0.sevice

Run service as user: systemctl --user {X} start {service}

Dump network (logs)
tcpdump -tni any 'udp port 51830' >> /var/log/wireguard/wireguard.log

Add new user
- add peer.template in wg0.conf
- generate private and public key user:  

WINDOWS
- Скопировать по ssh файл конфиг: wg0.conf находящийся в папке пользователя
- Через Планировщик заданий указать
  - Сценарий: PATH to wireguard.exe
  - Триггер: запуск компьютера
  - Аргументы: /installtunnelservice "PATH to wg0.conf"

LINUX
- apt install resolvconf
- apt install wireguard
- Execute: ./create-user login 
- Скопировать по ssh файл конфиг: wg0.conf находящийся в папке пользователя в папку: /etc/wireguard/wg0.conf
- wg-quick up wg0
- wg

Enable with start boot: 
- systemctl enable wg-quick@wg0
Disable with start boot: systemctl
- systemctl disable wg-quick@wg0 
