import requests
from rich.console import Console
from bs4 import BeautifulSoup
import random

console = Console()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
]

def get_random_user_agent():
    """
    Return a random User-Agent from the list.
    """
    return random.choice(USER_AGENTS)

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": get_random_user_agent()}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for result in soup.select(".tF2Cxc"):
                title = result.select_one(".LC20lb").text.strip()
                link = result.select_one("a")["href"]
                snippet = result.select_one(".VwiC3b").text.strip() if result.select_one(".VwiC3b") else ""
                results.append({"name": title, "username": link, "snippet": snippet})
            return {"status": "success", "data": results}
        else:
            return {"status": "error", "message": "Failed to fetch data from Google."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_linkedin(query):
    url = f"https://www.linkedin.com/search/results/people/?keywords={query}"
    headers = {"User-Agent": get_random_user_agent()}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for person in soup.select(".entity-result__content"):
                name = person.select_one(".entity-result__title-text").text.strip()
                username = person.select_one("a")["href"]
                results.append({"name": name, "username": username})
            return {"status": "success", "data": results}
        else:
            return {"status": "error", "message": "Failed to fetch data from LinkedIn."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_twitter(query):
    url = f"https://nitter.net/search?f=users&q={query}"
    headers = {"User-Agent": get_random_user_agent()}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for user in soup.select(".timeline-item"):
                username = user.select_one(".username").text.strip()
                full_name = user.select_one(".fullname").text.strip() if user.select_one(".fullname") else ""
                results.append({"name": full_name, "username": username})
            return {"status": "success", "data": results}
        else:
            return {"status": "error", "message": "Failed to fetch data from Twitter."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_instagram(query):
    url = f"https://www.instagram.com/web/search/topsearch/?query={query}"
    headers = {"User-Agent": get_random_user_agent()}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = [{"name": user["user"]["full_name"], "username": user["user"]["username"]} for user in data.get("users", [])]
            return {"status": "success", "data": results}
        else:
            return {"status": "error", "message": "Failed to fetch data from Instagram."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run():
    console.print("[cyan]Enter the name to search:[/cyan]")
    query = input("> ").strip()

    if not query:
        console.print("[red]✘ Name cannot be empty.[/red]")
        return

    results = {}
    try:
        google_results = search_google(query)
        results["Google"] = google_results

        linkedin_results = search_linkedin(query)
        results["LinkedIn"] = linkedin_results

        twitter_results = search_twitter(query)
        results["Twitter"] = twitter_results

        instagram_results = search_instagram(query)
        results["Instagram"] = instagram_results

        console.print("\n[yellow]Search Results:[/yellow]")
        for platform, result in results.items():
            if result.get("status") == "success":
                console.print(f"[green]{platform}:[/green]")
                for person in result["data"]:
                    console.print(f"  - {person['name']} ({person['username']})")
            else:
                console.print(f"[red]{platform}:[/red] {result['message']}")

    except Exception as e:
        console.print(f"[red]✘ Error during search: {e}[/red]")

if __name__ == "__main__":
    run()