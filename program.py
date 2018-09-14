import requests #Used with Beautiful Soup as an input for the web address
from bs4 import BeautifulSoup #Imports Beautiful soup which is used for scraping the websites
import csv #The file type used to store values in a .csv
import sys #system comands that allow the program to use the quit function
import tkinter #tkinter is the module used to create guis
def createRootWindow(): #The deafault main menu window that opens first

    root = tkinter.Tk()  #root is then used to call all the tkinter functions for this window

    w = 400 #The width of the gui
    h = 400 #The height of the gui

    ws = root.winfo_screenwidth() #The screen width of the screen being used
    hs = root.winfo_screenheight() #The screen height of the screen being used

    x = (ws / 2) - (w/2) #the x position for the centre of the screen
    y = (hs / 2) - (h/2) #the y position for the centre of the screen


    root.geometry("%dx%d+%d+%d" % (w, h, x, y)) #Sets the geometry of the window
    root.title("News Scraper") #Sets the window title that appears at the top of the screen
    root.iconbitmap("news.ico") #Sets the icon that appears in the top left corner of the screen
    root.config(bg="white") #Sets the bacground of the window to the colour white
    label = tkinter.Label(root, text="News Scraper:", font=("Comic Sans MS", 30), fg="cyan", bg="white")
    #Adds a lsbel onto the screen with the text News Scaper in a font and size, with different colours set as well
    guardianButton = tkinter.Button(root, text="Guardian Scraper", font=("Comic Sans MS", 20), bg="white" , command = lambda: [root.destroy(),guardianWindow()])
    #the lambda is used to allow multiple functions to be used as a command for when the button is clicked
    bbcButton = tkinter.Button(root, text="BBC Scraper", font=("Comic Sans MS", 20), bg="white", command = lambda: [root.destroy(),bbcWindow()])
    #root.destroy is the command used to destory the main menu gui which also shuts the program as well as there's nothing else to run
    quitButton = tkinter.Button(root, text="Quit", command=lambda: [root.destroy()], font=("Comic Sans MS", 10),
                                bg="white")
    label.pack()
    guardianButton.pack()
    bbcButton.pack()
    quitButton.pack()

    #Each widget needs to be packed in the order you want them to appear on the gui

    root.mainloop() #Finally, a mainloop is ran which prints the gui to the screen with all the settings from above

def guardianWindow():
    window = tkinter.Tk()

    w = 800
    h = 600

    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x = (ws / 2) - (w/2)
    y = (hs / 2) - (h/2)


    window.geometry("%dx%d+%d+%d" % (w, h, x, y))


    # window.geometry("800x600")
    window.title("Guardian Scraper")
    window.iconbitmap("news.ico")
    window.config(bg = "white")
    label = tkinter.Label(window, text="Guardian Scraper:", font=("Comic Sans MS", 30), fg="cyan", bg="white")
    quitButton = tkinter.Button(window, text="Back", command=lambda: [window.destroy(),createRootWindow()], font=("Comic Sans MS", 10))


    label.pack()

    scroll = tkinter.Scrollbar(window) #The widget for having a scroll bar
    scroll.pack(side = "right", fill = "y") #The scroll bar is on the right side

    text = tkinter.Text(window) #A text box for where the headlines will be displayed
    text.focus_set()
    text.pack(fill = "y")
    scroll.config(command = text.yview) #The scroll bar is set to control the textbox y view
    text.config(yscrollcommand = scroll.set)

    list = guardianScrape() #The variable list is equal to what is returned by the function when called
    for i in list:
        text.insert(tkinter.END, "%s\n" % i)
        #For every item in the list, it is added to the text box

    quitButton.pack()

