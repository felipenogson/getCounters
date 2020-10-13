import requests
from bs4 import BeautifulSoup
import os


def top_counters(soup):
    stat_champs = []
    champ_winrates = []
    top_three = {}
    worst_three = {}
    for top in soup.find_all('tr', {'data-champion-id':True}):
        #print(top)
        for champs in top.find_all('td', class_='champion-stats-header-matchup__table__champion'):
            stat_champs.append(champs.contents[2].strip("\t").strip("\n").lower())
        for winrate in top.find_all('b'):
            champ_winrates.append(((float(winrate.string[:-1]))-100)*-1)
    for x in range(0,6):
        if x <= 2:
            worst_three[stat_champs[x]] = champ_winrates[x]
        else:
            top_three[stat_champs[x]] = champ_winrates[x]
    return(top_three, worst_three)

def grab_champs(summoner):
    champ_plays = {}
    from requests_html import HTMLSession
    session = HTMLSession()
    r = session.get('https://www.leagueofgraphs.com/summoner/champions/na/'+summoner+'#championsData-all-queues')
    #print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    soup.find
    for items in soup.find_all("tr"):
        main = []
        for champ in items.find_all('span', class_="name"):
            main.append(champ.string.strip())
        find_td = []
        for plays in items.find_all('td', {'data-sort-value':True}):
            find_td.append(plays.attrs['data-sort-value'])
        if len(main) > 0 and len(find_td) > 0:
            champ_plays[main[0].lower()] = int(find_td[0])
    return(champ_plays)

def grab_most_used(user_champs, game_count):
    most_used = []
    for champ in user_champs:
        if user_champs[champ] >= game_count:
            most_used.append(champ.lower())
    return most_used



def find_counters(champ, lane, my_champs):
    counters = {}
    my_counter_champs = {}
    top_three = {}
    worst_three = {}

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get('https://www.op.gg/champion/'+champ+'/statistics/'+lane+'/matchup', headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    try: 
        top_three, worst_three = top_counters(soup)
    except: 
        pass

    for x in soup.find_all("div", class_="champion-matchup-champion-list__item"):
        counters[x.attrs['data-champion-name']] = round((float(x.attrs['data-value-winrate'])*100)*-1+100, 2)
    print("----Matchup-"+champ+"-"+lane+"----")
    for champion in my_champs:
        if champion.lower() in counters:
            my_counter_champs[champion] = counters[champion]
    my_counter_champs = {k: v for k, v in sorted(my_counter_champs.items(), key=lambda x: x[1], reverse=True)}

    return (my_counter_champs, top_three, worst_three)


def run_counter(my_champs):
    #my_champs = ['akali','yasuo','vladimir','anivia','fizz', 'jax', 'urgot', 'maokai', 'tarric', 'maokai', 'pyke', 'yasuo', 'ezreal', 'vayne', 'gragas']
    possible_lane = ['top','jungle','support','bot','mid']
    while True:
        lane = input('Enter lane (top,mid,bot,support,jungle):\n')
        champ = input("Enter enemy laner:\n")
        find_counters(champ.lower(), lane.lower(), my_champs)
        next = ('\n\n\nClick Enter to go again, exit to quit.\n')
        if next == 'quit':
            os._exit()



def main():
    summoner = input("Enter Summoner Name:\n")
    user_champs = grab_champs(summoner)
    user_champs = grab_most_used(user_champs, 10)
    run_counter(user_champs)

if __name__ == "__main__":
    main()
