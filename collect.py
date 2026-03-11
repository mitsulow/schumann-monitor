"""
SchumannResonanceLive API → CSV蓄積スクリプト
GitHub Actionsで15分ごとに実行
"""
import csv
import json
import os
import sys
from datetime import datetime, timezone, timedelta

import requests

API_URL = "https://schumannresonancelive.com/schumann_api.php?action=current&lang=en"
CSV_PATH = "data/schumann_log.csv"
JST = timezone(timedelta(hours=9))

HEADERS = [
    "timestamp_utc",
    "timestamp_jst",
    "sr1_freq", "sr1_amp", "sr1_peak", "sr1_power", "sr1_trend",
    "sr2_freq", "sr2_amp", "sr2_peak", "sr2_power", "sr2_trend",
    "sr3_freq", "sr3_amp", "sr3_peak", "sr3_power", "sr3_trend",
    "sr4_freq", "sr4_amp", "sr4_peak", "sr4_power", "sr4_trend",
    "sr5_freq", "sr5_amp", "sr5_peak", "sr5_power", "sr5_trend",
    "signal_strength", "snr", "noise_level", "quality_score", "stability",
    "main_frequency", "total_power", "average_amplitude"
]

def fetch_data():
    """APIからデータを取得"""
    try:
        resp = requests.get(API_URL, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] API fetch failed: {e}", file=sys.stderr)
        return None

def parse_data(raw):
    """APIレスポンスをCSV行に変換"""
    now_utc = datetime.now(timezone.utc)
    now_jst = now_utc.astimezone(JST)

    row = {
        "timestamp_utc": now_utc.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp_jst": now_jst.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # 各モード (SR1〜SR5)
    for f in raw.get("frequencies", []):
        fid = f["id"].lower()  # sr1, sr2, ...
        row[f"{fid}_freq"] = f.get("frequency", "")
        row[f"{fid}_amp"] = f.get("amplitude", "")
        row[f"{fid}_peak"] = f.get("peak", "")
        row[f"{fid}_power"] = f.get("power", "")
        row[f"{fid}_trend"] = f.get("trend", "")

    # 品質情報
    q = raw.get("quality", {})
    row["signal_strength"] = q.get("signal_strength", "")
    row["snr"] = q.get("snr", "")
    row["noise_level"] = q.get("noise_level", "")
    row["quality_score"] = q.get("quality_score", "")
    row["stability"] = q.get("stability", "")

    # 統計情報
    s = raw.get("statistics", {})
    row["main_frequency"] = raw.get("main_frequency", "")
    row["total_power"] = s.get("total_power", "")
    row["average_amplitude"] = s.get("average_amplitude", "")

    return row

def append_csv(row):
    """CSVに1行追記（ファイルがなければヘッダー付きで作成）"""
    file_exists = os.path.exists(CSV_PATH)

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Fetching Schumann data...")
    raw = fetch_data()
    if raw is None:
        sys.exit(1)

    row = parse_data(raw)
    append_csv(row)

    # 取得結果を表示
    print(f"  SR1={row['sr1_freq']}Hz  SR2={row['sr2_freq']}Hz  "
          f"SR3={row['sr3_freq']}Hz  SR4={row['sr4_freq']}Hz  SR5={row['sr5_freq']}Hz")
    print(f"  Signal={row['signal_strength']}  SNR={row['snr']}  Quality={row['quality_score']}")

    # CSVの行数を表示
    with open(CSV_PATH, "r") as f:
        lines = sum(1 for _ in f) - 1  # ヘッダー除く
    print(f"  Total records: {lines}")

if __name__ == "__main__":
    main()