def bbcWindow():
    window = tkinter.Tk()

    w = 800
    h = 600

    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    window.geometry("%dx%d+%d+%d" % (w, h, x, y))
    # window.geometry("800x600")

    window.title("BBC Scraper")
    window.iconbitmap("news.ico")
    window.config(bg="white")
    label = tkinter.Label(window, text="BBC Scraper:", font=("Comic Sans MS", 30), fg="cyan", bg="white")
    quitButton = tkinter.Button(window, text="Back", command=lambda: [window.destroy(), createRootWindow()],
                                font=("Comic Sans MS", 10))


    label.pack()

    scroll = tkinter.Scrollbar(window)
    scroll.pack(side="right", fill="y")

    text = tkinter.Text(window)
    text.focus_set()
    text.pack(fill="y")
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    list = bbcScrape()
    for i in list:

        text.insert(tkinter.END, "%s\n" % i)

    quitButton.pack()

def guardianScrape(): #Function used to scrape the guardian web page

    guardianFile = open("guardianScrape.csv", "w") #Sets the guardian file to the guardian.csv file in write mode
    guardianFileWriter = csv.writer(guardianFile) #the variable that is used to write to the guardianFile
    guardianFileWriter.writerow(["Headline", "Link"]) #The two headings that will appear at the top are headline and link

    guardianPage = requests.get("https://www.theguardian.com/business/economics")
    #The web url for the guardian business page
    soupGuardian = BeautifulSoup(guardianPage.content, "lxml")
    #uses lxml to store the contents of the guardian website in the variable
    guardianHeadlineList = [] #Sets to blank lists
    guardianLinkList = []

    for article in soupGuardian.find_all("div",class_="fc-slice-wrapper"):
        #The first for loop goes through each div class called fc-slice-wrapper on the website
        for row in article.find_all("div",class_="fc-item__container"):
            #Then it finds all the div classes called fc-item__container to get the information needed to find headlines
            headline = row.find("span",class_="js-headline-text").text
            #The headline is found in the span class called js-headline-text and to get just the headline, .text is used at the end
            link = row.find("a",class_="u-faux-block-link__overlay js-headline-text").get("href")
            #The link to the article is found in an a class and to get the href link,   .get("href") is used to get the url from the href
            guardianHeadlineList.append(format("Headline: " + headline))
            #format is used to add a headline text before every headline is printed to the sceen
            guardianLinkList.append(link)
            guardianFileWriter.writerow([headline,link])

    guardianFile.close() #Closes the file which saves all changes made
    return guardianHeadlineList #Returns the contents of the variable to the variable where the function was called

def bbcScraping(var,bbcFileWriter):
    global list
    bbcSummaryList = []
    bbcLinkList = []

    bbcPage  = requests.get("https://www.bbc.co.uk/news/business")
    soupBbc = BeautifulSoup(bbcPage.content, "lxml")
    for article in soupBbc.find_all("div",class_="container"):
        for container in article.find_all("div",class_=var):
            headline = container.find("span",class_="title-link__title-text").text
            list.append(format("Headline: " + headline))
            try:
                summary =  container.find("p").text
            except:
                summary = "None"
            link = container.find("a",class_="title-link").get("href")
            link = format("https://www.bbc.co.uk"+link)
            bbcLinkList.append(link)
            bbcFileWriter.writerow([headline,summary,link])
            if summary == "None":
                bbcSummaryList.append("No Summary available")
            else:
                bbcSummaryList.append(summary)
    return

def bbcScrape():
    global list
    bbcFile = open("bbcScrape.csv", "w")
    bbcFileWriter = csv.writer(bbcFile)
    bbcFileWriter.writerow(["Headline","Summary","Link"])
    list = []
    bbcScraping("buzzard-item",bbcFileWriter)
    bbcScraping("pigeon-item__body",bbcFileWriter)
    bbcScraping("pigeon-item faux-block-link",bbcFileWriter)
    bbcScraping("macaw-item__body",bbcFileWriter)
    #The BBC website is more difficult to scrape at once so different div sections need
    #to be used for different parts of the bbc site website
    bbcFile.close()

    return list

createRootWindow()