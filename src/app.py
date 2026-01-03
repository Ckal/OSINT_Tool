import streamlit as st
import requests
from src.github_analysis import analyze_github_repo
from src.url_fetcher import fetch_url_title
from src.fine_tune_helpers import fine_tune_model

# Title and description
st.title("OSINT Tool 🏢")
st.markdown("""
    This tool performs **Open Source Intelligence (OSINT)** analysis on GitHub repositories and fetches titles from URLs.
    It also allows uploading datasets (CSV format) for fine-tuning models like **DistilBERT**, **Code Summarization**, **Bug Fixing**, and more.
    """)

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose the mode", ["GitHub Repository Analysis", "URL Title Fetcher", "Dataset Upload & Fine-Tuning"])

# List of models for fine-tuning
available_models = [
    "semeru/code-text-galeras-code-summarization-3k-deduped",
    "semeru/code-code-InjectMutants",
    "semeru/code-code-BugFixingSmall",
    "semeru/code-code-GeneratingAssertsRaw",
    "deepseek-ai/DeepSeek-Prover-V1"
]

# GitHub Repository Analysis
if app_mode == "GitHub Repository Analysis":
    st.header("GitHub Repository Analysis")
    repo_owner = st.text_input("Enter GitHub Repository Owner", "huggingface")
    repo_name = st.text_input("Enter GitHub Repository Name", "transformers")
    
    if st.button("Analyze Repository"):
        if repo_owner and repo_name:
            repo_data = analyze_github_repo(repo_owner, repo_name)
            if repo_data:
                st.subheader("Repository Details")
                for key, value in repo_data.items():
                    st.write(f"**{key}**: {value}")
            else:
                st.error("Failed to retrieve repository details.")
        else:
            st.warning("Please enter both repository owner and name.")

# URL Title Fetcher
elif app_mode == "URL Title Fetcher":
    st.header("URL Title Fetcher")
    url = st.text_input("Enter URL", "https://www.huggingface.co")
    
    if st.button("Fetch Title"):
        if url:
            title = fetch_url_title(url)
            if title:
                st.write(f"**Page Title**: {title}")
            else:
                st.error("Failed to retrieve the page title.")
        else:
            st.warning("Please enter a valid URL.")

# Dataset Upload & Fine-Tuning
elif app_mode == "Dataset Upload & Fine-Tuning":
    st.header("Dataset Upload & Fine-Tuning")
    
    # Model selection for fine-tuning
    model_choice = st.selectbox("Choose Model for Fine-Tuning", available_models)
    
    # Upload a CSV file for fine-tuning
    uploaded_file = st.file_uploader("Upload a CSV file for fine-tuning", type="csv")
    
    if uploaded_file is not None:
        st.write(f"Preparing fine-tuning for model: **{model_choice}**")
        st.write("File successfully uploaded! Now starting fine-tuning process...")
        fine_tune_model(uploaded_file, model_choice)  # Assuming the fine_tune_model function handles fine-tuning

# Helper Functions for API Interaction
def analyze_github_repo(owner, repo):
    """Analyzes a GitHub repository and returns information about it."""
    try:
        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}')
        response.raise_for_status()
        repo_data = response.json()
        return {
            "Repository Name": repo_data['name'],
            "Owner": repo_data['owner']['login'],
            "Stars": repo_data['stargazers_count'],
            "Forks": repo_data['forks_count'],
            "Issues": repo_data['open_issues_count'],
            "Language": repo_data['language'],
            "Description": repo_data.get('description', 'No description available.')
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching GitHub repository: {e}")
        return None

def fetch_url_title(url):
    """Fetches the title of a webpage."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Extract the title from the HTML content
            html_content = response.text
            start_index = html_content.find("<title>") + len("<title>")
            end_index = html_content.find("</title>")
            return html_content[start_index:end_index]
        else:
            st.error(f"Failed to fetch URL: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return None
