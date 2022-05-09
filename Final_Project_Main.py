"""
Name: Robert DeMarco
CS230: Section 5
Data: ufo_sightins_8000_sample.csv
URL:

Description: This program analyzes the UFO dataset. It creates multiple charts and a map which can be used in order to analyze ufo data.
This analysis focuses almost entirely on within the United states because of the abundance of US UFO sightings.
"""
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk

# making dictionary for the rest of the project

ufodictionary = {}
ufofile = open("ufo_sightings_8000_sample.csv")
line = 0
lineararray = 0

x = 0
y = 0

# """
line = ufofile.readline()
while x < 8000:
    line = ufofile.readline()
    lineararray = line.split(",")
    ufodictionary[x] = lineararray
    x = x + 1


def piechart():  # this creates a piechart that shows the 5 states with the most sightings
    dictionaryofoccurances = {'state': [],
                              'occurences': []}

    # this section reads in the relevant parts of ufodictionary
    y = 0
    holder = 0
    secondholder = 0
    while y < 8000:
        holder = ufodictionary[y][2]
        if holder != "":
            if holder in dictionaryofoccurances['state']:
                secondholder = dictionaryofoccurances['state'].index(holder)
                dictionaryofoccurances['occurences'][secondholder] = dictionaryofoccurances['occurences'][
                                                                         secondholder] + 1
            else:
                dictionaryofoccurances['state'].append(holder)
                dictionaryofoccurances['occurences'].append(1)
        y = y + 1

    # this converts the data into a dataframe and deletes all but the top 5 states
    pandasstate = pd.DataFrame(dictionaryofoccurances)
    pandasstate = pandasstate.sort_values(by=["occurences"], ascending=False)
    pandasstate.drop(pandasstate.tail(62).index, inplace=True)

    # convertPandaback to 2 lists
    convertlist = pandasstate.values
    statelist = []
    occurancelist = []
    n = 0
    while n < len(convertlist):
        statelist.append(convertlist[n][0])
        occurancelist.append(convertlist[n][1])
        n = n + 1
    n = 0

    # plots pie graph
    fig, ax = plt.subplots()
    ax.pie(occurancelist, labels=statelist, autopct='%.1f%%')
    plt.title("Percent of Sightings for Top 5 States by Number of Occurrences")
    st.pyplot(fig)


def ufobyshape(x=10):  # this creates a bargraph that ranks the first x amount of shapes
    y = 0
    tail = 22 - (x)
    # dictionaryofshapes = {}
    dictionaryofshapes = {'Shape': [],
                          'occurences': []}
    # """
    holder = 0
    secondholder = 0
    # this section reads in the relevant parts of ufodictionary

    while y < 8000:
        holder = ufodictionary[y][4]
        if holder != "":
            if holder in dictionaryofshapes['Shape']:
                secondholder = dictionaryofshapes['Shape'].index(holder)
                dictionaryofshapes['occurences'][secondholder] = dictionaryofshapes['occurences'][secondholder] + 1
            else:
                dictionaryofshapes['Shape'].append(holder)
                dictionaryofshapes['occurences'].append(1)

        y = y + 1

    # this part uses pandas to sort the shapes by number of occurences
    pandasshapes = pd.DataFrame(dictionaryofshapes)
    pandasshapes = pandasshapes.sort_values(by=["occurences"], ascending=False)
    pandasshapes.drop(pandasshapes.tail(tail).index, inplace=True)

    # convertPandaback to 2 lists
    convertlist = pandasshapes.values
    shapelist = []
    occurancelist = []
    n = 0
    while n < len(convertlist):
        shapelist.append(convertlist[n][0])
        occurancelist.append(convertlist[n][1])
        n = n + 1
    n = 0
    # this is where the bar chart begins

    fig, ax = plt.subplots()
    ax.bar(shapelist, occurancelist, width=0.5, color=['g', "r", "c", "b", "y"])
    plt.xlabel("Shape")
    plt.ylabel("Number of Occurances")
    plt.title("Most Common Shapes for UFOs")
    st.pyplot(fig)


