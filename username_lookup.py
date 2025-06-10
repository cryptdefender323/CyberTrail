from rich.console import Console
import requests
from Levenshtein import distance as levenshtein_distance

console = Console()

def run():
    console.print("[cyan]Enter the username to search:[/cyan]")
    username = input("> ").strip()

    try:
        platforms = {
            "Twitter": f"https://twitter.com/{username}", 
            "Instagram": f"https://instagram.com/{username}", 
            "Facebook": f"https://facebook.com/{username}", 
            "GitHub": f"https://github.com/{username}", 
        }

        results = {}
        for platform, url in platforms.items():
            response = requests.get(url)
            if response.status_code == 200:
                results[platform] = url
            else:
                results[platform] = "Not Found"

        aliases = detect_aliases(username, ["user123", "user_123", "user-123"])

        console.print("\n[yellow]Search Results:[/yellow]")
        for platform, result in results.items():
            console.print(f"[green]{platform}:[/green] {result}")
        console.print("\n[yellow]Possible Aliases:[/yellow]")
        console.print(", ".join(aliases) if aliases else "None")

    except Exception as e:
        console.print(f"[red]✘ Error searching username: {e}[/red]")

def detect_aliases(username, usernames_list):
    aliases = []
    for alias in usernames_list:
        if levenshtein_distance(username, alias) <= 3:
            aliases.append(alias)
    return aliases