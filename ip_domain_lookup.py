from rich.console import Console
import requests
import json
import os
from datetime import datetime
import folium
import csv
import pdfkit
from cryptography.fernet import Fernet
import schedule
import time

console = Console()

ABUSEIPDB_API_KEY = "enter your API key"
VIRUSTOTAL_API_KEY = "enter your API key"
SHODAN_API_KEY = "enter your API key"
SECURITYTRAILS_API_KEY = "enter your API key"

def run():
    console.print("[cyan]Enter the IP/Domain to analyze:[/cyan]")
    target = input("> ").strip()

    if not target:
        console.print("[red]✘ Target cannot be empty.[/red]")
        return

    try:
        console.print(f"\n[yellow]Analyzing {target}...[/yellow]")
        results = {}

        whois_data = whois_lookup(target)
        results["whois"] = whois_data

        dns_records = dns_lookup(target)
        results["dns_records"] = dns_records

        abuseipdb_data = abuseipdb_check(target)
        results["abuseipdb"] = abuseipdb_data

        virustotal_data = virustotal_analysis(target)
        results["virustotal"] = virustotal_data

        shodan_data = shodan_analysis(target)
        results["shodan"] = shodan_data

        securitytrails_data = securitytrails_analysis(target)
        results["securitytrails"] = securitytrails_data

        historical_data = wayback_machine_analysis(target)
        results["historical"] = historical_data

        geolocation_mapping(abuseipdb_data.get("data", {}))

        save_results(results, target)

        display_results(results)

        export_results(results, target)

        real_time_updates(target)

    except Exception as e:
        console.print(f"[red]✘ Error analyzing IP/Domain: {e}[/red]")

def whois_lookup(target):
    console.print("[cyan]Performing WHOIS lookup...[/cyan]")
    try:
        response = requests.get(f"https://api.securitytrails.com/v1/domain/{target}",  headers={"APIKEY": SECURITYTRAILS_API_KEY})
        data = response.json()
        return data
    except Exception as e:
        console.print("[red]✘ WHOIS lookup failed.[/red]")
        return {"error": str(e)}

def dns_lookup(target):
    console.print("[cyan]Performing DNS records analysis...[/cyan]")
    try:
        response = requests.get(f"https://api.securitytrails.com/v1/dns/{target}/records",  headers={"APIKEY": SECURITYTRAILS_API_KEY})
        data = response.json()
        return data
    except Exception as e:
        console.print("[red]✘ DNS lookup failed.[/red]")
        return {"error": str(e)}

def abuseipdb_check(target):
    console.print("[cyan]Checking status...[/cyan]")
    try:
        response = requests.get(
            f"https://api.abuseipdb.com/api/v2/check?ipAddress={target}",
            headers={"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
        )
        data = response.json()
        return data
    except Exception as e:
        console.print("[red]✘ check failed.[/red]")
        return {"error": str(e)}

def virustotal_analysis(target):
    console.print("[cyan]Performing analysis...[/cyan]")
    try:
        response = requests.get(
            f"https://www.virustotal.com/api/v3/domains/{target}",
            headers={"x-apikey": VIRUSTOTAL_API_KEY}
        )
        data = response.json()
        return data
    except Exception as e:
        console.print("[red]✘ analysis failed.[/red]")
        return {"error": str(e)}

def shodan_analysis(target):
    console.print("[cyan]Performing analysis...[/cyan]")
    try:
        response = requests.get(
            f"https://api.shodan.io/shodan/host/{target}?key={SHODAN_API_KEY}"
        )
        data = response.json()
        return data
    except Exception as e:
        console.print("[red]✘ analysis failed.[/red]")
        return {"error": str(e)}

def securitytrails_analysis(target):
    console.print("[cyan]Performing analysis...[/cyan]")
    try:
        response = requests.get(
            f"https://api.securitytrails.com/v1/domain/{target}/subdomains",
            headers={"APIKEY": SECURITYTRAILS_API_KEY}
        )
        data = response.json()
        return data
    except Exception as e:
        console.print("[red]✘ analysis failed.[/red]")
        return {"error": str(e)}

def wayback_machine_analysis(target):
    console.print("[cyan]Performing analysis (Wayback Machine)...[/cyan]")
    try:
        response = requests.get(f"http://archive.org/wayback/available?url={target}")
        data = response.json()
        return data
    except Exception as e:
        console.print("[red]✘ Historical analysis failed.[/red]")
        return {"error": str(e)}

def geolocation_mapping(ip_data):
    console.print("[cyan]Generating geolocation map...[/cyan]")
    try:
        lat = ip_data.get("latitude")
        lon = ip_data.get("longitude")

        if lat and lon:
            map_obj = folium.Map(location=[lat, lon], zoom_start=10)
            folium.Marker([lat, lon], popup="Target Location").add_to(map_obj)

            map_file = f"logs/geolocation_map_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
            os.makedirs("logs", exist_ok=True)
            map_obj.save(map_file)
            console.print(f"[green]✓ Geolocation map saved to {map_file}[/green]")
        else:
            console.print("[yellow]ⓘ Latitude and longitude not found.[/yellow]")
    except Exception as e:
        console.print(f"[red]✘ Error generating geolocation map: {e}[/red]")

def save_results(results, target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/{target}_analysis_{timestamp}.json"
    os.makedirs("logs", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
    console.print(f"[green]✓ Results saved to {filename}[/green]")

def display_results(results):
    console.print("\n[yellow]Analysis Results:[/yellow]")
    for key, value in results.items():
        console.print(f"[bold green]{key.upper()}:[/bold green]")
        console.print(json.dumps(value, indent=4))

def export_to_csv(results, target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/{target}_analysis_{timestamp}.csv"
    os.makedirs("logs", exist_ok=True)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Key", "Value"])
        for key, value in results.items():
            writer.writerow([key, json.dumps(value)])

    console.print(f"[green]✓ Results exported to {filename}[/green]")

def export_to_pdf(results, target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    html_content = "<h1>Analysis Results</h1><pre>" + json.dumps(results, indent=4) + "</pre>"
    filename = f"logs/{target}_analysis_{timestamp}.pdf"
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
    filename = f"logs/{target}_encrypted_log_{timestamp}.bin"
    os.makedirs("logs", exist_ok=True)

    key = Fernet.generate_key()
    encrypted_data = encrypt_log(json.dumps(data), key)

    with open(filename, "wb") as f:
        f.write(encrypted_data)

    console.print(f"[green]✓ Encrypted log saved to {filename}[/green]")
    console.print(f"[yellow]Encryption Key:[/yellow] {key.decode()}")

def real_time_updates(target):
    console.print("[cyan]Starting real-time updates... (Press Ctrl+C to stop)[/cyan]")
    try:
        def update():
            console.print("\n[yellow]Fetching new data...[/yellow]")
            results = {
                "abuseipdb": abuseipdb_check(target),
                "virustotal": virustotal_analysis(target),
                "shodan": shodan_analysis(target),
                "securitytrails": securitytrails_analysis(target),
                "historical": wayback_machine_analysis(target)
            }
            console.print("[green]✓ Real-time update completed.[/green]")
            display_results(results)

        schedule.every(60).seconds.do(update)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[red]Stopping real-time updates.[/red]")

if __name__ == "__main__":
    run()