def ufostateyear(year="2000"):
    yeardictionary = {}
    y = 1
    holder = 0
    # this creates a dictionary of dictionaries that puts every states entries into a corresponding year dictionary
    while y < 8000:
        if "/" in ufodictionary[y][0]:
            x = ufodictionary[y][0].split("/")
            z = x[2].split(" ")
            yearholder = z[0]
            stateholder = ufodictionary[y][2]
            if stateholder != "":
                indexholder = 0
                if yearholder in yeardictionary:
                    if stateholder in yeardictionary[yearholder]["state"]:
                        indexholder = yeardictionary[yearholder]["state"].index(stateholder)
                        yeardictionary[yearholder]["occurances"][indexholder] = \
                        yeardictionary[yearholder]["occurances"][indexholder] + 1
                    else:
                        yeardictionary[yearholder]["state"].append(stateholder)
                        yeardictionary[yearholder]["occurances"].append(1)
                else:
                    yeardictionary[yearholder] = {"state": [], "occurances": []}
                    yeardictionary[yearholder]["state"].append(stateholder)
                    yeardictionary[yearholder]["occurances"].append(1)
        y = y + 1
        # this isolates the selected year
    newdictionary = {'state': [],
                     'occurances': []}
    n = 0
    while n < len(yeardictionary[year]["state"]):
        newdictionary['state'].append(yeardictionary[year]["state"][n])
        n = n + 1
    n = 0
    while n < len(yeardictionary[year]["occurances"]):
        newdictionary['occurances'].append(yeardictionary[year]["occurances"][n])
        n = n + 1

    # this sorts the data by alphabetical order
    stateyeardataframe = pd.DataFrame(newdictionary)
    stateyeardataframe = stateyeardataframe.sort_values(by=["state"], ascending=True)
    tail = len(stateyeardataframe) - 5
    stateyeardataframe.drop(stateyeardataframe.tail(tail).index, inplace=True)

    # converts stateyeardataframe back to list

    convertlist = stateyeardataframe.values
    statelist = []
    occurancelist = []
    n = 0
    statelist, occurancelist = conversion(convertlist, n)

    # creates graph
    plt.figure(figsize=(200, 200))
    fig, ax = plt.subplots()
    ax.bar(statelist, occurancelist, width=0.3, color=['r', "b", "y", "c", "g"])
    plt.xlabel("States")
    plt.ylabel("Number of Occurrences")
    plt.title("States With the Largest Number of Occurrences")
    st.pyplot(fig)


def ufoduration(minimumsecond=80, maximumsecond=300, state1="oh", state2="nc"):
    # this section reads in the relevant parts of ufodictionary

    durationdictionary = {'state': [],
                          'duration': []}
    y = 1
    while y < 8000:
        stateholder = ufodictionary[y][2]
        durationholder = ufodictionary[y][5]
        if stateholder != "":
            if durationholder != "":
                durationdictionary["state"].append(stateholder)
                durationdictionary["duration"].append(float(durationholder))

        y = y + 1

    durationpanda = pd.DataFrame(durationdictionary)
    durationpanda = durationpanda[
        (durationpanda["duration"] >= minimumsecond) & (durationpanda["duration"] <= maximumsecond) & (
            durationpanda["state"].isin([state1, state2]))]
    convertlist = durationpanda.values
    statelist = [state1, state2]
    occurancelist = [0, 0]

    z = 0
    while z < len(convertlist):
        if convertlist[z][0] == state1:
            occurancelist[0] = occurancelist[0] + 1
        else:
            occurancelist[1] = occurancelist[1] + 1
        z = z + 1

    fig, ax = plt.subplots()
    ax.bar(statelist, occurancelist, width=0.3, color=['r', "b"], )
    plt.xlabel("States")
    plt.ylabel("Amount of Sightings Between Parameters ")
    plt.title("State UFO Duration Analysis")
    st.pyplot(fig)


