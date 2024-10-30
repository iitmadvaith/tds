import pandas as pd
from rich import print
from scipy import stats

df_user = pd.read_csv("users.csv")
df_repos = pd.read_csv("repositories.csv")

df_user["created_at"] = pd.to_datetime(df_user["created_at"])
df_repos["created_at"] = pd.to_datetime(df_repos["created_at"])

df_user = df_user.sort_values(by="followers", ascending=False)
print(
    f"[bold green]top 5 users:[/bold green] [bold red]{','.join(df_user.head()['login'])}[/bold red]"
)

df_user.reset_index(drop=True, inplace=True)

df_user = df_user.sort_values(by="created_at")

print(
    f"[bold green]earlist users:[/bold green] [bold red]{','.join(df_user.head()['login'])}[/bold red]"
)
df_user.reset_index(drop=True, inplace=True)

print(
    f"[bold green]top license:[/bold green] [bold red]{','.join(df_repos["license_name"].value_counts().nlargest(3).index.to_list())}[/bold red]"
)

print(
    f"[bold green]top company:[/bold green] [bold red]{''.join(df_user["company"].value_counts().nlargest(1).index.to_list())}[/bold red]"
)

print(
    f"[bold green]top lang:[/bold green] [bold red]{''.join(df_repos["language"].value_counts().nlargest(1).index.to_list())}[/bold red]"
)


filtered_user_df = df_user[df_user["created_at"].dt.year > 2020]
filtered_repos = df_repos[df_repos["login"].isin(filtered_user_df["login"].to_list())]

print(
    f"[bold green]top lang for users created after 2020:[/bold green] [bold red]{''.join(filtered_repos["language"].value_counts().head(1).index.to_list())}[/bold red]"
)
# TODO: REWRITE TO USE GROUP BY
langs: dict[str, dict[str, int]] = {}
highest = ("nan", 0.0)

for _, repo in df_repos.iterrows():
    if not pd.isna(repo["language"]):
        langinfo = {}
        if langs.get(repo["language"]):
            langinfo = langs[repo["language"]]
            langinfo["stars"] += repo["stargazers_count"]
            langinfo["repos"] += 1
        else:
            langinfo["stars"] = repo["stargazers_count"]
            langinfo["repos"] = 1

        langs[repo["language"]] = langinfo

for lang in langs:
    if highest == ():
        data = langs[lang]
        avg = data["stars"] / data["repos"]
        highest = (lang, avg)
    else:
        data = langs[lang]
        avg = data["stars"] / data["repos"]
        if highest[1] < avg:
            highest = (lang, avg)

print(
    f"[bold green]the best lang for stars is:[/bold green] [bold red]{highest[0]}[/bold red]"
)

df_user_leader = df_user
df_user_leader["leader_strength"] = df_user_leader["followers"] / (
    1 + df_user_leader["following"]
)
df_user_leader = df_user_leader.sort_values(by="leader_strength", ascending=False)

print(
    f"[bold green]leader streangth users:[/bold green] [bold red]{','.join(df_user_leader.head()['login'])}[/bold red]"
)

print(df_user[["followers", "public_repos"]].corr())

slope, _, _, _, _ = stats.linregress(df_user["followers"], df_user["public_repos"])
print(
    f"[bold green]Regression slope of followers on repos:[/bold green] [bold red]{slope}[/bold red]"
)

print(df_repos[["has_projects", "has_wiki"]].corr())

avg_users = df_user["following"].mean()

filtered_user_df = df_user[df_user["hireable"] == True]
avg_users_hireable = filtered_user_df["following"].mean()
print(
    f"[bold green]do hireable users have emails:[/bold green] [bold red]{avg_users_hireable - avg_users}[/bold red]"
)

df_user["word_count"] = df_user["bio"].str.split().str.len()
filtered_user_df = df_user.fillna(0)

slope, _, _, _, _ = stats.linregress(
    filtered_user_df["followers"], filtered_user_df["word_count"]
)
print(
    f"[bold green]Regression slope of followers on bio word count[/bold green]: [bold red]{slope}[/bold red]"
)

weekend_df = df_repos[df_repos["created_at"].dt.day_of_week > 5]
print(",".join(weekend_df["login"].value_counts().nlargest(5).index.to_list()))

filtered_user_df = df_user[df_user["hireable"] == True]

print(filtered_user_df["email"].count() / df_user["email"].count())
df_user["surname"] = df_user["name"].str.split().str[-1]
print(",".join(df_user["surname"].value_counts().nlargest(1).index.to_list()))
