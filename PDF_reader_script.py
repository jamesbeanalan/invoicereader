from pdfreader import SimplePDFViewer
import os

import pandas
from pandas import *


# Directory containing PDF files
directory = r"C:\Users\alanbean\Downloads\Additional\PDF_compiler\MTMC"

dic = {}

def extract_file_info(filename):
    if filename.endswith('.pdf'):
            print(f"Processing file: {filename}")
            with open(filename, "rb") as f:
                viewer = SimplePDFViewer(f)
                text_content = []
                
                # Read each page
                for page in viewer:
                    text_content.extend(page.strings)
                
                # Find 'Invoice No.' and print the next element
                title = text_content[0]
                if (title == "Official Receipt"):
                    try:
                        index = text_content.index("This is a computer-generated document. No signature is required.")
                        payer_name = text_content[index + 1]
                        print(f"payer name: {payer_name}")
                        index = text_content.index("Receipt No. ")
                        invoice_number = text_content[index + 2]
                        print(f"Receipt Number: {invoice_number}")
                        index = text_content.index('Total Amount Received')
                        total_amount = text_content[index+1]
                        print(f"Payable Sum: {total_amount}")
                    except ValueError:
                        print("Something is wrong")
                else:
                    try:
                        index = text_content.index('Invoice Date')
                        payer_name = text_content[index + 4]
                        if payer_name == "Credit Term":
                            index = text_content.index("Credit Term")
                            if text_content[index+3] == '30 days' or text_content[index+3] == "Immediate":
                                payer_name = text_content[index + 4]
                            else:
                                payer_name = text_content[index + 3]
                        print(f"payer name: {payer_name}")
                        index = text_content.index('Invoice No.')
                        invoice_number = text_content[index + 3]
                        print(f"Invoice Number: {invoice_number}")
                        index = text_content.index('Total Payable Amount')
                        total_amount = text_content[index+1]
                        print(f"Payable Sum: {text_content[index+1]}")
                    except ValueError:
                        print("Invoice No. not found or format not as expected.")
                print()  # Print empty line for separation between files
            return payer_name,invoice_number,filename


