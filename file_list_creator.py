import boto3
import re
import json

def extract_info_from_filename(filename):
    # Example regular expression to extract information from the filename
    pattern = r'(.+)_([\d.]+)-.+~(.+)~(.+)_(\w+)\.(\w+)'
    match = re.match(pattern, filename)
    
    if match:
        path = "https://binaries2.erlang-solutions.com/" + filename
        version = match.group(2)
        os = match.group(3).capitalize()
        arch = match.group(5)
        
        return {
            "path": path,
            "version": version,
            "os": os,
            "arch": arch,
            "tests": "",
            "checksum": ""
        }
    else:
        return None

# Configure S3 client
s3_client = boto3.client('s3')

# S3 bucket name
bucket_name = 'esl-packages'

# Get the list of objects in the bucket
response = s3_client.list_objects(Bucket=bucket_name)

# Dictionary to store the final JSON structure for Elixir
elixir_json_data = {
    "tabs": [],
    "flavours_captions": {
        "main": "Standard"
    }
}

# Dictionary to store the final JSON structure for esl-erlang
erlang_json_data = {
    "tabs": [],
    "flavours_captions": {
        "main": "Standard"
    }
}

# Dictionary to store the final JSON structure for MongooseIM
mongooseim_json_data = {
    "tabs": [],
    "flavours_captions": {
        "main": "Standard"
    }
}

# Iterate over the objects
for obj in response['Contents']:
    filename = obj['Key']
    
    # Extract information from the filename
    file_info = extract_info_from_filename(filename)
    
    if file_info:
        tab_name, os_name = filename.split("/")[-2:]
        
        if "elixir" in filename:
            # Check if a tab with the OS name already exists in Elixir JSON data
            existing_tab = next((tab for tab in elixir_json_data["tabs"] if tab["name"] == os_name), None)
            if existing_tab:
                existing_flavour = next((flavour for flavour in existing_tab["flavours"] if flavour["name"] == "main"), None)
                if existing_flavour:
                    existing_flavour["packages"].append(file_info)
                else:
                    existing_tab["flavours"].append({
                        "name": "main",
                        "packages": [file_info],
                        "header": "",
                        "footer": ""
                    })
            else:
                elixir_json_data["tabs"].append({
                    "name": os_name,
                    "caption": os_name.capitalize(),
                    "header": "",
                    "footer": "",
                    "flavours": [
                        {
                            "name": "main",
                            "packages": [file_info],
                            "header": "",
                            "footer": ""
                        }
                    ]
                })
        elif "esl-erlang" in filename:
            # Check if a tab with the OS name already exists in esl-erlang JSON data
            existing_tab = next((tab for tab in erlang_json_data["tabs"] if tab["name"] == os_name), None)
            if existing_tab:
                existing_flavour = next((flavour for flavour in existing_tab["flavours"] if flavour["name"] == "main"), None)
                if existing_flavour:
                    existing_flavour["packages"].append(file_info)
                else:
                    existing_tab["flavours"].append({
                        "name": "main",
                        "packages": [file_info],
                        "header": "",
                        "footer": ""
                    })
            else:
                erlang_json_data["tabs"].append({
                    "name": os_name,
                    "caption": os_name.capitalize(),
                    "header": "",
                    "footer": "",
                    "flavours": [
                        {
                            "name": "main",
                            "packages": [file_info],
                            "header": "",
                            "footer": ""
                        }
                    ]
                })
        elif "mongooseim" in filename:
            # Check if a tab with the OS name already exists in MongooseIM JSON data
            existing_tab = next((tab for tab in mongooseim_json_data["tabs"] if tab["name"] == os_name), None)
            if existing_tab:
                existing_flavour = next((flavour for flavour in existing_tab["flavours"] if flavour["name"] == "main"), None)
                if existing_flavour:
                    existing_flavour["packages"].append(file_info)
                else:
                    existing_tab["flavours"].append({
                        "name": "main",
                        "packages": [file_info],
                        "header": "",
                        "footer": ""
                    })
            else:
                mongooseim_json_data["tabs"].append({
                    "name": os_name,
                    "caption": os_name.capitalize(),
                    "header": "",
                    "footer": "",
                    "flavours": [
                        {
                            "name": "main",
                            "packages": [file_info],
                            "header": "",
                            "footer": ""
                        }
                    ]
                })

# Write separate JSON files for Elixir, esl-erlang, and MongooseIM
with open('elixir_packages.json', 'w') as json_file:
    json_file.write("jsonCallback(" + json.dumps(elixir_json_data, indent=4) + ")")

with open('erlang_packages.json', 'w') as json_file:
    json_file.write("jsonCallback(" + json.dumps(erlang_json_data, indent=4) + ")")

with open('mongooseim_packages.json', 'w') as json_file:
    json_file.write("jsonCallback(" + json.dumps(mongooseim_json_data, indent=4) + ")")