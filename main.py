import requests
import re
import ctypes
import os
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)
if os.name == "nt":
    os.system("mode con: cols=138 lines=30")


def logo():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print(
        f"""{Fore.LIGHTMAGENTA_EX}

                                ███████╗███████╗     ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗███████╗███████╗
                                ██╔════╝╚══███╔╝     ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝██║██╔════╝██╔════╝
                                █████╗    ███╔╝█████╗██████╔╝██████╔╝██║   ██║ ╚███╔╝ ██║█████╗  ███████╗
                                ██╔══╝   ███╔╝ ╚════╝██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗ ██║██╔══╝  ╚════██║
                                ███████╗███████╗     ██║     ██║  ██║╚██████╔╝██╔╝ ██╗██║███████╗███████║
                                ╚══════╝╚══════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
                                                    {Fore.LIGHTGREEN_EX}Scraping IpVanish Proxies has never been easier!

{Fore.RESET}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n
    """
    )


def proxie_scrap():
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(f"EzProxies | By Goldy")
    else:
        print(f"\33]0;EzProxies | By Goldy\a", end="", flush=True)

    logo()
    cookie = input(
        f"{Fore.LIGHTCYAN_EX}Please enter your Authentification Cookie.\n{Fore.RESET}~# "
    )

    logo()
    print(f"{Fore.LIGHTYELLOW_EX}Connecting...")

    accountpage = requests.get(
        "https://account.ipvanish.com/index.php", headers={"cookie": cookie}
    ).text
    if not "Log in to IPVanish Control Panel" in accountpage:
        email = re.findall('name="Email" value="(.+?)"', accountpage)[0]
        status = re.findall(
            'Account Status:</b></span>\n<span class="profile_label">(.+?)<',
            accountpage,
        )[0]
        plan = re.findall(
            'Current Plan:</b></span>\n<span class="profile_label">(.+?)<', accountpage
        )[0]
        renewaldate = re.findall(
            'Renewal Date:</b></span>\n<span class="profile_label">(.+?)<', accountpage
        )[0]
        renewaltype = re.findall(
            'Renewal Type:</b></span>\n<span class="profile_label">(.+?)<', accountpage
        )[0]
        renewalplan = re.findall(
            'Renewal Plan:</b></span>\n<span class="profile_label">(.+?)<', accountpage
        )[0]

        #Useless
        # paymentmethod = re.findall(
        #     'Payment Method:</b></span>\n<span class="profile_label"><i>(.+?)<',
        #     accountpage,
        # )[0]

        logo()
        print(
            f"{Fore.LIGHTCYAN_EX}{email}\n    Account Status - {status}\n    Current Plan - {plan}\n    Renewal Date - {renewaldate}\n    Renewal Type - {renewaltype}\n    Renewal Plan - {renewalplan}" #\n    Payment Method - {paymentmethod}
        )
        print(f"{Fore.LIGHTYELLOW_EX}\n\nScraping Proxies...")

        credentialspage = requests.get(
            "https://account.ipvanish.com/index.php?t=SOCKS5%20Proxy",
            headers={"cookie": cookie},
        ).text

        proxyusername = re.findall("Username:</b> (.+?)<", credentialspage)[0]
        proxypassword = re.findall("Password:</b> (.+?)<", credentialspage)[0]
        proxyport = re.findall("Port:</b> (.+?)<", credentialspage)[0]

        proxiespage = requests.get(
            "https://account.ipvanish.com/index.php?t=Server%20List",
            headers={"cookie": cookie},
        ).text
        proxies = re.findall(".*-.*.ipvanish.com", proxiespage)

        date = datetime.now().strftime("%d-%m-%Y %Hh%Mm%Ss")

        if not os.path.exists(f"scraped/{date}/"):
            os.makedirs(f"scraped/{date}/")

        for proxy in proxies:
            if (
                proxy
                != '                  <div class="why-vpn"><a href="https://www.ipvanish.com'
            ):
                with open(f"scraped/{date}/socks5.txt", "a") as file:
                    file.write(
                        proxy.replace('<td class="StatTDLabel">', "")
                        .replace("</td>", "")
                        .replace(" ", "")
                        + f":{proxyport}:{proxyusername}:{proxypassword}\n"
                    )
                    file.close()

        logo()
        print(
            f"{Fore.LIGHTCYAN_EX}{email}\n    Account Status - {status}\n    Current Plan - {plan}\n    Renewal Date - {renewaldate}\n    Renewal Type - {renewaltype}\n    Renewal Plan - {renewalplan}" #\n    Payment Method - {paymentmethod}
        )
        print(
            f"{Fore.LIGHTGREEN_EX}\n\n{len(proxies)} proxies have been scraped!\nSaved in scraped/{date}/"
        )
    else:
        logo()
        print(
            f"{Fore.LIGHTRED_EX}[ERROR] Unable to Connect to the Account. Please be sure that your Authentification Cookie is correct!"
        )


if __name__ == "__main__":
    try:
        proxie_scrap()
        input()
    except KeyboardInterrupt:
        exit()
