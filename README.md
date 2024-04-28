# Sendgrid_Subaccounts_API_Keys_Extraction
Ready-to-use Python Script for Extracting all Subaccounts API Keys under Parent SendGrid Account.

## Note
The code, in its current stage is for downloading only subaccount API keys and wrtiting them to a CSV file, if you wish the code can be configured to bring any information you wish that the API call might include during extraction, such as dedicated IP Addresses of each subaccount.

## Prerequisites 
* **Python 3.12 or higher**. Download it from https://www.python.org/downloads/
* **IDE** - I personally used Visual Studio Code but it is upto your preference.
* **Libraries - Requests**: Run in Terminal of enviornment or in command prompt **pip install requests**
* **Libraries - Threading**: Run in Terminal of enviornment or in command prompt **pip install threading**
* **Libraries - CSV**: Run in Terminal of enviornment or in command prompt **pip install csv**
* **SendGrid API Key**. You must have the API key enabled with minimum Read permissions from your Sendgrid Parent account.

## Languages, Frameworks and API calls used in the script
The Script uses the following:

- *[Python 3.12.3](https://www.python.org/downloads/release/python-3123/)* as the primary Programming Language.
- *[Visual Studio Code](https://code.visualstudio.com/download)* as the IDE.
- *[Sendgrid V3 API](https://docs.sendgrid.com/api-reference/how-to-use-the-sendgrid-v3-api/authentication)* as the primary endpoint for primary Authorization header.
- *[Sendgrid V3 API Subusers](https://docs.sendgrid.com/api-reference/subusers-api/list-all-subusers)* as secondary API endpoint for listing all subuser accounts in the parent account. The same endpoint also contains offset and limit parameters for generating **paginated** results, all subuser accounts.
- *[Sendgrid V3 API On-Behalf-Of](https://docs.sendgrid.com/api-reference/how-to-use-the-sendgrid-v3-api/on-behalf-of)* as the endpoint for making api endpoint calls for each subaccount on behalf of the parent account to allow GET requests access to each subaccount.
- *[Sendgrid V3 API Keys](https://docs.sendgrid.com/api-reference/api-keys/retrieve-an-existing-api-key)* the endpoint for making GET calls to each individual subaccount for retrieving any API Keys that they may have generated in their account.
- *[Requests Module](https://pypi.org/project/requests/)* allows us to make HTTP/1.1 request calls.
- *[Threading Module](https://docs.python.org/3/library/threading.html)* is used to allow us to make multiple parallel API calls using multi-threading of the computation device in order to retrieve multiple API Keys simuoultaneously to increase efficiency.
**Note** concurrent.futures.ThreadPoolExecutor module can also be used in place here for increasing if you wish for a higher level of control and wish to push tasks to background threads, which will increase process time a bit but put less stress on the machine.  
-  *[CSV Module](https://docs.python.org/3/library/csv.html)* allows us to write or read CSV files, in this case write all retrieved data to a CSV file.

## Legal
* This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by Sendgrid or any of its affiliates or subsidiaries. This is an independent and unofficial software. Use at your own risk. Commercial use of this code/repo is strictly prohibited.

## Basic Usage

### API_Key Replacement
Simply replace the value in **sendgrid_api_key** with your own API key and run the script. 

#Set your SendGrid API key
```
sendgrid_api_key = 'YOUR_API_KEY'
```

### Adjusting Chunk Size
You can also adjust the **chunk_size** value to allow to retrieve a larger chunk of data depending on the scale of the database you wish to retrieve as well as the capabilities of your machine.
```python
#Create threads for fetching API keys concurrently
        threads = []
        result_list = []
        chunk_size = 20  # Adjust the chunk size based on your requirements
        for i in range(0, len(all_subaccounts), chunk_size):
            chunk = all_subaccounts[i:i+chunk_size]
            thread = threading.Thread(target=fetch_api_keys, args=(chunk, result_list))
            threads.append(thread)
            thread.start()
```

### Adjusting Page Size
You can also adjust the **page_size** value for the number of data you wish for each paginated results to retrieve. This value will defer from case to case and you may need to do trial and error for finding the perfect sweet spot but I recommend on average starting with 100 pages and increasing the number upwards until diminishing returns on processing speed.
```python
# Function to fetch SendGrid subaccounts with pagination
def get_sendgrid_subaccounts(page=1, page_size=1000): #Page size adjust according to you requirements
    try:
        headers = {
            'Authorization': f'Bearer {sendgrid_api_key}'
        }
        params = {
            'limit': page_size,
            'offset': (page - 1) * page_size
        }
        response = requests.get(sendgrid_subaccounts_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error fetching SendGrid subaccounts:", e)
        return None
```

### CSV File
The data will be saved in a CSV file **sendgrid_subaccounts.csv**, which you can change to your desire and also include a path for saving if you wish but by default the file will be saved in the IDE Directory folder. 
            
