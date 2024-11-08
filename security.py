from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
import os
import json

def hasFile(file):
    return os.path.isfile(os.path.abspath(file))
def hasRSA():
    if os.path.isfile(os.path.abspath('./key/public_key.pem')) and os.path.isfile(os.path.abspath('./key/private_key.pem')):
        return True
    else:
        print("False")
        return False
def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)
def read_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    return data
def remove_data(data):
    os.remove(os.abs.path(data))
def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    write_file(os.path.abspath("./key/public_key.pem"), public_key)
    write_file(os.path.abspath("./key/private_key.pem"), private_key)
    
def encrypt_data(data,name):
    if hasRSA() == True:
        public_key = read_file(os.path.abspath("./key/public_key.pem"))
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        encrypted_data = cipher.encrypt(data)
        write_file(os.path.abspath("./SavedData/"+name+"_encrypted.txt"), encrypted_data)
    
    else:
        generate_key_pair()
        encrypt_data(data,name)
        
def delete_user_data(user):
    os.remove(os.path.abspath(f"./SavedData/user_{user}_encrypted.txt"))
    
def decrypt_data(filename):
    with open(os.path.abspath(filename), 'rb') as file:
        encrypted_data = file.read()
    
    key = RSA.import_key(open(os.path.abspath('./key/private_key.pem')).read())
    cipher = PKCS1_OAEP.new(key)
    
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
    except ValueError as e:
        print(f"復号化エラー: {e}")
        return None

    #else:
    #    generate_key_pair()
    #    return decrypt_data(data)
# ファイルに書き出す

#encrypt_data('ariitaiyo'.encode('utf-8'),'id')

def encrypt_user_data(userid, password, alias):
    """ユーザー情報を暗号化して保存"""
    data = {
        'userid': userid,
        'password': password
    }
    encrypted_data = json.dumps(data).encode('utf-8')
    encrypt_data(encrypted_data, f'user_{alias}')

def get_saved_users():
    """保存されているユーザー一覧を取得"""
    saved_users = []
    data_dir = os.path.abspath("./SavedData")
    for file in os.listdir(data_dir):
        if file.startswith('user_') and file.endswith('_encrypted.txt'):
            alias = file[5:-14]  # 'user_' と '_encrypted.txt' を除去
            saved_users.append(alias)
    return saved_users

def get_user_data(alias):
    """特定のユーザー情報を復号化して取得"""
    filename = os.path.abspath(f"./SavedData/user_{alias}_encrypted.txt")
    if not os.path.exists(filename):
        return None
    
    decrypted_data = decrypt_data(filename)
    if decrypted_data:
        return json.loads(decrypted_data)
    return None