import json
import random
from datetime import datetime
import os

path = 'Data'
if not os.path.exists(path):
    os.mkdir(path)
now = datetime.now() 
date_time = now.strftime("%d-%m-%Y-%H-%M-%S")





def lootjesPicken(namen, loten, number, resLootjes):
    while True:
        randomNummer = random.randint(0,len(resLootjes)- 1)
        if namen[number] != resLootjes[randomNummer]:
            break
    loten[number] = resLootjes[randomNummer]
    resLootjes.pop(randomNummer)
    return loten, resLootjes
    

namenLijstje = list() #maak de lijst
lootjes = list()
restrerendeLootjes = list()
namenVraagRondje = True #zorg voor de loop
print("geef drie+ namen, laat leeg als je niemand meer nodig hebt")
while namenVraagRondje == True:
    antwoord = input()
    if antwoord != "": #als het niet leeg is
        if antwoord not in namenLijstje:
            namenLijstje.append(antwoord)
    else:
        namenVraagRondje = False #stop de loop
if len(namenLijstje) > 2:
    for x in range(len(namenLijstje)):
        lootjes.append(namenLijstje[x])
        restrerendeLootjes.append(namenLijstje[x])
    testEnvirement = True
    for x in range(len(namenLijstje)):
        lootjes, restrerendeLootjes = lootjesPicken(namenLijstje, lootjes, x, restrerendeLootjes)
    for x in range(len(namenLijstje)):
        print(f"{namenLijstje[x]} heeft {lootjes[x]}'s lootje getrokken")
lootjesDict = {}
for x in range(len(namenLijstje)):
    lootjesDict[namenLijstje[x]] = lootjes[x]

json_string_lootjesDict = json.dumps(lootjesDict)
with open(f"Data/{date_time}.json", 'w') as outfile:
    json.dump(json_string_lootjesDict, outfile)   