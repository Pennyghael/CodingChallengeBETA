import csv
import struct
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator

pitchData = {
    'Time': [],
    'Data': [],
    'Type': []
}
rollData = {
    'Time': [],
    'Data': [],
    'Type': []
}
yawData = {
    'Time': [],
    'Data': [],
    'Type': []
}
throttleSpinData = {
    'Time': [],
    'Data': [],
    'Type': []
}
function_mapping = {
    '07E3': lambda data, time: process07E3(data, time),
    '07E4': lambda data, time: process07E4(data, time),
    '0001': lambda data, time: processFloat(data, time, pitchData, 'Angle'),
    '0002': lambda data, time: processFloat(data, time, pitchData, 'Rate'),
    '0003': lambda data, time: processFloat(data, time, rollData, 'Angle'),
    '0004': lambda data, time: processFloat(data, time, rollData, 'Rate'),
    '0005': lambda data, time: processFloat(data, time, yawData, 'Angle'),
    '0006': lambda data, time: processFloat(data, time, yawData, 'Rate')
}


# Reads the csv file according to the indexes entered by the user, skipping the first lines without data.
# If no indexes entered, the entire file will be process.
# First data is detected by the string "Number" in the first entry of the row.
# Detects and processes relevant entries.
def processCSV():
    filePath = getFilePath()
    firstIndex = getInput("Enter first line you want to process (leave blank to process the entire file): ", 1) or 1
    nbLine = getInput("Enter number of lines you want to process (leave blank to process the entire file): ", 1)
    try:
        with open(filePath) as csvfile:
            start = False
            reader = csv.reader(csvfile, delimiter=';')

            for count, row in enumerate(reader, start=0):
                if not start or count < firstIndex - 1:
                    if row and row[0] == 'Number':
                        start = True
                    continue
                id = row[5]
                data = row[8:]
                time = float(row[1])

                if id in function_mapping:
                    function_mapping[id](data, time)

                if nbLine and count >= firstIndex + nbLine - 1:
                    break
    except Exception as e:
        print(f"An unexpected error has occurred : {e}")


# Prompts the user for the file path until program manages to open it
def getFilePath():
    while True:
        file_path = input("Enter csv file path: ")
        try:
            with open(file_path) as file:
                return file_path
        except FileNotFoundError:
            print("Error: file not found. Please check the file path and try again.")


# Prompts the user for an integer greater than a minimum
def getInput(prompt, minimum):
    while True:
        try:
            value = input(prompt)
            if value == '':
                return None
            else:
                value = int(value)
            if value >= minimum:
                return value
            else:
                print(f"Please enter a number greater than or equal to {minimum}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Gets data from ID 07E3 and stores it in the correct dataset
def process07E3(data, time):
    rollData['Time'].append(time)
    pitchData['Time'].append(time)
    yawData['Time'].append(time)
    throttleSpinData['Time'].append(time)

    rollData['Data'].append(struct.unpack('>h', bytes.fromhex(data[0] + data[1]))[0])
    pitchData['Data'].append(struct.unpack('>h', bytes.fromhex(data[2] + data[3]))[0])
    yawData['Data'].append(struct.unpack('>h', bytes.fromhex(data[4] + data[5]))[0])
    throttleSpinData['Data'].append(struct.unpack('>H', bytes.fromhex(data[6] + data[7]))[0])

    rollData['Type'].append('Input')
    pitchData['Type'].append('Input')
    yawData['Type'].append('Input')
    throttleSpinData['Type'].append('Hover')


# Gets data from ID 07E4 and stores it in the correct dataset
def process07E4(data, time):
    throttleSpinData['Time'].append(time)
    throttleSpinData['Time'].append(time)

    throttleSpinData['Data'].append(struct.unpack('>B', bytes.fromhex(data[0]))[0])
    throttleSpinData['Data'].append(struct.unpack('>h', bytes.fromhex(data[2] + data[3]))[0])

    throttleSpinData['Type'].append('Spin')
    throttleSpinData['Type'].append('Pusher')


# Gets float data and stores it in the correct dataset
def processFloat(data, time, dataDict, dataType):
    dataDict['Time'].append(time)
    dataDict['Data'].append(struct.unpack('>f', bytes.fromhex(data[0] + data[1] + data[2] + data[3]))[0])
    dataDict['Type'].append(dataType)


# Plots 3 types of data on the same x-axis.
# Type 1 data can be read on the left-hand axis, and types 2 and 3 on the right-hand axis.
# Limits of right-hand axis are sets by ylim.
def plot(data, title, type1, type2, type3, ylim=None):
    df = pd.DataFrame(data)
    dataScale1 = df[df['Type'].isin([type1])]
    dataScale2 = df[df['Type'].isin([type2, type3])]

    fig, ax1 = plt.subplots()
    try:
        ax1.xaxis.set_major_locator(MultipleLocator(data['Time'][-1] / 5))
    except IndexError:
        print("No data found. Please try again with more data.")
    ax2 = ax1.twinx()
    if ylim is not None:
        ax2.set_ylim(ylim[0], ylim[1])

    plt1 = sns.lineplot(data=dataScale1, x='Time', y='Data', color='green', ax=ax1)
    plt1.set_ylabel(type1)
    plt2 = sns.lineplot(data=dataScale2, x='Time', y='Data', hue='Type', ax=ax2)
    plt2.set_ylabel(type2 + type3)

    handles, labels = plt.gca().get_legend_handles_labels()
    handles.extend([Line2D([0], [0], label=type1, color='g', linestyle='-')])
    plt.legend(handles=handles, loc='lower left')
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    processCSV()
    plot(pitchData, "Pitch Data", "Input", "Angle", "Rate")
    plot(rollData, "Roll Data", "Input", "Angle", "Rate")
    plot(yawData, "Yaw Data", "Input", "Angle", "Rate")
    plot(throttleSpinData, "Throttle and Spin Data", "Spin", "Hover", "Pusher", [-32767, 32767])
