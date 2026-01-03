import requests

def analyze_github_repo(owner, repo):
    try:
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}")
        if response.status_code == 200:
            data = response.json()
            repo_data = {
                "Name": data['name'],
                "Owner": data['owner']['login'],
                "Stars": data['stargazers_count'],
                "Forks": data['forks_count'],
                "Language": data['language'],
                "Description": data['description'],
            }
            return repo_data
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
