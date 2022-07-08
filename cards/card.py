import requests
import sqlalchemy as db
import pandas as pd
import urllib.request
import climage
from rich.console import Console
from rich.table import Table
import time
from rich.progress import track


# Returns a list of keys
def getList(d):
    return list(d.keys())


# Returns the nested dictionary from a key
def nestedGet(dic, keys):
    for key in keys:
        dic = dic[key]
    return dic


# Returns dictionary from API data
def createAPIData(url):
    response = requests.get(url)
    data = response.json()
    return data


# Returns the user full name
def getName(d):
    v = d["name"]
    if v is None:
        return "User has no name!"
    return v


# Returns number of repos
def getNumOfRepos(d):
    v = d["public_repos"]
    if v is None:
        return "User has no repos!"
    return v


# Returns location of user
def getLocation(d):
    v = d["location"]
    if v is None:
        return "User has no location!"
    return v


# Returns user profile pic image address
def getAvatar(d):
    v = d["avatar_url"]
    if v is None:
        return "User doesn't have profile avatar!"
    return v


# Returns number of followers
def getFollowers(d):
    v = d["followers"]
    if v is None:
        return "User has no followers!"
    return v


# Returns number of people they follow
def getFollowing(d):
    v = d["following"]
    if v is None:
        return "User doesn't follow anyone"
    return v


# Returns users bio
def getBio(d):
    v = d["bio"]
    if v is None:
        return "User doesn't have bio!"
    return v


# Returns users email
def getContact(d):
    v = d["email"]
    if v is None:
        return "User doesn't have email!"
    return v


# Returns the birth of the account
def getYears(d):
    v = d["created_at"]
    if v is None:
        return
    return v


# Opens avatar image
def openImage(url):
    urllib.request.urlretrieve(url, "avatar.png")
    output = climage.convert("avatar.png", width=50)
    print(output)


# Returns relevent data from getUserData
def filterUserData(d):
    filter_dict = {
        "Name": [getName(d)],
        "Followers": [getFollowers(d)],
        "Following": [getFollowing(d)],
        "Bio": [getBio(d)],
        "Location": [getLocation(d)],
        "Number of Repos": [getNumOfRepos(d)],
        "Contact": [getContact(d)],
    }
    return filter_dict


def createQuery(table_dict):
    # initialize dataframe
    df = pd.DataFrame.from_dict(table_dict, orient="index")
    engine = db.create_engine("sqlite:///data_base_name.db")

    # Creating query result
    df.to_sql("Github", con=engine, if_exists="replace", index=True)
    query_result = engine.execute("SELECT * FROM Github;").fetchall()

    return query_result


def createTable(data):
    console = Console()
    progressDisplay()
    print(" ")
    user_dict = filterUserData(data)
    openImage(getAvatar(data))
    query_result = createQuery(user_dict)

    table = Table(show_header=True, header_style="bold sea_green3")
    table.add_column(query_result[0][0], width=12)
    table.add_column(query_result[1][0], justify="right")
    table.add_column(query_result[2][0], justify="right")
    table.add_column(query_result[3][0], justify="right")
    table.add_column(query_result[4][0], justify="right")
    table.add_column(query_result[5][0], justify="right")
    table.add_column(query_result[6][0], justify="right")
    table.add_row(
        query_result[0][1],
        query_result[1][1],
        query_result[2][1],
        query_result[3][1],
        query_result[4][1],
        query_result[5][1],
        query_result[6][1],
    )

    console.print(table)


def progressDisplay():
    for i in track(range(5), description="[cyan]Processing..."):
        time.sleep(1)
    for j in track(range(4), description="[red]Don't panic, just count to infinity..."):
        time.sleep(1)
    for i in track(range(3), description="[green]Still there? ..."):
        time.sleep(1)


def main():
    console = Console()
    console.print("GITHUB PROFILE CARDS", style="bold sea_green3")
    console.print(
        "This programs gives overview of a github profile.", style="bold bright_white"
    )
    while True:

        user_input = input("Enter Github username: ")
        user_url = "https://api.github.com/users/{0}".format(user_input)
        data = createAPIData(user_url)

        if len(data) < 3:
            print("User Not Found")
            openImage(
                "https://cdn2.vectorstock.com/i/1000x1000/81/66/question-mark-and-background-vector-28488166.jpg"
            )

        else:
            createTable(data)

        user_input = input("Want to lookup someone else?(Y/N) ")
        if user_input == "N" or user_input == "n":
            break

    print(" ")
    console.print("Thank you for using Github Profile Cards", style="bold bright_white")


# main function
if __name__ == "__main__":
    main()
