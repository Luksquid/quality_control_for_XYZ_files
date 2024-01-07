from math import sqrt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def doesContains(x, y, epsg):
    epsg = int(epsg)
    x = float(x)
    y = float(y)
    if epsg == 32633:
        x_min = 166021.44; y_min = 0.0; x_max = 833978.56; y_max = 9329005.18
    elif epsg == 32632:
        x_min = 166021.44; y_min = 0.0; x_max = 833978.56; y_max = 9329005.18
    elif epsg == 2180:
        x_min = 144693.28; y_min = 125837.02; x_max = 876500.36; y_max = 908411.19
    elif epsg == 2178:
        x_min = 6998248.3; y_min = 5429210.14; x_max = 7730457.33; y_max = 6221575.79
    if x>=x_min and x<=x_max and y>=y_min and y<=y_max:
        return True
    else:
        return False


def action(inDir, outDir, epsg):
    allFiles = os.listdir(inDir)
    firstOpening = True
    for file in allFiles:
        if(file.endswith('.xyz')):
            with open(inDir + "/" + file, 'r') as directoryFile:
                coordinates = directoryFile.readlines()
                inBounds = True
                listOfHeight = []
                minz = float(coordinates[0].split(' ', 2)[2])
                maxz = float(coordinates[0].split(' ', 2)[2])
                for coordinate in coordinates:                              # pętla sprawdza czy koordynat jest poza granicami
                    tempCoords = coordinate.split(' ', 2)
                    listOfHeight.append(float(tempCoords[2]))
                    if not doesContains(tempCoords[0], tempCoords[1], epsg):
                        inBounds = False
                    if float(tempCoords[2]) > maxz:
                        maxz = float(tempCoords[2])
                    if float(tempCoords[2]) < minz:
                        minz = float(tempCoords[2])
                averageHeight = sum(listOfHeight) / len(listOfHeight)
                standardDeviationCount = 0
                for coordinate in coordinates:                              # pętla sprawdza czy koordynat jest poza granicami
                    tempCoords = coordinate.split(' ', 2)
                    standardDeviationCount += (float(tempCoords[2]) - averageHeight)**2
                standardDeviation = sqrt(standardDeviationCount/len(coordinates))
                listOfWringPoints = []
                for coordinate in range(len(coordinates)):
                    tempCoords = coordinates[coordinate].split(' ', 2)
                    if(float(tempCoords[2])>(averageHeight+3*standardDeviation)):
                        listOfWringPoints.append(coordinate)
            if(firstOpening):
                openningMode = 'w'
            else:
                openningMode = 'a'
            with open(outDir + "/report.txt", openningMode) as report:
                firstOpening = False
                report.write("File name: " + str(file) + "\n")
                if inBounds == True:
                    report.write("Files are inside the bounding box\n")
                else:
                    report.write("Files are outside the bounding box\n")
                report.write("Minimal height: " + str(minz))
                report.write("\nMaximal height: " + str(maxz))
                report.write("\nAvarge height: " + str(averageHeight))
                report.write("\nOutliers: ")
                for point in listOfWringPoints:
                    report.write(str(point) + " ")
                report.write("\n\n")
                report.close()



def open_folder_dialog1():
    folder_path = filedialog.askdirectory()
    path_entry1.delete(0, tk.END)
    path_entry1.insert(tk.END, folder_path)

def open_folder_dialog2():
    folder_path = filedialog.askdirectory()
    path_entry2.delete(0, tk.END)
    path_entry2.insert(tk.END, folder_path)

def submit():
    popupWidow = tk.Tk()
    popupWidow.geometry("90x90")
    popupWidow.title("Comunicate")
    padding = 10
    popupWidow.resizable(False, False)
    try:
        folder1 = path_entry1.get()
        folder2 = path_entry2.get()
        epsg = listEpsg.get()
        action(folder1, folder2, epsg)
        succesLabel = tk.Label(popupWidow, text="  Succes  ")
        succesLabel.grid(row=0, column=0, padx=padding, pady=padding)
        ok_button = tk.Button(popupWidow, text="Ok", command=popupWidow.destroy, height=1, width=6)
        ok_button.grid(row=1, column=0, padx=20, pady=padding)
    except ValueError:
        popupWidow.geometry("170x90")
        errorLabel = tk.Label(popupWidow, text="You can type only numbers")
        errorLabel.grid(row=0, column=0, padx=padding, pady=padding)
        ok_button = tk.Button(popupWidow, text="Ok", command=popupWidow.destroy, height=1, width=6)
        ok_button.grid(row=1, column=0, padx=padding, pady=padding)
    except FileNotFoundError:
        errorLabel = tk.Label(popupWidow, text="Wrong path")
        errorLabel.grid(row=0, column=0, padx=padding, pady=padding)
        ok_button = tk.Button(popupWidow, text="Ok", command=popupWidow.destroy, height=1, width=6)
        ok_button.grid(row=1, column=0, padx=padding, pady=padding)
    except UnboundLocalError:
        errorLabel = tk.Label(popupWidow, text="Wrong epsg")
        errorLabel.grid(row=0, column=0, padx=padding, pady=padding)
        ok_button = tk.Button(popupWidow, text="Ok", command=popupWidow.destroy, height=1, width=6)
        ok_button.grid(row=1, column=0, padx=padding, pady=padding)

window = tk.Tk()
window.geometry("490x180")
window.title("Python skrypt quality control plików XYZ")
# window.resizable(False, False)
buttonWidth = 6
buttonHeiht = 1
# Tworzenie przycisku "Browse" dla folderu 1
browse_button1 = tk.Button(window, text="Browse", command=open_folder_dialog1, height= buttonHeiht, width=buttonWidth)
browse_button1.pack()
browse_button1.grid(row=1, column=2, padx=10)


label0 = tk.Label(window, text=" ")
label0.grid(row=0, column=0)

# Pole tekstowe dla folderu 1
path_entry1 = tk.Entry(window, width=53)
path_entry1.grid(row=1, column=1)

# Tworzenie przycisku "Browse" dla folderu 2
browse_button2 = tk.Button(window, text="Browse", command=open_folder_dialog2, height= buttonHeiht, width=buttonWidth)
browse_button2.grid(row=3, column=2)

#lista dla epsg
epsgOptions = ["32633", "32632", "2180", "2178"]
listEpsg = tk.ttk.Combobox(window, values=epsgOptions, width=50)
listEpsg.grid(row=2, column=1)

# Etykieta epsg
label3 = tk.Label(window, text="Epsg")
label3.grid(row=2, column=0, padx=25, pady=10)

# Pole tekstowe dla folderu 2
path_entry2 = tk.Entry(window, width=53)
path_entry2.grid(row=3, column=1)

# Przycisk "Submit"
submit_button = tk.Button(window, text="Run", command=submit, height= buttonHeiht, width=buttonWidth)
submit_button.grid(row=4, column=1, pady=10, sticky=tk.E)
# Przycisk "Cancel"
cancel_button = tk.Button(window, text="Cancel", command=window.quit, height= buttonHeiht, width=buttonWidth)
cancel_button.grid(row=4, column=2)

label1 = tk.Label(window, text="Input")
label1.grid(row=1, column=0, padx=25, pady=5)

label2 = tk.Label(window, text="Output")
label2.grid(row=3, column=0)
# Uruchomienie pętli głównej programu
window.mainloop()