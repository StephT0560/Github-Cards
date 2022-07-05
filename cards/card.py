import requests
import sqlalchemy as db
import pandas as pd
import urllib.request
import climage
from PIL import Image

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

#Returns the user full name
def getName(d):
    v = d['name']
    if v is None:
        return "User has no name!"
    return v

#Returns number of repos
def getNumOfRepos(d):
    v = d['public_repos']
    if v is None:
        return "User has no repos!"
    return v

#Returns location of user
def getLocation(d):
    v = d['location']
    if v is None:
        return "User has no location!"
    return v

#Returns user profile pic image address
def getAvatar(d):
    v = d['avatar_url']
    if v is None:
        return "User doesn't have profile avatar!"
    return v

#Returns number of followers 
def getFollowers(d):
    v = d['followers']
    if v is None:
        return "User has no followers!"
    return v
    
#Returns number of people they follow
def getFollowing(d):
    v = d['following']
    if v is None:
        return "User doesn't follow anyone"
    return v

#Returns users bio
def getBio(d):
    v = d['bio']
    if v is None:
        return "User doesn't have bio!"
    return v

#Returns users email
def getContact(d):
    v = d['email']
    if v is None:
        return "User doesn't have email!"
    return v

#Returns the birth of the account
def getYears(d):
    v = d['created_at']
    if v is None:
        return
    return v

#Opens avatar image 
def openImage(url):
    urllib.request.urlretrieve(url,"avatar.png")
    output = climage.convert('avatar.png')
    print(output)

#Returns relevent data from getUserData
def filterUserData(d):
    filter_dict = { 
      "Name":[getName(d)],
      "Followers":[getFollowers(d)],
      "Following":[getFollowing(d)],
      "Bio":[getBio(d)],
      "Location":[getLocation(d)],
      "Number of Repos":[getNumOfRepos(d)],
      "Contact":[getContact(d)]
    }
    return filter_dict
  
def createTable(table_dict):
    #initialize dataframe 
    df = pd.DataFrame.from_dict(table_dict,orient='index')
    engine = db.create_engine("sqlite:///data_base_name.db")

    #Create table
    df.to_sql("Github", con=engine, if_exists="replace", index=True)
    query_result = engine.execute("SELECT * FROM Github;").fetchall()
    return pd.DataFrame(query_result)

def createUserCard(data):
    user_dict = filterUserData(data)
    openImage(getAvatar(data))
    print(createTable(user_dict))


def main():
    #Ask for user input: 'username'
    user_input = input("Enter Github username: ")
    user_url = "https://api.github.com/users/{0}".format(user_input)
    data = createAPIData(user_url)
    if len(data) < 3:
        return print("User Not Found")
    
    #Create a card for user in data set
    createUserCard(data)
    

#main function 
if __name__ == "__main__":
    main()


