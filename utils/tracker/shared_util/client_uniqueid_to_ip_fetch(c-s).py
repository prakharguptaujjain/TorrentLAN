import socket
import os
import json
import base64

CONFIG_CLIENT = "configs/client(c-s).json"
SERVER_CONFIG="configs/server.json"
SERVER_ADDR=json.load(open(SERVER_CONFIG))["server_addr"]

PORT = 8888

def get_ip_address(address):
    try:
        ip_address = socket.gethostbyname(address)
        return ip_address
    except socket.gaierror:
        return None

def get_ips_and_netmasks(unique_ids):
    ip = get_ip_address(SERVER_ADDR)
    print(f"Connecting to {ip}")
    try:
        # Connect to server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to server")
            s.connect((ip, PORT))
            print("Connected to server")
            js_data = {}
            js_data["ip_get"]=True
            js_data["unique_ids"] = unique_ids
            data_to_send = json.dumps(js_data)
            data_to_send += "<7a98966fd8ec965d43c9d7d9879e01570b3079cacf9de1735c7f2d511a62061f>" #"<"+ sha256 of "<EOF>"+">"
            s.sendall(data_to_send.encode())

            # Receive data
            data=b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data+=chunk
                if data.endswith(b"<7a98966fd8ec965d43c9d7d9879e01570b3079cacf9de1735c7f2d511a62061f>"): #"<"+ sha256 of "<EOF>"+">"
                    data = data[:-66]  # Remove termination sequence from the data
                    break
            json_returned_data = json.loads(data.decode())
            s.close()
        return True,json_returned_data
    except ConnectionRefusedError:
        print("Server is down")
        return False,None
if __name__ == '__main__':
    get_ips_and_netmasks()
