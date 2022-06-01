import tkinter
import sys
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import messagebox

fileLoaded = False
selection = None

def fileNotLoadedException():
    global fileLoaded
    if not fileLoaded:
        tkinter.messagebox.showwarning("Nieprawidłowe polecenie", "Najpierw wybierz plik!")
        return True
    return False

def noSelectionException():
    global selection
    if not selection:
        tkinter.messagebox.showwarning("Nieprawidłowe polecenie", "Najpierw wybierz kanał!")
        return True
    return False

def findBegin(channel, index):
    while index >= 0 and channel[index] > channel[index-1]:
        index -= 1
    return index

def findEnd(channel, index):
    while index < len(channel) and channel[index] <= 0:
        index += 1
    return index

def openFile():
    global filenameopen
    global text
    global SampleFreq
    global column
    global fileLoaded
    global selectionLabel

    filenameopen = tkinter.filedialog.askopenfilename(initialdir = "/", title = "Otwórz plik:", filetypes = (("Pliki CSV", "*.csv"), ("Pliki tekstowe", "*.txt")))
    if not filenameopen:
        tkinter.messagebox.showwarning("Niepowodzenie", "Nie wybrano pliku!")
        return

    plik = open(filenameopen)
    text = plik.readlines()
    plik.close()

    SampleFreq = float(text[0][17:-1].replace(',', '.'))

    text = text[13:]
    column = [[] for i in range(4)]

    for x in text:
       
        x = x.replace(',', '.')
        fields = x.split('. ')
        for i in range(4):
            column[i].append(float(fields[i]))

    fileLoaded = True
    selectionLabel.config(text=filenameopen)
    

def onselect(event):
    global selection
    widget = event.widget
    selection = widget.get(int(widget.curselection()[0]))

def showMax():
    global selection
    global column
    if fileNotLoadedException():
        return
    if noSelectionException():
        return
    tkinter.messagebox.showinfo("Amplituda", "Wartość amplitudy fali N wynosi: " + str(max(column[int(selection)-1])))

def showTime():
    global selection
    global column
    global SampleFreq
    if fileNotLoadedException():
        return
    if noSelectionException():
        return
    
    index = int(selection) - 1
    beg = findBegin(column[index], column[index].index(max(column[index])))
    time=1/SampleFreq*beg
    time=time*1000
    time=round(time,3)
    tkinter.messagebox.showinfo("Czas nadejscia", 
                    "Falę N zarejestrowano po upływie: " + str(time) + " ms")

    
def showFreq():
    global SampleFreq
    global column
    global selection
    global czestotliwosc
    if fileNotLoadedException():
        return
    if noSelectionException():
        return

    index = int(selection) - 1
    beg, end = findBegin(column[index], column[index].index(max(column[index]))), findEnd(column[index], column[index].index(min(column[index])))
    fu1 = np.fft.fft(column[index][beg:end])
    n1=round((len(fu1))/2)
    fu2=abs(fu1[:n1])
    m=1
    maxii=0
    while m<n1:
        if fu2[m]>maxii:
            maxii=fu2[m]
            maxi2=m
        m=m+1
    czestotliwosc=maxi2*(SampleFreq/(2*n1))
    czestotliwosc=round(czestotliwosc,2)
            
    
    tkinter.messagebox.showinfo("Harmoniczna", "Wartość częstotliwości pierwszej harmonicznej wynosi " + str(czestotliwosc) + " Hz")
 

def showPeriod():
    global SampleFreq
    global selection
    global column
    if fileNotLoadedException():
        return
    if noSelectionException():
        return
    index = int(selection)-1
    period = 1 / SampleFreq * (findEnd(column[index], column[index].index(min(column[index])))
    - findBegin(column[index], column[index].index(max(column[index]))))
    period = period*1000
    period = round(period, 3)
    tkinter.messagebox.showinfo("Czas trwania", "Czas trwania fali N wynosi: " + str(period) + " ms")

def showChartwst():
    global selection
    global column
    global SampleFreq
    if fileNotLoadedException():
        return
    if noSelectionException():
        return
    index = int(selection)-1
    
    
    y= column[index]
    
    
    plt.ylabel("Amplituda [Pa]")
    plt.xlabel("Liczba próbek")

    plt.plot(y)
    plt.show()

def showChart():
    global selection
    global column
    global SampleFreq
    if fileNotLoadedException():
        return
    if noSelectionException():
        return
    index = int(selection)-1
    beg, end = findBegin(column[index], column[index].index(max(column[index]))), findEnd(column[index], column[index].index(min(column[index])))
    
    
    y= column[index][beg-50:end+100]
    z=len(y)
    
    x=np.linspace(1000*(1/SampleFreq)*(beg-50), 1000*(1/SampleFreq)*(end+100), z)
    plt.ylabel("Amplituda [Pa]")
    plt.xlabel("Czas [ms]")

    plt.plot(x,y)
    plt.show()
    