# Iterate over files in directory
def files_in_folder(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(directory, filename)
            print(f"Processing file: {filename}")
            
            # Open the PDF file in binary mode
            with open(filepath, "rb") as f:
                viewer = SimplePDFViewer(f)
                text_content = []
                
                # Read each page
                for page in viewer:
                    text_content.extend(page.strings)
                
                # Find 'Invoice No.' and print the next element
                title = text_content[0]
                if (title == "Official Receipt"):
                    try:
                        index = text_content.index("This is a computer-generated document. No signature is required.")
                        payer_name = text_content[index + 1]
                        print(f"payer name: {payer_name}")
                        index = text_content.index("Receipt No. ")
                        invoice_number = text_content[index + 2]
                        print(f"Receipt Number: {invoice_number}")
                        index = text_content.index('Total Amount Received')
                        total_amount = text_content[index+1]
                        print(f"Payable Sum: {total_amount}")
                    except ValueError:
                        print("Something is wrong")
                else:
                    try:
                        index = text_content.index('Invoice Date')
                        payer_name = text_content[index + 4]
                        if payer_name == "Credit Term":
                            payer_name = text_content[index + 8]
                        print(f"payer name: {payer_name}")
                        index = text_content.index('Invoice No.')
                        invoice_number = text_content[index + 3]
                        print(f"Invoice Number: {invoice_number}")
                        index = text_content.index('Total Payable Amount')
                        total_amount = text_content[index+1]
                        print(f"Payable Sum: {text_content[index+1]}")
                    except ValueError:
                        print("Invoice No. not found or format not as expected.")
        print()  # Print empty line for separation between files
    return payer_name,invoice_number,filename

def get_name_TINV(str):
    try:
        index = str.index("Credit Term")
        if str[index+3] == '30 days' or str[index+3] == "Immediate":
            return str[index + 4]
        else:
            return str[index + 3]
    except ValueError:
        print("Name not found")

def list_folders(directory):
    # Check if the provided directory path exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return []
    
    # Initialize an empty list to store folder names
    folder_names = []
    
    # Iterate through items (files and directories) in the specified directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        # Check if the item is a directory
        if os.path.isdir(item_path):
            folder_names.append(item)
    
    return folder_names

def list_all_files_in_all_folders(directory):
    lsts = list_folders(directory)
    for folders in lsts:
        temp = directory + "\\" +  folders
        print(f"folder location: {folders}")
        try:
            files_in_folder(temp)
            print()
            print()
        except ValueError:
            list_all_files_in_all_folders(temp)
    return

def search_nested_dict(dictionary, target_key):
    # Base case: if dictionary is empty, return None
    if not dictionary:
        return None
    
    # Check if the target key is in the current level of the dictionary
    if target_key in dictionary:
        return dictionary[target_key]
    else:   
        # Recursive case: iterate through each key-value pair and search recursively
        for key, value in dictionary.items():
            # Check if the value is a dictionary (assuming nested dictionaries)
            if type(value) == dict:
                # Recursively search in the nested dictionary
                result = search_nested_dict(dictionary[key], target_key)
                if result is not None:
                    return result
    return None

def set_dictionary(workbook):
    dic = {}
    for sheet_name, df in workbook.items():
        # Assuming "Module Code" and "Participant Name" columns exist in each sheet
        dic[sheet_name] = {}
        for index, row in df.iterrows():
            Module_code = row["Module Code"]
            Participant_name = row["Participant Name"]
            if Module_code not in dic[sheet_name]:
                count = "count"
                dic[sheet_name][Module_code] = {count : 0}
            if dic[sheet_name][Module_code].get(count) < 9:
                newcount = f"(0{dic[sheet_name][Module_code].get(count) + 1})"
            else:
                newcount = f"({dic[sheet_name][Module_code].get(count) + 1})"
            dic[sheet_name][Module_code][Participant_name] = newcount
            dic[sheet_name][Module_code][count] += 1
    return dic

#def rename_files(directory, df):
    lsts = list_folders(directory)
    dict = set_dictionary(df)
    for folders in lsts:
        temp = directory + "\\" +  folders
        print(f"folder location: {folders}")
        name, invoice, oldfile = files_in_folder(temp)
        number = search_nested_dict(dict,name)
        if number is None:
            print(f"{name} not in dictionary renaming with company...")
            os.rename(f"{temp}\\{oldfile}",f"{temp}\\{invoice} - {name}.pdf")
            print()
            print()
        else:
            print(f"{name} is found, renaming...")
            os.rename(f"{temp}\\{oldfile}",f"{temp}\\{number} {invoice} - {name}.pdf")
            print()
            print()
    return

def rename_files(directory, df):
    lsts = list_folders(directory)
    print(lsts)
    dict = set_dictionary(df)
    for folders in lsts:
        temp = directory + "\\" +  folders
        print(f"folder location: {folders}")
        print()
        for root, _, files in os.walk(temp):
            for filename in files:
                print(filename)
                filepath = os.path.join(root, filename)
                name, invoice, oldfile = extract_file_info(filepath)
                number = search_nested_dict(dict,name)
                if number is None:
                    print(f"{name} not in dictionary renaming with company...")
                    os.rename(f"{oldfile}",f"{temp}\\{invoice} - {name}.pdf")
                    print()
                    print()
                else:
                    print(f"{name} is found, renaming...")
                    print(oldfile)
                    os.rename(f"{oldfile}",f"{temp}\\{number} {invoice} - {name}.pdf")
                    print()
                    print()
    return   

directory = r"your directory"
dataframe1 = pandas.read_excel('your data set',sheet_name = None)

rename_files(directory, dataframe1)
