#!/usr/bin/env python3

from rich.console import Console
from rich.prompt import Prompt
import os
from modules import (
    metadata_extractor,
    reverse_image_search,
    ip_domain_lookup,
    people_search,
    username_lookup,
    darkweb_search,  
)

console = Console()

def pause_return():
    try:
        input("\n[bold blue]→ Tekan ENTER untuk kembali ke menu utama...[/bold blue]")
    except:
        pass
    clear_screen()
    show_banner()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner():
    banner = r"""
 ██████╗ ██████╗ ██╗   ██╗██████╗ ████████╗██╗  ██╗ ██████╗ ██████╗ ███╗   ███╗
██╔════╝ ██╔══██╗██║   ██║██╔══██╗╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗████╗ ████║
██║  ███╗██████╔╝██║   ██║██████╔╝   ██║   ███████║██║   ██║██████╔╝██╔████╔██║
██║   ██║██╔═══╝ ██║   ██║██╔═══╝    ██║   ██╔══██║██║   ██║██╔═══╝ ██║╚██╔╝██║
╚██████╔╝██║     ╚██████╔╝██║        ██║   ██║  ██║╚██████╔╝██║     ██║ ╚═╝ ██║
 ╚═════╝ ╚═╝      ╚═════╝ ╚═╝        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝     ╚═╝
                            CryptDefender V1 • OSINT TOOLS
    """
    console.print(banner, style="bold green")
    console.print("[italic cyan]Created By: CryptDefender[/italic cyan]\n")

def show_menu():
    console.print("\n[bold cyan]:: CryptDefender | SELECT A MODULE ::[/bold cyan]")
    console.print("[1] Metadata Extractor with Threat Analysis")
    console.print("[2] Deep Reverse Image Search")
    console.print("[3] Advanced IP/Domain Intel Lookup")
    console.print("[4] People Search Aggregator")
    console.print("[5] Username Search Aggregator")
    console.print("[6] Dark Web Search")
    console.print("[99] Exit")

def run_module(name, func):
    try:
        console.print(f"[yellow]↪ Menjalankan {name}... (Tekan Ctrl+C untuk membatalkan)[/yellow]")
        func()
    except KeyboardInterrupt:
        console.print(f"\n[red]❌ {name} dibatalkan oleh pengguna.[/red]")
    except Exception as e:
        console.print(f"[red]✘ Terjadi error dalam modul {name}: {e}[/red]")
    finally:
        pause_return()

def main():
    os.makedirs("logs", exist_ok=True)
    while True:
        try:
            clear_screen()
            show_banner()
            show_menu()
            choice = Prompt.ask("\n[bold green]crypthecom>[/bold green]", default="00")

            if choice == "1":
                run_module("Metadata Extractor", metadata_extractor.run)
            elif choice == "2":
                run_module("Reverse Image Search", reverse_image_search.run)
            elif choice == "3":
                run_module("IP/Domain Intel Lookup", ip_domain_lookup.run)
            elif choice == "4":
                run_module("People Search Aggregator", people_search.run)
            elif choice == "5":
                run_module("Username Search Aggregator", username_lookup.run)
            elif choice == "6":
                run_module("Dark Web Search", darkweb_search.run)
            elif choice == "99":
                console.print("[bold red]Keluar dari CryptDefender. Sampai jumpa![/bold red]")
                break
            else:
                console.print("[yellow]✘ Input tidak valid. Pilih angka dari 1 hingga 6.[/yellow]")
                pause_return()

        except KeyboardInterrupt:
            continue

if __name__ == "__main__":
    main()