def californiamap():  # this def shows a map of ufo sightings in california
    mapdic = {"state": [],
              "longitude": [],
              "latitude": []}

    stateholder = 0
    longitudeholder = 0
    latitudeholder = 0
    y = 1
    # this creates a dictionary holding state latitude and longitude then sorts to california
    while y < 8000:
        stateholder = ufodictionary[y][2]
        longitudeholder = ufodictionary[y][10]
        latitudeholder = ufodictionary[y][9]
        if longitudeholder != 0 and latitudeholder != 0:
            mapdic["state"].append(stateholder)
            mapdic["longitude"].append(float(longitudeholder))
            mapdic["latitude"].append(float(latitudeholder))
        y = y + 1
    pandasus = pd.DataFrame(mapdic)
    pandascalifornia = pandasus[(pandasus["state"] == "ca")]
    # this creates a map
    st.map(pandascalifornia)


def conversion(convertlist, n):
    # this creates two corresponding state and occurance lists to display in a graph
    statelist = []
    occurancelist = []
    while n < len(convertlist):
        statelist.append(convertlist[n][0])
        occurancelist.append(convertlist[n][1])
        n = n + 1
    return statelist, occurancelist


# Streamlit stuff, all of this is the user interface
st.title("UFO Data Analysis")
st.text("Please select from the drop down menu what you want to do.")
st.image("seti.png", width=100)
maindropdown = st.selectbox("", (
"", "Most Common Shapes of UFO", "5 US states with most sightings", "Top 5 Occurances by Year",
"UFO Sighting duration analysis", "california sightings map"))

if maindropdown == "Most Common Shapes of UFO":
    xdropdown = st.selectbox("Please select whether you want the top 3,4 or 5 shapes for UFOs", ("", "3", "4", "5"))
    if xdropdown == "3":
        ufobyshape(3)
    elif xdropdown == "4":
        ufobyshape(4)
    elif xdropdown == "5":
        ufobyshape(5)
if maindropdown == "5 US states with most sightings":
    piechart()
if maindropdown == "Top 5 Occurances by Year":
    st.sidebar.header("Year Select")
    year = st.sidebar.select_slider("pick a year", [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010])
    if year == 2000:
        ufostateyear()
    if year == 2001:
        ufostateyear("2001")
    if year == 2002:
        ufostateyear("2002")
    if year == 2003:
        ufostateyear("2003")
    if year == 2004:
        ufostateyear("2004")
    if year == 2005:
        ufostateyear("2005")
    if year == 2006:
        ufostateyear("2006")
    if year == 2007:
        ufostateyear("2007")
    if year == 2008:
        ufostateyear("2008")
    if year == 2009:
        ufostateyear("2009")
    if year == 2010:
        ufostateyear("2010")

if maindropdown == "UFO Sighting duration analysis":
    minimum = 0
    maximum = 1000
    firststate = "oh"
    secondstate = "nc"

    tminimum = st.number_input("Minimum Duration Time in Seconds:", 0, 1000, key=1)
    if tminimum > maximum:
        st.warning("Your number is higher than the maximum!, please input a smaller number.")
        minimum = tminimum
    else:
        minimum = tminimum

    tmaximum = st.number_input("Maximum Duration Time in Seconds:", 0, 1000, key=2)
    if tmaximum < minimum:
        st.warning("Your number is smaller than the minimum!, please input a larger number.")
        maximum = tmaximum
    else:
        maximum = tmaximum

    # Allows you to input what states, this took a while to fill in
    firststate = st.selectbox("Please select your first state:", (
    "", "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi", "id", "il", "in", "ia", "ks", "ky", "ka",
    "me", "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nd", "oh", "ok", "or", "pa",
    "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy"), key=1)
    secondstate = st.selectbox("Please select your first state:", (
    "", "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi", "id", "il", "in", "ia", "ks", "ky", "ka",
    "me", "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nd", "oh", "ok", "or", "pa",
    "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy"), key=2)

    ufoduration(minimum, maximum, firststate, secondstate)

if maindropdown == "california sightings map":
    californiamap()

# """
