import boto3
import re
import argparse
import os

# Ustawienia połączenia z S3
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

BUCKET_NAME = 'developer-task'
PREFIX = 'a-wing/'

# Tworzenie sesji boto3
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
s3 = session.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

def list_files():
    print("Lista plików w bucket:")
    for obj in bucket.objects.filter(Prefix=PREFIX):
        print(obj.key)

def upload_file(local_file, s3_file):
    try:
        bucket.upload_file(local_file, s3_file)
        print(f'Plik {local_file} został przesłany jako {s3_file}.')
    except Exception as e:
        print(f'Wystąpił błąd podczas przesyłania pliku: {e}')

def list_files_with_filter(regex):
    pattern = re.compile(regex)
    print("Pliki pasujące do filtra:")
    for obj in bucket.objects.filter(Prefix=PREFIX):
        if pattern.search(obj.key):
            print(obj.key)

def delete_files_matching_regex(regex):
    pattern = re.compile(regex)
    deleted_files = []
    for obj in bucket.objects.filter(Prefix=PREFIX):
        if pattern.search(obj.key):
            bucket.Object(obj.key).delete()
            deleted_files.append(obj.key)
    print("Usunięte pliki:")
    for file in deleted_files:
        print(file)

def main():
    parser = argparse.ArgumentParser(description='CLI do zarządzania plikami S3.')
    parser.add_argument('--list', action='store_true', help='Wyświetl wszystkie pliki w bucket.')
    parser.add_argument('--upload', nargs=2, metavar=('LOCAL_FILE', 'S3_FILE'), help='Prześlij plik do bucket.')
    parser.add_argument('--filter', type=str, help='Wyświetl pliki zgodne z podanym regexem.')
    parser.add_argument('--delete', type=str, help='Usuń pliki zgodne z podanym regexem.')

    args = parser.parse_args()

    if args.list:
        list_files()
    if args.upload:
        local_file, s3_file = args.upload
        upload_file(local_file, PREFIX + s3_file)
    if args.filter:
        list_files_with_filter(args.filter)
    if args.delete:
        delete_files_matching_regex(args.delete)

if __name__ == '__main__':
    main()
