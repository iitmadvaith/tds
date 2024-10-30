import csv
from os import environ

from dotenv import load_dotenv
from github import Auth, Github
from local_types import RepoDetails, UserDetails
from rich.console import Console

_ = load_dotenv()
PAT = environ.get("PAT")
if not PAT:
    print("pat was not set")
    exit(1)


auth = Auth.Token(PAT)
users: list[UserDetails] = []
repos: list[RepoDetails] = []

g = Github(auth=auth)

search = g.search_users(query="location:Delhi followers:>100", sort="followers")
console = Console()
user_details: UserDetails | None = None
repo_data: RepoDetails | None = None
for user in search:
    company = None
    if user.company:
        company = user.company.strip().strip("@").upper()
    user_details = {
        "login": user.login,
        "name": user.name,
        "company": company,
        "location": user.location,
        "email": user.email,
        "hireable": user.hireable if user.hireable else False,
        "bio": user.bio.replace("\n", "").replace("\r", "") if user.bio else "",
        "public_repos": user.public_repos,
        "followers": user.followers,
        "following": user.following,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    repo_num = 0
    with console.status(f"Fetching repos for {user.login}") as status:
        for repo in user.get_repos():
            repo_data = {
                "login": user.login,
                "full_name": repo.full_name,
                "created_at": repo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "stargazers_count": repo.stargazers_count,
                "watchers_count": repo.watchers_count,
                "language": repo.language,
                "has_projects": repo.has_projects,
                "has_wiki": repo.has_wiki,
                "license_name": repo.license.key if repo.license else "None",
            }
            repos.append(repo_data)
            if repo_num >= 500:
                break
            else:
                repo_num += 1

    users.append(user_details)

if user_details and repo_data:
    with open("users.csv", "w") as file:
        w = csv.DictWriter(file, user_details.keys())
        w.writeheader()
        w.writerows(users)

    with open("repositories.csv", "w") as file:
        w = csv.DictWriter(file, repo_data.keys())
        w.writeheader()
        w.writerows(repos)
