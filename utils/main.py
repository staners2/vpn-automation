from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List
from colorama import Fore
import os, argparse, sys, ipaddress
import chevron

@dataclass
class User:
    interface: dict = field(default_factory=dict)
    peer: dict = field(default_factory=dict)
    username: Optional[str] = None
    
    def __get_username(self) -> str:
        return f"\n{Fore.GREEN}{self.username}{Fore.RESET}\n"

    def __get_key_settings(self, key: str) -> str:
        return f"    {Fore.CYAN}{key}{Fore.RESET}"
    
    def __get_value_settings(self, value: str) -> str:
        return f"{Fore.RED}{value}{Fore.RESET}"
    
    def __str__(self) -> str:
        message = self.__get_username()
        message += "  Interface:\n"
        
        for key, value in self.interface.items():
            message += f"{self.__get_key_settings(key)} = {self.__get_value_settings(value)}\n"
        message += "\n  Peer:\n"
        for key, value in self.peer.items():
            message += f"{self.__get_key_settings(key)} = {self.__get_value_settings(value)}\n"
        return message
    
    def only_ip(self) -> str:
        message = self.__get_username()
        for key, value in self.interface.items():
            if key == "Address":
                message += f"{self.__get_key_settings(key)} = {self.__get_value_settings(value)}"
        return message
        
@dataclass
class Users:
    users: List[User] = field(default_factory=list)
    
    def __str__(self) -> str:
        message = ""
        for user in self.users:
           message += str(user)
        return message
            
    def only_ip(self) -> str:
        message = ""
        for user in self.users:
            message += user.only_ip()    
        return message
    
    def get_free_ip(self) -> str:
        max_address = ipaddress.ip_address(self.users[0].interface["Address"].split("/")[0])
        for user in self.users:
            current_address = ipaddress.ip_address(user.interface["Address"].split("/")[0])
            if current_address > max_address:
                max_address = current_address
        
        return f"{max_address + 1}/32"
        


MAIN_DIRECTORY = Path("/home/wireguard/wireguard.conf")
PATH_USERS = Path(str(MAIN_DIRECTORY.absolute()) + "/users")
# TEST_PATH_USERS = Path("." + "/users")
CONFIG_NAME = "wg0.conf"

def check_user(path: Path) -> User | None:
    """Готовит словарь конфигурации для пользователя

    Args:
        path (Path): путь до папки пользователя

    Returns:
        User | None: готовая конфигурация пользователя
    """
    interface = dict()
    peer = dict()
    current_array = None
    file = str(path.absolute()) + "/" + CONFIG_NAME
    
    if not Path(file).exists():
        print(f'{Path(file).parent} file not found!')
        return None
    
    for row in open(file).readlines():
        if row.__contains__("Peer"):
            current_array = peer
            continue
        if row.__contains__("Interface"):
            current_array = interface
            continue

        value = row.replace("\n", "").split(" = ")
        try:
            current_array[value[0]] = value[1]
        except:
            continue
    return User(interface, peer, path.name)

def generate_secret(name: str, folder: Path) -> (str, str):
    path_folder = str(folder.absolute())
    os.system(f"wg genkey | tee {folder}/{name}_private | wg pubkey | tee {folder}/{name}_public > /dev/null")
    
    private_key = Path(str(folder.absolute()) + f"/{name}_private").read_text()
    public_key = Path(str(folder.absolute()) + f"/{name}_public").read_text()
    
    return public_key, private_key

def generate_body_config_user(ip: str, private_key: str, folder: Path) -> str:
    data = {"ip": ip, "private_key": private_key}
    return chevron.render(Path("/etc/wireguard/utils/template/new_user.mustache").read_text(), data)

def generate_new_user(users: Users, name: str):
    folder = Path(str(PATH_USERS.absolute()) + f"/{name}")
    folder.mkdir(exist_ok=True)
    
    public_key, private_key = generate_secret(name, folder)
    ip = users.get_free_ip()
    config_body = generate_body_config_user(ip, private_key, folder)
    
    config = Path(str(folder.absolute()) + f"/{CONFIG_NAME}")
    config.write_text(config_body)
    
    print(f"{Fore.GREEN}>>> User {Fore.CYAN}{name}{Fore.GREEN} sucessfull created with ip: {Fore.CYAN}{ip}")

if __name__ == "__main__":
    users = Users()
    for _, dirs, _ in os.walk(PATH_USERS):
        for dir in dirs:
            user = check_user(Path(str(PATH_USERS.absolute()) + "/" + dir)) 
            if user is not None:
                users.users.append(user)
    
    parser = argparse.ArgumentParser(description='Утилита вывода конфигурации WireGuard')
    parser.add_argument('-a', '--all-info', dest="all_info", action="store_true", help='Отображает весь конфиг пользователей')
    parser.add_argument('-ip', '--only-ip', dest="only_ip", action="store_true", help='Отобразить IP всех пользователей')
    parser.add_argument('-free', '--free-ip', dest="free_ip", action="store_true", help='Получить свободный IP')
    parser.add_argument('-create', '--create-user', dest="create_user", type=str, help='Логин пользователя')
    args = parser.parse_args(sys.argv[1:])
    
    if args.only_ip:
        print(users.only_ip())
    elif args.all_info:
        print(users)
    elif args.free_ip:
        print(users.get_free_ip())
    elif args.create_user:
        generate_new_user(users, args.create_user)

