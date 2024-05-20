import requests
import threading
import csv

# Set your SendGrid API key
sendgrid_api_key = 'YOUR_API_KEY'

# Define SendGrid API endpoint for subaccounts
sendgrid_subaccounts_url = 'https://api.sendgrid.com/v3/subusers'

# Function to fetch SendGrid subaccounts with pagination
def get_sendgrid_subaccounts(page=1, page_size=1000):
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

# Function to fetch API keys for a subaccount
def get_subaccount_api_keys(subaccount_username):
    try:
        headers = {
            'Authorization': f'Bearer {sendgrid_api_key}',
            'on-behalf-of': subaccount_username
        }
        url = f'https://api.sendgrid.com/v3/api_keys'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching API keys for subaccount {subaccount_username}:", e)
        return None

# Function to fetch API keys for multiple subaccounts concurrently
def fetch_api_keys(subaccounts, result_list):
    api_keys_list = []
    for subaccount in subaccounts:
        subaccount_username = subaccount['username']
        api_keys = get_subaccount_api_keys(subaccount_username)
        if api_keys is None:
            api_keys = {'result': []}  # Empty dictionary if no API keys found
        api_keys_list.append((subaccount, api_keys))
    result_list.extend(api_keys_list)

# Main function to execute
def main():
    # Fetch SendGrid subaccounts with pagination
    page = 1
    all_subaccounts = []
    while True:
        subaccounts = get_sendgrid_subaccounts(page=page)
        if not subaccounts:
            break
        all_subaccounts.extend(subaccounts)
        page += 1

    # Open CSV file for writing
    with open('sendgrid_subaccounts.csv', 'w', newline='') as csvfile:
        fieldnames = ['Subaccount Username', 'API Key ID', 'API Key Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Create threads for fetching API keys concurrently
        threads = []
        result_list = []
        chunk_size = 20  # Adjust the chunk size based on your requirements
        for i in range(0, len(all_subaccounts), chunk_size):
            chunk = all_subaccounts[i:i+chunk_size]
            thread = threading.Thread(target=fetch_api_keys, args=(chunk, result_list))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Write subaccount information to CSV file
        for subaccount, keys in result_list:
            subaccount_username = subaccount['username']
            if keys['result']:  # Check if API keys are present
                for key in keys['result']:
                    writer.writerow({'Subaccount Username': subaccount_username,
                                        'API Key ID': key['api_key_id'],
                                        'API Key Name': key.get('name', 'Unnamed')})
            else:
                writer.writerow({'Subaccount Username': subaccount_username,
                                    'API Key ID': 'No API keys found',
                                    'API Key Name': ''})

if __name__ == "__main__":
    main()
