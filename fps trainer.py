import tkinter
import tkinter.messagebox
gameVersion = '1.2.0'
#old variant: [name,[time],{appDictionary},randint1,randint2,[data with lock += 2 randints],[dataHistory],[data with lock without 2 randints]]
#new variant: [name,[time],{appDictionary},randint1,randint2,[data with lock += 2 randints],[dataHistory],[data with lock without 2 randints]], {achievements}, {collectables}

import pickle
import os
import datetime
import random
import configparser


if os.path.isfile("systemConfig.ini"):#read config if it exists
    config = configparser.ConfigParser()
    config.read('systemConfig.ini')
else:#create config
    with open('systemConfig.ini', 'w') as configfile:
        config = configparser.ConfigParser(allow_no_value=True)
        folder = input('do you have a specific folder where you want to store account data?\nimport the path, or not\n>')
        config['DEFAULT'] = {'#don\'t change the file-extention if you are not sure of what it is' : None,
            'fileExtention' : 'mcld'}
        if os.path.isdir(folder):#check if the inputted folder exists
            if folder[len(folder)-1] != '/' and folder[len(folder)-1] != '\\':
                folder += '\\'
            config['User'] = {'SaveFileFolder' : folder,'AutoLogin' : 'False', 'AccountName' : 'testaccount'}
        else:
            config['User'] = {'SaveFileFolder' : 'accounts/','AutoLogin' : 'False', 'AccountName' : 'testaccount'}
            try:
                os.mkdir('accounts/')
            except:
                pass
        config.write(configfile)
        print('we created systemConfig.ini, this contains configurations for the account system, change the [User] section at any time')

#load config data
fileExtention = config['DEFAULT']['fileExtention']
path = config['User']['SaveFileFolder']
autoLogin = config['User']['AutoLogin']
autoLoginName = config['User']['AccountName']

def checkSave(pickledData):#check if account is corrupted
    def corruptedAccount():#what to do when account is corrupted
        exit()
    try:
        name, list1, dictionary, num1, num2, data1, data2, data3, achievements, collectables = pickledData
    except:
        name, list1, dictionary, num1, num2, data1, data2, data3 = pickledData
    if data3[1] - data3[0] != data1[1] - data1[0] or data1[0] != data3[0] + (num1 * num2):#check if decryption is possible
        input('Account Data Corrupted, Please find a way to fix it or create a new one')
        corruptedAccount()
        return False
    else:
        print('Account Loaded Correctly')
        return True

def fixData(data):#remove encryption
    data[1] = data[1] - data[0]
    return data

def loadAccount():
    if checkSave(pickle.load( open(f'{path}{search}.{fileExtention}', "rb" ))) == True: #check if it is not corrupted (in my encryption)
        try:
            name, list1, appDataDict, num1, num2, data1, data2, data3, achievements, collectables= pickle.load( open(f'{path}{search.lower()}.{fileExtention}', "rb" )) #load the account
        except:
            name, list1, appDataDict, num1, num2, data1, data2, data3 = pickle.load( open(f'{path}{search.lower()}.{fileExtention}', "rb" )) #load old variant of account
            achievements = {}
            collectables = {}
        startTime = datetime.datetime.now()#start counting how long you are using the program
        data = fixData(data3)#decrypt data
    return name, list1, appDataDict, num1, num2, data1, data2, data3, achievements, collectables, startTime, data


