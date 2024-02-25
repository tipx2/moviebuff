from flask import Flask, render_template
import requests
import json

API_KEY = open("apikey.txt", "r").read().strip("\n")

headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + API_KEY
}

def load_json(url):
    """loads json from a specified url into a python json object

    Args:
        url (string): api url to get the data from

    Returns:
        json object: json object containing the response
    """
    return json.loads(requests.get(url, headers=headers).text)

def search_actors(query):
    response = load_json(f"https://api.themoviedb.org/3/search/person?query={query}&include_adult=false&language=en-US&page=1")
    
    id_list = [(actor["id"], actor["name"]) for actor in response["results"]]
    return id_list

def get_actor_movies(actor_id):
    """returns a list of ids of the movies for the actor id passed in

    Args:
        actor_id (int): an actor id

    Returns:
        list: list of movie ids
    """
    response = load_json(f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?language=en-US")
    
    id_list = [movie["id"] for movie in response["cast"]] + [movie["id"] for movie in response["crew"]]
    return id_list

def get_common_movies(actor_id_list): # note -> for less api calls might have to refactor this to take in a list of lists of movie ids, and then just store the lists of movies with the actors when we retrieve them to place them on the board
    """takes in a list of actor ids and returns a list of common movie ids between them

    Args:
        actor_id_list (list): list of actor ids
    
    Returns:
        list: list of common movie ids between the actors passed in
    """
    movie_lists = [get_actor_movies(actor_id) for actor_id in actor_id_list]
    
    return list(set.intersection(*map(set, movie_lists))) # a bit of pythonic wizardry