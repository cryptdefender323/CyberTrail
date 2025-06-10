from PIL import Image
from PIL.ExifTags import TAGS
from rich.console import Console
import os

console = Console()

def extract_metadata(file_path):
    console.print("[cyan]Extracting metadata from file...[/cyan]")
    if not os.path.exists(file_path):
        console.print("[red]✘ File not found.[/red]")
        return None

    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        
        if not exif_data:
            console.print("[yellow]ⓘ No metadata found in the file.[/yellow]")
            return {}

        metadata = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            metadata[tag] = value

        return metadata

    except Exception as e:
        console.print("[red]✘ Metadata extraction failed.[/red]")
        return {"error": str(e)}

def run():
    console.print("[cyan]Enter the path to the file for metadata analysis:[/cyan]")
    file_path = input("> ").strip()

    if os.path.exists(file_path):
        metadata_data = extract_metadata(file_path)
        console.print("\n[yellow]Metadata Results:[/yellow]")
        console.print(metadata_data)
    else:
        console.print("[red]✘ File not found.[/red]")