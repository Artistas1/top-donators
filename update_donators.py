
import requests
import json
import datetime
import os

# Nustatymai
STREAMLABS_TOKEN = "1624F2174BE6EF4588320B3850566266EE9EE8456BC1A816B4C1BFA3697A9B79F15B13163FEFDCC82CC69777AF30E7E8E7FB4DFAECE81A36CB4AD59383B1BC4196E928C2740C79776F62719ADF3FA06199274F79A18BE6A6C0CCCA094F8037045531248D2E7FB2C5167CD68E7408EDB5F161C8DA8C300007099254ABC0"
GITHUB_REPO_PATH = "./top-donators"  # Lokaliai klonuotas GitHub Pages repo

# Gaunam donacijas
def get_donations():
    url = f"https://streamlabs.com/api/v1.0/donations?access_token={STREAMLABS_TOKEN}&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        donations = data["data"]
        return donations
    else:
        print("Klaida gaunant donacijas:", response.text)
        return []

# Top 10 donatoriai pagal sumą
def get_top_donators(donations):
    summary = {}
    for d in donations:
        name = d["name"]
        amount = float(d["amount"])
        summary[name] = summary.get(name, 0) + amount
    sorted_donators = sorted(summary.items(), key=lambda x: x[1], reverse=True)[:10]
    return [{"name": name, "total": total} for name, total in sorted_donators]

# Sukuriam HTML
def generate_html(top_donators):
    rows = "\n".join([f"<li>{d['name']}: ${d['total']:.2f}</li>" for d in top_donators])
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Top Donators</title>
  <style>
    body {{ font-family: Arial; background: #000; color: #fff; padding: 20px; }}
    h1 {{ font-size: 24px; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ font-size: 20px; margin-bottom: 5px; }}
  </style>
</head>
<body>
  <h1>Top Donators</h1>
  <ul>
    {rows}
  </ul>
  <p>Atnaujinta: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</body>
</html>
"""

# Įrašom į failą ir siunčiam į GitHub
def save_and_commit(html):
    index_path = os.path.join(GITHUB_REPO_PATH, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    os.system(f"cd {GITHUB_REPO_PATH} && git add . && git commit -m 'Update top donators' && git push")

def main():
    donations = get_donations()
    if donations:
        top_donators = get_top_donators(donations)
        html = generate_html(top_donators)
        save_and_commit(html)

if __name__ == "__main__":
    main()
