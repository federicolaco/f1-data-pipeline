import json
import requests
from src.config import BASE_URL, USER_AGENT, SEASON, RAW_DIR

def fetch_json(path: str, params: dict | None = None) -> dict:
  url = f"{BASE_URL}/{path}"
  response = requests.get(
    url,
    params=params,
    headers = {"User-Agent": USER_AGENT},
    timeout = 30,
  )
  response.raise_for_status()
  return response.json()

def fetch_all_pages(path: str, page_size: int = 100) -> list[dict]:
  pages = []
  offset = 0
  total = None
  while total is None or offset < total:
    payload = fetch_json(path, {"limit": page_size, "offset": offset})
    pages.append(payload)
    meta = payload["MRData"]
    total = int(meta["total"])
    offset += int(meta["limit"])
  return pages

def save_raw(name: str, payload: dict) -> None:
  RAW_DIR.mkdir(parents=True, exist_ok=True)
  target = RAW_DIR / f"{name}.json"
  target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
  print(target)

def main() -> None:
  endpoints = [
    ("drivers", f"{SEASON}/drivers.json"),
    ("constructors", f"{SEASON}/constructors.json"),
    ("circuits", f"{SEASON}/circuits.json"),
    ("races", f"{SEASON}/races.json"),
  ]
  for name, path in endpoints:
    payload = fetch_json(path)
    save_raw(f"{name}_{SEASON}", payload)
  pages = fetch_all_pages(f"{SEASON}/results.json")
  for page in pages:
    offset = page["MRData"]["offset"]
    save_raw(f"results_{SEASON}_offset_{offset}", page)

if __name__ == "__main__":
  main()