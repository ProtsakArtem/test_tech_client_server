import socket
import asyncio
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import hashlib
import json
import os

async def main():
    with open("server_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    reader, writer = await asyncio.open_connection('localhost', 9999)

    choice = str(input("Оберіть дію: 1-додати запис, 2-завантажити багато записів з json "))

    if choice == '1':
        command= 'add_record'
        name = input("Введите имя: ")
        description = input("Введите описание: ")
        data = {'command': command, 'name': name, 'description': description}
    elif choice == '2':
        command = 'add_multiple_records'
        print('Формат json: {"user1": "data1", "user2": "data2"...}')
        json_file_path = input("Введіть шлях до файлу з JSON: ")
        if not os.path.isfile(json_file_path):
            print("Файл не знайдено")
            return
        try:
            with open(json_file_path, 'r') as file:
                records = json.load(file)
            data = {'command': command, 'records': records}
        except json.JSONDecodeError:
            print("Некоректний JSON формат")
            return
    else:
        print("Невідома команда.")
        return

    data_json = json.dumps(data).encode('utf-8')

    hash_object = hashlib.sha256(data_json)
    data_hash = hash_object.hexdigest()

    data_with_hash = data_json + b":" + data_hash.encode('utf-8')

    symmetric_key = Fernet.generate_key()
    cipher_suite = Fernet(symmetric_key)

    encrypted_data = cipher_suite.encrypt(data_with_hash)

    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    writer.write(encrypted_symmetric_key + b'::' + encrypted_data)
    await writer.drain()

    encrypted_response = await reader.read(4096)

    decrypted_response = cipher_suite.decrypt(encrypted_response).decode('utf-8')

    response_message, response_hash = decrypted_response.rsplit(':', 1)
    hash_object = hashlib.sha256(response_message.encode('utf-8'))
    if hash_object.hexdigest() == response_hash:
        print("Відповідь від сервера:", response_message)
    else:
        print("Перевірка цілісності відповіді не пройдена.")

    writer.close()
    await writer.wait_closed()

asyncio.run(main())
