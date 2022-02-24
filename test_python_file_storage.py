from flask import Flask
from io import BytesIO
from werkzeug.datastructures import FileStorage


if __name__ == "__main__":
    copy = None
    print("Starting")
    file_storage = None
    file = open("uploads/test.png", 'rb')
    print("original")
    print(file.read())
    file.seek(0)
    file_storage = FileStorage(file)
    copy = BytesIO(file_storage.stream.read())



    file.close()
    print("copied")
    reader = file_storage.stream
    # print(file_storage.stream)
    print(reader)
    print(copy.read())
    # with open(reader, 'rb') as fp:
    #     print(fp.read())
