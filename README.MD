Cоздание ключа для сервера
```bash
wg genkey | tee /etc/wireguard/{title_private_key} | wg pubkey | tee /etc/wireguard/{title_pub_key}
```

---

### Настройка VPN client для ОС:
#### WINDOWS
1. Execute: ./create-user {login}
2. Скопировать по ssh файл конфиг: wg0.conf находящийся в папке пользователя 
3. Через Планировщик заданий указать
  - Сценарий: PATH to wireguard.exe
  - Триггер: запуск компьютера
  - Аргументы: /installtunnelservice "PATH to wg0.conf"

#### LINUX
1. apt install resolvconf wireguard
2. Execute: ./create-user {login} 
3. Скопировать по ssh файл конфиг: wg0.conf находящийся в папке пользователя в папку: /etc/wireguard/wg0.conf
4. wg-quick up wg0
5. wg

--- 

### Полезные команды
Добавление нового клиента:
```bash
./create-user {login}
```

Просмотр всех клиентов и их IP:
```bash
./show
```

Отображение свободного IP:
```bash
./free
```

---
### Работа со службой wireguard
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

Enable with start boot: 
```bash
systemctl enable wg-quick@wg0
```

Disable with start boot: systemctl
```bash
systemctl disable wg-quick@wg0 
```

---

### Отладка
Dump network (logs)
```bash
tcpdump -tni any 'udp port 51830' >> /var/log/wireguard/wireguard.log
```
