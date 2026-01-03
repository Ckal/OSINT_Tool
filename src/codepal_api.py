import requests

# Replace with your CodePal API Key
API_KEY = "YOUR_API_KEY"

# Define the request URL
url = "https://api.codepal.ai/v1/cicd-pipeline-writer/query"

# Define the request body (the description of the pipeline you want to generate)
data = {
    "prompt": "Builds a Docker image and deploys it to a Kubernetes cluster using GitHub Actions.",
    "pipeline_name": "github-actions"
}

# Set up the headers for authentication
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Send the POST request to CodePal
response = requests.post(url, headers=headers, data=data)

# Handle the response
if response.status_code == 201:
    pipeline = response.json()
    print("Pipeline Generated Successfully:")
    print(pipeline["result"])  # This will print the generated pipeline code
else:
    print(f"Error: {response.status_code}")
    print(response.text)
