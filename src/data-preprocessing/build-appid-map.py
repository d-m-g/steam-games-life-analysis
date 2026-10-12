"""Build data/sullygnome/appid_map.csv: candidate links between SullyGnome Twitch categories and Steam appids.

Run from the repository root: python src/data-preprocessing/build-appid-map.py
"""
import pandas as pd, glob, re, os

# sullygnome games that normalise onto a DIFFERENT steam game -- verified by hand
BLOCK = {486, 1084, 60854, 562, 853}
# 486 "The Stanley Parable Mod", 1084 "eXperience 112", 60854 "Spelunky Classic",
# 562 FF III/VI naming clash, 853 "DOOM³"

SUP = str.maketrans("¹²³⁴⁵⁶⁷⁸⁹", "123456789")
def norm(s):
    s = str(s).translate(SUP).lower().replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "", s)

def has_ccu(appid):
    return any(os.path.exists(f"data/steam-games-dataset/{p}/{appid}.csv")
               for p in ("PlayerCountHistoryPart1", "PlayerCountHistoryPart2"))

steam = pd.read_csv("data/steam-games-dataset/applicationInformation.csv", encoding="cp1252")
sully = pd.concat([pd.read_csv(f) for f in glob.glob("data/sullygnome/monthly/*.csv")])
games = sully.groupby(["id", "name", "url"], as_index=False)["viewminutes"].sum()
games = games[~games["id"].isin(BLOCK)]

steam["k"] = steam["name"].map(norm)
cand = pd.concat([
    games.assign(k=games["url"].map(norm),  via="url"),
    games.assign(k=games["name"].map(norm), via="name"),
]).drop_duplicates(subset=["id", "k"])

m = steam.merge(cand, on="k", suffixes=("_steam", "_sully"))
m["prio"] = (m["via"] == "url").astype(int)     # slug match beats display-name match
m["ccu"]  = m["appid"].map(has_ccu)

# many appids -> one twitch category: slug match first, then has-CCU, then base (lowest) appid
m = m.sort_values(["prio", "ccu", "appid"], ascending=[False, False, True])
m = m.drop_duplicates(subset="id")

# one appid -> many twitch categories: keep all (duplicate categories, summed downstream)
mapping = (m[["appid", "name_steam", "id", "name_sully", "url", "via", "viewminutes"]]
             .rename(columns={"id": "sully_id"})
             .sort_values(["appid", "viewminutes"], ascending=[True, False])
             .reset_index(drop=True))

print(f"{mapping['appid'].nunique()} appids  <-  {len(mapping)} twitch categories")
print(f"appids fed by >1 category: {mapping['appid'].duplicated().sum()}")
mapping.to_csv("data/sullygnome/appid_map.csv", index=False)
