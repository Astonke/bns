#!/bin/python3
import socket
import threading
import base64
import hashlib
#import binascii
import re
from my_func import *

   

print("                    </Tasker_master>")
host = '0.0.0.0'  # Listen on all network interfaces
port = 5050        # The port used by the server (non-privileged ports are > 1023)
session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'server set to work on:{host}:{port}..\n')
session.bind((host, port))
session.listen()


def is_origin_allowed(origin):
    return True
            

def svr_handler(session_data,session_address,origin):
    if is_origin_allowed(origin):
        key_match =re.search(r"Sec-WebSocket-key: (,+?)\r\n",session_data.recv(2048).decode('utf-8'))
        key = key_match.group(1) if key_match else None
        if key:
            #calc websocket handshake
            response_key=base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5ABODC85B11").encode('utf-8')).digest()).decode('utf-8')
            response={
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {response_key}"
            }
            session_data.send(response.encode('utf-8'))
            
    print(f'\nwaiting for connection at[0.0.0.0:{port}]...')
     
    
def main():
    session_data,session_address=session.accept()
    out_data=session_data.recv(2048).decode('utf-8')
    origin_match=re.search(r'Origin: (,+?)\r\n',out_data)
    origin = origin_match.group(1) if origin_match else None
    
    print(f"\n{session_address}")
    #print(out_data)
    
    #response_data=json.dumps(json_data)
            
    response_data=get_page('index.html')
    
    if 'amount' in str(out_data):
        print(f'received data:\n{out_data}')
        j_response={'redirect':True,'info':'order_made'}
        responder(j_response,session_data)
    if 'register' in (out_data):
        print(f'\nreceived_data_from sign_in:\n{out_data}\n')
        client_feed=make_dict(take_json(out_data))
        name=client_feed['name']
        email=client_feed['email']
        password=client_feed['psk']
        mobile_no=client_feed['mobile']
        if check_in_db(mobile_no):
            #user exists
            j_response={'redirect':True,'info':'user already exists'}
            responder(j_response,session_data)
        else:
            c_data=[mobile_no,email,password,name]
            append_data(c_data,'data.csv')
            j_response={'redirect':True,'info':'Account_created'}
            responder(j_response,session_data)
        #session_data.close()
    if 'login' in out_data:
        print(f'\nreceived_data_from sign_in:\n{out_data}\n')
        client_feed=make_dict(take_json(out_data))
        print(client_feed)
        password=client_feed['psk']
        mobile_no=client_feed['mobile']
        if check_in_db(mobile_no):
            client_list=get_user_data(read_data('data.csv'), "mobile", mobile_no)
            psk=client_list[2]
            if  password==psk:
                user_id=client_list[3]
                j_response={'redirect':True,'info':'verified','user_id':mobile_no}
                #print(j_response)
                responder(j_response,session_data)
            
            else:
                j_response={'redirect':False,'info':'invalid_psk'}
                responder(j_response,session_data)
                pass
        else:
            j_response={'redirect':False,'info':'invalid'}
            responder(j_response,session_data)
            pass
        
    #config multithread      
    client_handler=threading.Thread(target=svr_handler,args=(session_data,session_address,origin))
    client_handler.start() 
    
while True:
    main()