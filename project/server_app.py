import socket
import asyncio
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from asgiref.sync import sync_to_async
import hashlib
import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from data_handler.models import DataRecord

@sync_to_async
def save_data_record(name, description):
    DataRecord.objects.create(name=name, encrypted_data=description)

@sync_to_async
def save_multiple_data_records(records):
    for name, description in records.items():
        DataRecord.objects.create(name=name, encrypted_data=description)

def validate_data_record(name, description):
    if not name or not description:
        return False, "Name and description must not be empty."
    return True, ""

def validate_multiple_data_records(records):
    for name, description in records.items():
        valid, message = validate_data_record(name, description)
        if not valid:
            return False, message
    return True, ""

async def handle_client(reader, writer):
    try:
        encrypted_message = await reader.read(4096)

        encrypted_symmetric_key, encrypted_data = encrypted_message.split(b'::')

        with open("server_private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)

        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        cipher_suite = Fernet(symmetric_key)
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')

        data_parts = decrypted_data.rsplit(':', 1)
        data_json = data_parts[0]
        received_hash = data_parts[1]

        hash_object = hashlib.sha256(data_json.encode('utf-8'))
        calculated_hash = hash_object.hexdigest()

        if calculated_hash == received_hash:
            data = json.loads(data_json)
            command = data.get('command')

            if command == 'add_record':
                name = data.get('name')
                description = data.get('description')
                valid, message = validate_data_record(name, description)
                if valid:
                    await save_data_record(name, description)
                    response_message = "DataRecord saved successfully."
                else:
                    response_message = f"Validation failed: {message}"
            elif command == 'add_multiple_records':
                records = data.get('records')
                valid, message = validate_multiple_data_records(records)
                if valid:
                    await save_multiple_data_records(records)
                    response_message = "Multiple DataRecords saved successfully."
                else:
                    response_message = f"Validation failed: {message}"
            else:
                response_message = "Unknown command."
        else:
            response_message = "Data integrity check failed."

    except Exception as e:
        response_message = f"Decryption or data integrity check failed: {e}"

    response_message = response_message.encode('utf-8')
    response_hash = hashlib.sha256(response_message).hexdigest()
    response_with_hash = response_message + b':' + response_hash.encode('utf-8')
    encrypted_response = cipher_suite.encrypt(response_with_hash)

    writer.write(encrypted_response)
    await writer.drain()

    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 9999)
    async with server:
        await server.serve_forever()

asyncio.run(main())
