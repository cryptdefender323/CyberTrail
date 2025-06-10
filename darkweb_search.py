from rich.console import Console
import requests
import json
import os
from datetime import datetime
import csv
import pdfkit
from cryptography.fernet import Fernet
from stem import Signal
from stem.control import Controller

console = Console()

TOR_PROXY = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}

def run():
    console.print("[cyan]Enter the target (IP/Domain/Keyword) to search on the dark web:[/cyan]")
    target = input("> ").strip()

    if not target:
        console.print("[red]✘ Target cannot be empty.[/red]")
        return

    try:
        console.print(f"\n[yellow]Searching for {target} on the dark web...[/yellow]")
        results = {}

        dark_web_data = advanced_dark_web_search(target)
        results["dark_web"] = dark_web_data

        save_results(results, target)

        display_results(results)

        export_results(results, target)

    except Exception as e:
        console.print(f"[red]✘ Error searching the dark web: {e}[/red]")

def renew_tor_identity():
    """Renew Tor identity to get a new IP address."""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="your_password")
        controller.signal(Signal.NEWNYM)

def advanced_dark_web_search(target):
    console.print("[cyan]Performing advanced dark web search...[/cyan]")
    try:
        dark_web_platforms = {
            "Dread": f"http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/search?q={target}",
            "0xchan": f"http://7ccvmu6zrnf62qgo.onion/search.php?search={target}",
            "Dark.Fail": f"http://darkfailllnkf4vf.onion/list?query={target}",
            "Recon": f"http://reconmnwgeip27t3.onion/search?query={target}",
            "Toxbin": f"http://toxbin2brzg52wpe.onion/paste/{target}",
            "DeepPaste": f"http://deeppastexyguz3xi.onion/paste/{target}",
            "BreachForums": f"http://breachforumsrevived.onion/search?q={target}",
        }

        results = {}
        for platform, url in dark_web_platforms.items():
            console.print(f"[cyan]Searching on {platform}...[/cyan]")
            renew_tor_identity()
            try:
                response = requests.get(url, proxies=TOR_PROXY, timeout=30)
                if response.status_code == 200:
                    results[platform] = {"status": "Found", "url": url, "content": response.text[:500]}
                else:
                    results[platform] = {"status": "Not Found", "url": url}
            except Exception as e:
                results[platform] = {"status": "Error", "url": url, "error": str(e)}
        return results
    except Exception as e:
        console.print("[red]✘ Advanced dark web search failed.[/red]")
        return {"error": str(e)}

def save_results(results, target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/{target}_darkweb_analysis_{timestamp}.json"
    os.makedirs("logs", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
    console.print(f"[green]✓ Results saved to {filename}[/green]")

def display_results(results):
    console.print("\n[yellow]Dark Web Search Results:[/yellow]")
    for key, value in results.items():
        console.print(f"[bold green]{key.upper()}:[/bold green]")
        console.print(json.dumps(value, indent=4))

def export_to_csv(results, target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/{target}_darkweb_analysis_{timestamp}.csv"
    os.makedirs("logs", exist_ok=True)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Platform", "Status", "URL", "Content/Error"])
        for platform, data in results.items():
            writer.writerow([platform, data.get("status"), data.get("url"), data.get("content", data.get("error"))])

    console.print(f"[green]✓ Results exported to {filename}[/green]")

def export_to_pdf(results, target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    html_content = "<h1>Dark Web Search Results</h1><pre>" + json.dumps(results, indent=4) + "</pre>"
    filename = f"logs/{target}_darkweb_analysis_{timestamp}.pdf"
    os.makedirs("logs", exist_ok=True)

    pdfkit.from_string(html_content, filename)
    console.print(f"[green]✓ Results exported to {filename}[/green]")

def export_results(results, target):
    console.print("[cyan]Do you want to export results? (y/n):[/cyan]")
    if input().lower() == "y":
        console.print("[cyan]Export to CSV or PDF? (csv/pdf):[/cyan]")
        choice = input().lower()
        if choice == "csv":
            export_to_csv(results, target)
        elif choice == "pdf":
            export_to_pdf(results, target)

def encrypt_log(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def save_encrypted_log(data, target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/{target}_encrypted_darkweb_log_{timestamp}.bin"
    os.makedirs("logs", exist_ok=True)

    key = Fernet.generate_key()
    encrypted_data = encrypt_log(json.dumps(data), key)

    with open(filename, "wb") as f:
        f.write(encrypted_data)

    console.print(f"[green]✓ Encrypted log saved to {filename}[/green]")
    console.print(f"[yellow]Encryption Key:[/yellow] {key.decode()}")

if __name__ == "__main__":
    run()