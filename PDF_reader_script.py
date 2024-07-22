from pdfreader import SimplePDFViewer
import os

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
                        receipt_number = text_content[index + 2]
                        print(f"Receipt Number: {receipt_number}")
                        index = text_content.index('Total Amount Received')
                        print(f"Payable Sum: {text_content[index+1]}")
                    except ValueError:
                        print("Something is wrong")
                else:
                    try:
                        index = text_content.index("30 days")
                        payer_name = text_content[index + 1]
                        print(f"payer name: {payer_name}")
                        index = text_content.index('Invoice No.')
                        invoice_number = text_content[index + 3]
                        print(f"Invoice Number: {invoice_number}")
                        index = text_content.index('Total Payable Amount')
                        print(f"Payable Sum: {text_content[index+1]}")
                    except ValueError:
                        print("Invoice No. not found or format not as expected.")
        print()  # Print empty line for separation between files


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
        print( f"folder location: {folders}")
        files_in_folder(temp)
        print()
        print()
    return
    