def saveToFile():
    global column
    global selection
    global SampleFreq
    global czestotliwosc
    global filenameopen
    if fileNotLoadedException():
        return
    if noSelectionException():
        return

    index = int(selection) - 1
    
    maxi = str(max(column[index]))
    
    period = 1 / SampleFreq * (findEnd(column[index], column[index].index(min(column[index])))
    - findBegin(column[index], column[index].index(max(column[index]))))
    period=period*1000
    period=round(period,3)
    
    beg, end = findBegin(column[index], column[index].index(max(column[index]))), findEnd(column[index], column[index].index(min(column[index])))
    fu1 = np.fft.fft(column[index][beg:end])
    n1=round((len(fu1))/2)
    fu2=abs(fu1[:n1])
    m=1
    maxii=0
    while m<n1:
        if fu2[m]>maxii:
            maxii=fu2[m]
            maxi2=m
        m=m+1
    czestotliwosc=maxi2*(SampleFreq/(2*n1))
    czestotliwosc=round(czestotliwosc,2)
    
    beg = findBegin(column[index], column[index].index(max(column[index])))
    time=1/SampleFreq*beg
    time=time*1000
    time=round(time,3)

    
    filename = tkinter.filedialog.asksaveasfilename(initialdir="/", title="Zapisz plik:", filetypes=(("Pliki CSV", "*.csv"), ("Pliki tekstowe", "*.txt")))
    if not filename:
        tkinter.messagebox.showwarning("Niepowodzenie", "Nie wybrano pliku!")
        return
    
    
    plik = open(filename,'a')
    plik.writelines('\n' + str(filenameopen) + ', ' + 'kanał '+str(selection)+', ' + str(maxi) + ', ' + str(period) + ' ms, '+ str(czestotliwosc)+' Hz, ' + str(time)+ ' ms.')
    plik.close()

def showFFT():
    global SampleFreq
    global column
    global selection
    if fileNotLoadedException():
        return
    if noSelectionException():
        return

    index = int(selection) - 1
    beg, end = findBegin(column[index], column[index].index(max(column[index]))), findEnd(column[index], column[index].index(min(column[index])))
    fu = np.fft.fft(column[index][beg:end])
    n=len(fu)
    f=np.linspace(0, SampleFreq, n)
    plt.bar(f[:n // 6], np.abs(fu)[:n // 6] * 1 / n, width=500)
    plt.ylabel("Amplituda")
    plt.xlabel("Częstotliwosc [Hz]")
    plt.grid()
    plt.show()


app = tkinter.Tk()
app.title("Odczyt danych fali N")
content = tkinter.Frame(app)
topFrame = tkinter.Frame(content)
channelsFrame = tkinter.Frame(content)
fFrame = tkinter.Frame(content)
chartFrame = tkinter.Frame(content)
bottomFrame = tkinter.Frame(content)

selectionLabel = tkinter.Label(topFrame, text="<brak otwartego pliku>", wraplength=130)
openButton = tkinter.Button(topFrame, text="Otwórz", command=openFile, width=18, height=1)

channelsLabel = tkinter.Label(channelsFrame, text="Wybór kanału:", width=22, height=1)
channelsList = tkinter.Listbox(channelsFrame, selectmode="SINGLE", justify="center", bg="#FFC6B5", width=22, height=4)
channelsList.bind('<<ListboxSelect>>', onselect)
channelsList.insert(1, "1")
channelsList.insert(2, "2")
channelsList.insert(3, "3")
channelsList.insert(4, "4")

maxButton = tkinter.Button(fFrame, text="Amplituda fali N", command=showMax, width=18, height=1)
fButton = tkinter.Button(fFrame, text="Harmoniczna fali N", command=showFreq, width=18, height=1)
periodButton = tkinter.Button(fFrame, text="Czas trwania fali N", command=showPeriod, width=18, height=1)

chartButton = tkinter.Button(chartFrame, text="Przebieg fali N", command=showChart, width=18, height=1)
fftButton = tkinter.Button(chartFrame, text="Rozkład harmonicznych", command=showFFT, width=18, height=1)

saveButton = tkinter.Button(bottomFrame, text="Zapisz", command=saveToFile, 
                            width=18, height=1)

chartwstButton = tkinter.Button(chartFrame, text="Przebieg rejestracji", 
                                command=showChartwst, width=18, height=1)
timeButton = tkinter.Button(fFrame, text="Czas nadejscia fali N", 
                            command=showTime, width=18, height=1)

content.grid(column=0, row=0, padx=10, pady=10)

topFrame.grid(column=1, row=0, pady=10)
selectionLabel.grid(column=1, row=0)
openButton.grid(column=1, row=1)

channelsFrame.grid(column=1, row=2, pady=10)
channelsLabel.grid(column=1, row=2)
channelsList.grid(column=1, row=3)

fFrame.grid(column=1, row=4, pady=10)
maxButton.grid(column=1, row=4)
fButton.grid(column=1, row=5)
periodButton.grid(column=1, row=6)

chartFrame.grid(column=1, row=8, pady=10)
chartButton.grid(column=1, row=12)
fftButton.grid(column=1, row=9)

bottomFrame.grid(column=1, row=10, pady=10)
saveButton.grid(column=1, row=10)

chartwstButton.grid(column=1, row=8)
timeButton.grid(column=1, row=7)

app.mainloop()
