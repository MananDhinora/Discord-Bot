import discord
import json
from bs4 import BeautifulSoup
import requests


# Constants
def constants(credential):
    with open("env.json") as env:
        credentials = json.load(env)
        return credentials[credential]


# Discord Client init
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_fitgirl_link(url):
    """
    New method to scrape the magnet link for all the articles found
    """
    for tag in link:
        name = tag.text.strip()
        article_url = tag.get("href")
        searched_page = requests.get(article_url)
        searched_soup = BeautifulSoup(searched_page.text, features="html.parser")
        search_magnet_link = searched_soup.find_all(
            "a", href=lambda href: href and href.startswith("magnet:?xt=urn")
        )
        try:
            magnet_link = search_magnet_link[0]["href"]
        except IndentationError:
            magnet_link = "No magnet link was found."

        return f"**{name}** \nArticle: {article_url} \n**Magnet Link**: \n{magnet_link}"

def get_onlinefix_link(url):
    """
    New method to scrape the torrent file from online-fix
    """
    page = requests.get(url, headers=os.getenv("MULTI_PLAYER_HEADERS"))
    soup = BeautifulSoup(page.txt, features="html.parser")
    print(soup)


async def search_fitgirl(message):
    """
    New method to search the message on fitgirl
    """
    search_word = message.content[8:]
    search_url = os.getenv("SINGLE_PLAYER_URL")
    # creating the search url that is to be scrapped for the required urls
    if " " in search_word:
        search_word.replace(" ", "+")
    search_url = search_url + search_word
    try:
        page = requests.get(search_url)
    except Exception:
        await message.channel.send("An error has occured, please try again")
    soup = BeautifulSoup(page.text, features="html.parser")
    # getting every article with the class entry-title as that class is used to display
    # every article that is relative to our serch query
    for link in soup.find_all("h1", class_="entry-title"):
        # sending a new message every time due to the 2000 char per message limit in discord
        await message.channel.send(get_link(link))
    await message.channel.send("Above are the search results you asked for.")


async def search_onlinefix(message):
    """
    New method to search on online-fix
    """
    search_word = message.content[8:]
    # creating the search url that is to be scrapped for the required urls
    if " " in search_word:
        search_url = search_url + search_word.replace(" ", "+")
    # url = "https://online-fix.me"
    page = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(page.text, features="html.parser")
    links = soup.find_all("h2")
    for h2 in links:
        if h2.parent.name == "a":
            get_onlinefix_link(h2.parent["href"])

# Discord events
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith("!help"):
        await message.channel.send(
            "To search, message the following:"
            "\n Example: '!search <name of the game>'"
        )
    elif message.content.startswith("!offline"):
        await search_fitgirl(message)
    elif message.content.startswith("!online"):
        await search_onlinefix(message)


# Run discord client
client.run(constants(credential="TOKEN"))
