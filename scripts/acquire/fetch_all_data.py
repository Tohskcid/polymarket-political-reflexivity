#!/usr/bin/env python3
"""Acquire Polymarket price history and FiveThirtyEight polling data for 2024 US Presidential Election."""

import datetime
import hashlib
import json
import os
import socket
import ssl
import sys
import urllib.request
from pathlib import Path

# Setup DNS bypass for Taiwan/ISP blocking of polymarket.com
original_getaddrinfo = socket.getaddrinfo

def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if "polymarket.com" in host:
        return original_getaddrinfo("104.18.34.205", port, family, type, proto, flags)
    return original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = custom_getaddrinfo

CTX = ssl.create_default_context()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

SWING_STATES = {
    "PA": {
        "name": "Pennsylvania",
        "dem_token": "96404870680531697292788145333705429762370661278621665925868256650124167091957",
        "rep_token": "75951511934878014812323289513632732239356274541965522720897159608390126393735"
    },
    "MI": {
        "name": "Michigan",
        "dem_token": "67987395510317512691808452556846479650140447681921231570668523107587946046381",
        "rep_token": "105184348976114274990683066782141725521410345945023353024053078695238621958578"
    },
    "WI": {
        "name": "Wisconsin",
        "dem_token": "7374237615890526880478224649885278725219793468355446734533315746155037370158",
        "rep_token": "8506489790932625039746959405160059426243994232527626857062384302531008283468"
    },
    "GA": {
        "name": "Georgia",
        "dem_token": "71266923597682191255015907302921683041435419763570474059916757401212183782544",
        "rep_token": "10874846387975190407444713373765853114527145924436779240006871443341352408992"
    },
    "AZ": {
        "name": "Arizona",
        "dem_token": "77888176678720060596595785704561867851638990901352765132303721825934989281472",
        "rep_token": "64972410044896218211047269420581789917870192018252181026286744947120013986348"
    },
    "NV": {
        "name": "Nevada",
        "dem_token": "23452090462928163585257733383879365528898800849298930788345778676568194082451",
        "rep_token": "22811156622772246927379314532791131581149105511872861362055243423465705837015"
    },
    "NC": {
        "name": "North Carolina",
        "dem_token": "100038420537482572525556691531865148324318723289388392794253042393988283565188",
        "rep_token": "25474014705297439146444713942104010240322868585952420291288261803408266882449"
    }
}

NATIONAL_MARKETS = {
    "party_dem": "11015470973684177829729219287262166995141465048508201953575582100565462316088",
    "party_rep": "65444287174436666395099524416802980027579283433860283898747701594488689243696",
    "trump": "21742633143463906290569050155826241533067272736897614950488156847949938836455",
    "harris": "69236923620077691027083946871148646972011131466059644796654161903044970987404",
    "biden": "88027839609243624193415614179328679602612916497045596227438675518749602824929"
}

def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        return resp.read()

def fetch_history(token_id: str, fidelity: int = 1440) -> list:
    url = f"https://clob.polymarket.com/prices-history?market={token_id}&interval=all&fidelity={fidelity}"
    data = fetch_json(url)
    return data.get("history", [])

