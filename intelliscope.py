# intelliscope : IntelliScope is an advanced Python tool designed for offensive security practitioners. By leveraging Google Dorking techniques, it allows users to search for specific websites in a given country based on features like "bank," "e-commerce," or "hospital."
import time
import random
import pycountry
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from googlesearch import search
import os
import readline

if os.name == "posix":
   os.system('clear')
else:
   exit()

console = Console()

quotes = [
    "Hacking is not a crime. Ignorance is.",
    "Recon is the foundation of all successful attacks.",
    "You can't secure what you don't understand.",
    "Information is power — gather it wisely.",
    "Tools don’t hack people. People do."
]

def show_banner():
    banner = r"""
 █████╗ ███╗   ██╗████████╗████████╗██╗     ██╗███████╗ ██████╗ ██████╗ ███████╗
██╔══██╗████╗  ██║╚══██╔══╝╚══██╔══╝██║     ██║██╔════╝██╔════╝ ██╔══██╗██╔════╝
███████║██╔██╗ ██║   ██║      ██║   ██║     ██║█████╗  ██║  ███╗██████╔╝█████╗  
██╔══██║██║╚██╗██║   ██║      ██║   ██║     ██║██╔══╝  ██║   ██║██╔═══╝ ██╔══╝  
██║  ██║██║ ╚████║   ██║      ██║   ███████╗██║███████╗╚██████╔╝██║     ███████╗
╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚══════╝╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝
"""
    console.print(banner, style="bold green")
    console.print(f"[bold yellow italic]\"{random.choice(quotes)}\"[/bold yellow italic]", justify="center")
    console.print("\n")

def get_country_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2.lower() if country else None
    except:
        return None

def build_dork(country_code, feature):
    tlds = {
    "us": ".com",       # United States (commonly .com used for businesses)
    "ca": ".ca",        # Canada
    "ng": ".ng",        # Nigeria
    "uk": ".co.uk",     # United Kingdom
    "in": ".in",        # India
    "de": ".de",        # Germany
    "fr": ".fr",        # France
    "es": ".es",        # Spain
    "it": ".it",        # Italy
    "nl": ".nl",        # Netherlands
    "se": ".se",        # Sweden
    "no": ".no",        # Norway
    "fi": ".fi",        # Finland
    "dk": ".dk",        # Denmark
    "ru": ".ru",        # Russia
    "cn": ".cn",        # China
    "jp": ".jp",        # Japan
    "kr": ".kr",        # South Korea
    "au": ".com.au",    # Australia
    "nz": ".co.nz",     # New Zealand
    "br": ".com.br",    # Brazil
    "mx": ".com.mx",    # Mexico
    "za": ".co.za",     # South Africa
    "ae": ".ae",        # United Arab Emirates
    "sa": ".sa",        # Saudi Arabia
    "ke": ".ke",        # Kenya
    "gh": ".gh",        # Ghana
    "pk": ".pk",        # Pakistan
    "bd": ".bd",        # Bangladesh
    "sg": ".sg",        # Singapore
    "my": ".my",        # Malaysia
    "id": ".co.id",     # Indonesia
    "ph": ".ph",        # Philippines
    "tr": ".com.tr",    # Turkey
    "pl": ".pl",        # Poland
    "ch": ".ch",        # Switzerland
    "at": ".at",        # Austria
    "be": ".be",        # Belgium
    "ie": ".ie",        # Ireland
    "cz": ".cz",        # Czech Republic
    "gr": ".gr",        # Greece
    "ro": ".ro",        # Romania
    "il": ".co.il",     # Israel
    "th": ".co.th",     # Thailand
    "vn": ".vn",        # Vietnam
    "ar": ".com.ar",    # Argentina
    "cl": ".cl",        # Chile
    "co": ".com.co",    # Colombia
    "tn": ".tn"
}

    tld = tlds.get(country_code, ".com")
    dorks = {
    "bank": f"inurl:{tld} intitle:bank",
    "e-commerce": f"inurl:{tld} intitle:shop OR intitle:ecommerce",
    "hospital": f"inurl:{tld} intitle:hospital OR intitle:clinic",
    "school": f"inurl:{tld} intitle:school OR intitle:university OR intitle:college",
    "airport": f"inurl:{tld} intitle:airport OR intitle:airlines OR intitle:aviation",
    "government": f"inurl:{tld} site:.gov.{tld} OR intitle:government OR intitle:ministry",
    "telecom": f"inurl:{tld} intitle:telecom OR intitle:mobile OR intitle:network",
    "energy": f"inurl:{tld} intitle:energy OR intitle:power OR intitle:electric",
    "healthcare": f"inurl:{tld} intitle:healthcare OR intitle:medical OR intitle:clinic",
    "insurance": f"inurl:{tld} intitle:insurance OR intitle:policy OR intitle:cover",
    "university": f"inurl:{tld} intitle:university OR intitle:campus",
    "real estate": f"inurl:{tld} intitle:real estate OR intitle:property OR intitle:rent",
    "transport": f"inurl:{tld} intitle:transport OR intitle:logistics OR intitle:shipping",
    "finance": f"inurl:{tld} intitle:finance OR intitle:financial OR intitle:investment",
    "manufacturing": f"inurl:{tld} intitle:manufacturing OR intitle:factory OR intitle:industrial",
    "tourism": f"inurl:{tld} intitle:tourism OR intitle:travel OR intitle:holiday OR intitle:vacation"
}

    return dorks.get(feature, None)

def find_real_domains(country, feature):
    country_code = get_country_code(country)
    if not country_code:
        console.print(f"[red]Could not resolve country: {country}[/red]")
        return []

    dork_query = build_dork(country_code, feature)
    if not dork_query:
        console.print("[red]Invalid feature selected[/red]")
        return []

    console.print("[bold blue]Searching for results...[/bold blue]")
    time.sleep(1)

    try:
        results = list(search(dork_query,  lang="en", num_results=50))
        return results
    except Exception as e:
        console.print(f"[red]Error fetching data:[/red] {e}")
        return []


def display_results(results, feature, country):
    table = Table(title=f"[bold magenta]{feature.capitalize()} Websites ( {country} )[/bold magenta]", box=box.DOUBLE_EDGE)
    table.add_column("No.", justify="center", style="cyan", no_wrap=True)
    table.add_column("Website URL", style="green")

    for i, domain in enumerate(results, start=1):
        table.add_row(str(i), domain)

    console.print("\n")
    console.print(table)

def main():
    show_banner()
    country = Prompt.ask("🌍 Enter a country (e.g., Canada)")
    feature = Prompt.ask("🧠 Select a feature", choices=["bank", "e-commerce", "hospital", "school", "airport", "government", "telecom", "energy", "healthcare", "insurance", "univerisity", "real estate", "transport", "finance", "manufacturing", "tourism"], default="bank")

    results = find_real_domains(country, feature)

    if results:
        display_results(results, feature, country)
    else:
        console.print("[bold red]No websites found. Try another country or feature.[/bold red]")

    console.print("\n[bold green]Scan complete.[/bold green]")

if __name__ == "__main__":
    main()
