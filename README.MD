Cоздание ключа для сервера
```bash
wg genkey | tee /etc/wireguard/{title_private_key} | wg pubkey | tee /etc/wireguard/{title_pub_key}
```

Restart service: 
```bash
wg-quick@wg0.service
```
Status service: 
```bash
systemctl restart wg-quick@wg0.sevice
```

Run service as user: 
```bash
systemctl --user {X} start {service}
```

Dump network (logs)
```bash
tcpdump -tni any 'udp port 51830' >> /var/log/wireguard/wireguard.log
```

Add new user:
1. add peer.template in wg0.conf
2. generate private and public key user:  

WINDOWS
1. Скопировать по ssh файл конфиг: wg0.conf находящийся в папке пользователя
2. Через Планировщик заданий указать
  - Сценарий: PATH to wireguard.exe
  - Триггер: запуск компьютера
  - Аргументы: /installtunnelservice "PATH to wg0.conf"

LINUX
1. apt install resolvconf
2. apt install wireguard
3. Execute: ./create-user login 
4. Скопировать по ssh файл конфиг: wg0.conf находящийся в папке пользователя в папку: /etc/wireguard/wg0.conf
5. wg-quick up wg0
6. wg

Enable with start boot: 
```bash
systemctl enable wg-quick@wg0
```

Disable with start boot: systemctl
```bash
systemctl disable wg-quick@wg0 
```