def main():
    root = Path(__file__).resolve().parent.parent.parent
    raw_dir = root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir = root / "literature" / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)

    print("1. Fetching Polymarket National daily price histories...")
    national_history = {}
    for key, token_id in NATIONAL_MARKETS.items():
        print(f"  Fetching {key} (token {token_id[:10]}...)...")
        hist = fetch_history(token_id, fidelity=1440)
        national_history[key] = hist
        print(f"    -> {len(hist)} points")

    national_path = raw_dir / "polymarket_national_daily.json"
    with open(national_path, "w", encoding="utf-8") as f:
        json.dump(national_history, f, indent=2)
    print(f"  Saved national price history to {national_path}")

    print("\n2. Fetching Polymarket Swing States daily price histories...")
    state_history = {}
    for st, info in SWING_STATES.items():
        print(f"  Fetching state {st} ({info['name']})...")
        dem_hist = fetch_history(info["dem_token"], fidelity=1440)
        rep_hist = fetch_history(info["rep_token"], fidelity=1440)
        state_history[st] = {
            "name": info["name"],
            "dem_history": dem_hist,
            "rep_history": rep_hist
        }
        print(f"    -> Dem: {len(dem_hist)} points, Rep: {len(rep_hist)} points")

    state_path = raw_dir / "polymarket_swing_states_daily.json"
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state_history, f, indent=2)
    print(f"  Saved swing states price history to {state_path}")

    print("\n3. Fetching FiveThirtyEight 2024 Presidential Polling Averages...")
    polls_url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/polls/2024-averages/presidential_general_averages_2024-09-12_uncorrected.csv"
    polls_bytes = fetch_bytes(polls_url)
    polls_path = raw_dir / "fivethirtyeight_polls_2024.csv"
    with open(polls_path, "wb") as f:
        f.write(polls_bytes)
    print(f"  Saved 538 polling data to {polls_path} ({len(polls_bytes)} bytes)")

    print("\n4. Generating Event and News Timeline Metadata...")
    events = [
        {"date": "2024-01-15", "event": "Iowa Caucuses", "type": "primary", "description": "Trump wins Iowa caucuses with 51% of vote."},
        {"date": "2024-03-05", "event": "Super Tuesday", "type": "primary", "description": "Trump sweeps Super Tuesday primaries; Haley suspends campaign on March 6."},
        {"date": "2024-05-30", "event": "Trump NY Verdict", "type": "legal", "description": "Jury finds Trump guilty on all 34 felony counts in Manhattan."},
        {"date": "2024-06-27", "event": "First Presidential Debate", "type": "debate", "description": "CNN Presidential Debate between Biden and Trump in Atlanta."},
        {"date": "2024-07-13", "event": "Trump Assassination Attempt", "type": "shock", "description": "Trump injured in shooting at campaign rally in Butler, PA."},
        {"date": "2024-07-15", "event": "Republican National Convention", "type": "convention", "description": "RNC convenes in Milwaukee; Vance announced as VP."},
        {"date": "2024-07-21", "event": "Biden Withdrawal & Endorsement", "type": "structural_change", "description": "Biden announces withdrawal from presidential race and endorses Harris."},
        {"date": "2024-08-19", "event": "Democratic National Convention", "type": "convention", "description": "DNC convenes in Chicago; Harris accepts presidential nomination."},
        {"date": "2024-09-10", "event": "Second Presidential Debate", "type": "debate", "description": "ABC News debate between Harris and Trump in Philadelphia."},
        {"date": "2024-10-05", "event": "Polymarket Whale Influx (Fredi9999/Théo)", "type": "market_microstructure", "description": "Four anonymous accounts (Fredi9999, Theo4, PrincessCaro, Michie) begin massive Trump bet accumulation ($30M+)."},
        {"date": "2024-11-05", "event": "Election Day", "type": "election", "description": "2024 United States Presidential Election polls close."}
    ]
    events_path = raw_dir / "campaign_shocks_timeline.json"
    with open(events_path, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)
    print(f"  Saved political event timeline to {events_path}")

    # Generate Checksums file
    print("\n5. Computing SHA-256 Checksums for data/raw/...")
    checksums = {}
    for p in [national_path, state_path, polls_path, events_path]:
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        checksums[p.name] = h
        print(f"  {p.name}: {h}")

    checksums_path = raw_dir / "checksums.sha256"
    with open(checksums_path, "w", encoding="utf-8") as f:
        for fname, h in checksums.items():
            f.write(f"{h}  {fname}\n")
    print(f"  Saved SHA-256 manifest to {checksums_path}")

if __name__ == "__main__":
    main()
