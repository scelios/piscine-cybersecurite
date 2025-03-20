import argparse
import os
import sys
import time
import requests
import json
import re

class Vaccine:
    def __init__(self, args):
        self.url = args.url
        self.output = args.o
        self.request_type = args.X
        self.input = self.extract_form_inputs(self.get_data_from_url())

    def get_data_from_url(self):
        match self.request_type:
            case "GET":
                return requests.get(self.url).text
            case "POST":
                return requests.post(self.url).text
            case "HEAD":
                return requests.head(self.url).text
            case "PUT":
                return requests.put(self.url).text
            case "DELETE":
                return requests.delete(self.url).text
            case "OPTIONS":
                return requests.options(self.url).text
            case "TRACE":
                return requests.trace(self.url).text
            case "PATCH":
                return requests.patch(self.url).text
            case _:
                return None

    def get_payloads(self):
        os.open("payloads.txt", "r")

    def extract_form_inputs(self, data):
        return re.findall(r'<input[^>]*>', data)
    
    def send_SQL_injection(self):
        for root, _, files in os.walk("injection/detect/"):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        payload = f.read()
                        filename = file.split(".")[0]
                        for input in self.input:
                            requests.post(self.url, data={input: payload})
                            with open(self.output, "a") as f:
                                f.write(f"Payload: {payload} - Input: {input}\n")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    
    def check_database(self):
        

def get_args():
    parser = argparse.ArgumentParser(
        description="SQL Injection tester, will test for SQL Injection vulnerabilities in a given URL"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="url to test")
    parser.add_argument("-o", type=str, default="output.txt", help="Archive file, by default it is output.txt")
    parser.add_argument("-X", type=str, default="GET", help="Request type, by default it is GET")
    args = parser.parse_args()

    return args

def check_args(args):
    autorised_request_types = ["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH"]
    if not os.path.exists(args.url):
        raise Exception("URL not found")
    if args.X not in autorised_request_types:
        raise Exception("Request type not allowed")
    if args.o == "" or len(args.o) < 5 or args.o[-4:] != ".txt" or len(args.o) > 30:
        raise Exception("Output file name not allowed")

def main():
    try:
        args = get_args()
        check_args(args)
        vaccine = Vaccine(args)
        vaccine.send_SQL_injection()


    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()