def closeAccount(name, list1, data1):#close the account
    def scrambleData(data,num1,num2,key, num):
        data[0] = key + ((num1 * num2) * num)#add encryption
        data[1] += data[0]
        return data
    global startTime
    closeTime = datetime.datetime.now()#check the time
    list1[0] = round(list1[0] + ((closeTime - startTime).total_seconds()) // 60)#check difference in time from when opened
    num1 = random.randint(0,1000)#key1
    num2 = random.randint(0,1000)#key2
    key = random.randint(0,10000)#masterKey
    #this was used when the data is still encrypted, but if it's decrypted, keep this a comment:
    #data1 = fixData(data1)
    pickle.dump([name, list1, appDataDict, num1, num2, scrambleData(list(data1),num1,num2,key,1), scrambleData(list(data1),num1,num2,key,2), scrambleData(list(data1),num1,num2,key,0), achievements, collectables] , open(f'{path}{name}.{fileExtention}', "wb" ) )

def stringToSeed(seedString): #turns everything into ther ASCII value
    seedList = []
    for x in seedString:
        seedList.append(ord(x))#change every character into its ASCII value
    seedString = ''.join([str(elem) for elem in seedList])#add list together into string
    seed = int(seedString)
    return seed

#for easy loading and testing the account, you can enable this in the config
if autoLogin.lower() == 'true':
    search = autoLoginName
else:
    search = input('please give username\n>')


if os.path.exists(f'{path}{search.lower()}.{fileExtention}'):#check if account exists
    print('user found')
    name, list1, appDataDict, num1, num2, data1, data2, data3, achievements, collectables, startTime, data = loadAccount()
        
else:
    while True:
        print('user not found, do you want to create a new user with this name? Y/N')

        #for easy loading and testing the account
        #answer = 'y'#you can use this to skip the input for testing your code

        answer = input('you will be logged out afterwards\n>')
        if answer.lower() == 'y':
            pickle.dump([search.lower(), [0], {}, 69, 420, [41325, 41325], [41325, 41325], [12345, 12345], {}, {}], open(f'{path}{search.lower()}.{fileExtention}', "wb" ) )
            exit()
        elif answer.lower() == 'n':
            exit()

#example achievement


#use the dictonary for app related files, like for example rebirths or amounts of diamonds
#change this to your app their name
appName = 'fpsTrainerMartijn'

if appName not in appDataDict:#if the user hasn't played before
    appDataDict[appName] = [gameVersion, {}]
else:
    #print(appDataDict[appName])#prints your data, just to show you how it works
    pass


#this is your game data, for easy use. but you can also just access your gamedata without this
appData = appDataDict[appName]
#it works the same with the collectables and achievements dictionaries as with the account data dict








#code:

possibleActionsList = ['Press A', 'Press S', 'Press W', 'Press D', 'Press Space', 'Click', 'Double Click', 'Triple Click']


defaultTimeVariable = 20
timeVariable = defaultTimeVariable

window = tkinter.Tk()
window.geometry('650x350')
window.attributes('-topmost',True)

countdown = timeVariable
if timeVariable not in appDataDict[appName][1]:
    highscore = 0
else:
    highscore = appDataDict[appName][1][timeVariable]
neededAction = -1
allowPlay = False
score = 0

timeString = tkinter.StringVar(value=f'Time Left: {countdown}')
highscoreString = tkinter.StringVar(value=f'Highscore: {highscore}')
currentScoreString = tkinter.StringVar(value=f'Current Score: {score}')
actionString = tkinter.StringVar(value=f'{possibleActionsList[neededAction]}')

def on_closing():
    global appDataDict
    window.destroy()
    #use this line if you edited the gamedata before the closeAccount(), if you didn't edit the gamedata, you can skip it
    try:
        appDataDict[appName][1][timeVariable] = int(highscore)
    except:
        pass
    #close the account correctly (so it won't get corrupted), use this where you need it, and save it here as a comment
    closeAccount(name, list1, data)

def updateLabels():
    global timeString
    global highscoreString
    global currentScoreString
    global appData
    if allowPlay == True:
        appDataDict[appName][1][timeVariable] = highscore
    timeString.set(f'Time Left: {countdown}')
    highscoreString.set(f'Highscore: {highscore}')
    currentScoreString.set(f'Current Score: {score}')

def actionFunction(actionPreformed, points = 1):
    global score 
    global neededAction
    global highscore
    updateLabels()
    if actionPreformed == neededAction:
        score += points
        if score > highscore:
            highscore = score
        neededAction = random.randint(0,len(possibleActionsList)-1)
        createLabel()

def createLabel():
    global actionLabel
    global actionString
    global neededAction
    neededAction = random.randint(0,len(possibleActionsList)-1)
    try:
        actionLabel.destroy()
    except:
        pass
    actionString.set(f'{possibleActionsList[neededAction]}')
    actionLabel = tkinter.Label(window)
    actionLabel.configure(bg = 'white', fg = 'black', textvariable=actionString, font=("Comic Sans MS", 11))
    actionLabel.place(y = random.randint(45,322), x = random.randint(0,575))
    actionLabel.bind('<Double-Button-1>',lambda event: actionFunction(6,2))
    actionLabel.bind('<Triple-Button-1>',lambda event: actionFunction(7,2))
    actionLabel.bind('<Button-1>',lambda event: actionFunction(5,2))

def startGame():
    global countdown
    global allowPlay
    global startbutton
    global amountOfTime_entry
    global amountOfTime_label
    global highscore
    global timeVariable
    if amountOfTime_var.get() != '':
        timeVariable=int(amountOfTime_var.get())
        if timeVariable < 0:
            timeVariable *= -1
        if timeVariable not in appDataDict[appName][1]:
            appDataDict[appName][1][timeVariable] = 0
        highscore = appDataDict[appName][1][timeVariable]
        amountOfTime_entry.destroy()
        amountOfTime_label.destroy()
        startButton.destroy()
        allowPlay = True
        countdown = timeVariable + 1
        updateLabels()
        createLabel()
        tick()

def timeUp():
    global startButton
    global score
    global amountOfTime_entry
    global amountOfTime_label
    updateLabels()
    appDataDict[appName][1][timeVariable] = highscore
    if tkinter.messagebox.askokcancel("Time is up!", f"You got {score} points!\nDo you want to play again?"):
        startButton = tkinter.Button(window)
        startButton.configure(fg = 'black', bg = 'white', font=("Comic Sans MS", 11), text = 'press here to start', command = startGame)
        startButton.place(y=170, x=250)
        amountOfTime_entry = tkinter.Entry(window,textvariable = amountOfTime_var, font=('calibre',10,'normal'))
        amountOfTime_entry.place(y=150, x=250)
        amountOfTime_label = tkinter.Label(window, text = 'Input Time To Play', font = ('calibre',10,'bold'))
        amountOfTime_label.place(y=125, x=250)
        score = 0
    else:
        on_closing()

def callback(*args):
    global timeVariable
    global highscore
    global countdown
    while amountOfTime_var.get() != '':
        try:
            timeVariable=int(amountOfTime_var.get())
            if timeVariable < 0:
                timeVariable *= -1
            break
        except:
            amountOfTime_var.set(amountOfTime_var.get()[0:-1])
    if timeVariable not in appDataDict[appName][1]:
        highscoreString.set(f'Highscore: -')
        highscore = ' -'
    else:
        highscore = appDataDict[appName][1][timeVariable]
    countdown = timeVariable
    updateLabels()
    if amountOfTime_var.get() == '':
        highscoreString.set(f'Highscore: NaN')
        timeString.set(f'Time Left: NaN')
        

def tick():
    global allowPlay
    global countdown
    if allowPlay == True:
        countdown -= 1
        if countdown == 0:
            allowPlay = False
            try:
                actionLabel.destroy()
                timeUp()
            except:
                pass
        else:
            window.after(1000, tick)
    appDataDict[appName] = appData 
    updateLabels()
    
balkje = tkinter.Label(window)
balkje.configure(bg = 'black')
balkje.pack(ipady=10, ipadx=200, fill = 'x')
timeCounter = tkinter.Label(window)
timeCounter.configure(bg = 'black', fg = 'white', textvariable=timeString, font=("Comic Sans MS", 19))
timeCounter.place(y = 0, x = 0)
highscoreCounter = tkinter.Label(window)
highscoreCounter.configure(bg = 'black', fg = 'white', textvariable=highscoreString, font=("Comic Sans MS", 19))
highscoreCounter.place(y = 0, x = 200)
currentScore = tkinter.Label(window)
currentScore.configure(bg = 'black', fg = 'white', textvariable=currentScoreString, font=("Comic Sans MS", 19))
currentScore.place(y = 0, x = 400)


amountOfTime_label = tkinter.Label(window, text = 'Input Time To Play', font = ('calibre',10,'bold'))
amountOfTime_label.place(y=130, x=250)
amountOfTime_var=tkinter.StringVar()
amountOfTime_var.set(timeVariable)
amountOfTime_entry = tkinter.Entry(window,textvariable = amountOfTime_var, font=('calibre',10,'normal'))
amountOfTime_entry.place(y=150, x=250)
amountOfTime_var.trace('w', callback)


startButton = tkinter.Button(window)
startButton.configure(fg = 'black', bg = 'white', font=("Comic Sans MS", 11), text = 'press here to start', command = startGame)
startButton.place(y=170, x=250)

window.bind('<space>',lambda event: actionFunction(4))
window.bind('w',lambda event: actionFunction(2))
window.bind('a',lambda event: actionFunction(0))
window.bind('s',lambda event: actionFunction(1))
window.bind('d',lambda event: actionFunction(3))



window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()



