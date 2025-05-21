# 🔐 SendGrid Subaccount API Key Exporter
This Python script retrieves all subaccounts under a SendGrid parent account and exports their associated API keys to a structured CSV file. It is designed for enterprise use cases such as audits, compliance reviews, access management, and automated reporting.
---
## 🚀 Key Features
* ✅ Authenticates using a parent-level SendGrid API key

* 🔄 Handles pagination automatically to retrieve all subaccounts

* ⚡ Fetches API keys for each subaccount concurrently using threads

* 📁 Outputs to a clean CSV format with subaccount-level granularity

* 🛡️ Built-in error handling for network/API errors and permission issues

---

## 🔧 Prerequisites
- Python 3.7+

- requests module (install with pip install requests)

---

## 🔐 Authentication
The script requires a parent SendGrid API key with permission to:

- List all subusers (GET /v3/subusers)

- Impersonate subaccounts (on-behalf-of header)

- List API keys under each subaccount (GET /v3/api_keys)

--- 

## 🧪 Environment Variables
Before running the script, ensure the following environment variable is set:

| Variable           | Description             | Required |
| ------------------ | ----------------------- | -------- |
| `SENDGRID_API_KEY` | Parent SendGrid API key | ✅ Yes    |

You can export it in your shell or load from a .env file:
```bash
export SENDGRID_API_KEY='your_sendgrid_parent_api_key'
```

## 📦 Usage
🖥️ Run the Script
```bash
python sendgrid_subaccount_export.py
```
Upon execution, the script will:

1. Fetch all SendGrid subaccounts.

2. Retrieve API keys for each subaccount in parallel.

3. Write results to sendgrid_subaccounts.csv.

---

📄 Output
The output file is named:
```bash
sendgrid_subaccounts.csv
```
Example CSV Structure:
| Subaccount Username | API Key ID                           | API Key Name    |
| ------------------- | ------------------------------------ | --------------- |
| client\_a           | 1e3a4f90-8f2b-4374-bdd4-abc123def456 | production\_key |
| client\_b           | No API keys found                    |                 |

---
## ⚙️ Performance & Scalability
- Uses multithreading for API key fetching to minimize latency.

- Adjustable chunk_size to control concurrency.

- Suitable for handling hundreds or thousands of subaccounts.

## 🛑 Error Handling
- Retries and fallbacks are built-in to gracefully handle:

     - API throttling

     - Subaccount permission issues

     - Network interruptions

If any subaccount fails to return API keys, it is recorded with "No API keys found".

---

## 🐳 Containerization Ready
This script relies only on environment variables and writes to the local directory—making it fully compatible with Docker containers or CI/CD pipelines.

## 📌 Notes
- API keys are sensitive credentials. Use access-controlled environments and rotate API keys regularly.

- SendGrid may enforce rate limits; consider spacing out requests or increasing chunk size if needed.

- API key details are limited to ID and Name. Secret values are not accessible via the API.

## 🤝 Contributing
Pull requests are welcome. For major changes:
* Fork the repo
* Create a feature branch
* Test your changes
* ubmit a PR with context

## 📝 License
This project is licensed under the MIT License

## 📬 Contact
For issues, questions, or feature requests, please contact:
Author: Mainul Hossain
Email: hossainmainul83@gmail.com
