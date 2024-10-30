from typing import TypedDict


class UserDetails(TypedDict):
    login: str
    name: str | None
    company: str | None
    location: str | None
    email: str | None
    hireable: bool
    bio: str | None
    public_repos: int
    followers: int
    following: int
    created_at: str

class RepoDetails(TypedDict):
    login: str
    full_name: str
    created_at: str
    stargazers_count: int
    watchers_count: int
    language: str
    has_projects: bool
    has_wiki: bool
    license_name: str
