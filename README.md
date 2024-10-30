1. I scrapped the data via the python library pygithub, I queried the search_users api with `location:Delhi followers:>100` and sorted by followers. as i went through each user i extracted the data i needed and then queried all their repos. i then wrote this to 2 csv files.
2. I was suprised the fact Svelte has the highest avergae number of stars. I believe this is due to svelets realtive low amount of adoption and infancy meaning there are a higher amount of "high quality" repos
3. Developers looking to be hired should focus on a lower number of "high quality" repos as oppsed to creating a large amount of public repos.


# Reproducing
To reproduce the results you will need to have [uv](https://docs.astral.sh/uv/). You will need to have python 3.13 installed which can be done via `uv python install 3.13`. Next simply run `uv pip install -r pyproject.toml`. you can run `uv run python scripts/fetch_users.py` and `uv run python scripts/analyse.py`