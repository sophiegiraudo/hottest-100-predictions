import requests
import os
import time
"""
You need to set your API key as environment variable. Do not hardcode the API key, they expire and you 
will be left wondering why the program that worked yesterday is now broken. 

To set the environment variable on a *nix system open a terminal and type:

export SPOTIFY_KEY=<YOUR-API-KEY>

To set the environment variable on a windows computer open command prompt and type:

set SPOTIFY_KEY=<YOUR-API-KEY>


"""

start_time = time.time()
access_token = os.environ.get("SPOTIFY_KEY")
headers = {"Authorization":"Bearer {}".format(access_token)}

# Dictionary containing the spotify IDs for the playlists to be analysed.
playlists = {"2012":"0ATly1Vhu2JLUggKJ4Kp1P"}

# , "2017":"5vSiOmiS1UflyJkPBfMvqP", "2016": "5nSPdyDCKD4VzEuBDP5X25", "2018":"1hlmJOyuxrfPZi8XvuURbT", "2018":"1hlmJOyuxrfPZi8XvuURbT"

if(not access_token):
    print("You don't have an API token set as an environment variable dummy")

for playlist in playlists.keys():
    playlist_id = playlists[playlist]
    
    file = open(playlist + ".csv", "w")
    print("Name\tAlbum\tRank\tArtist\tTrack_id\tDuration\tExplicit\tPopularity\tDanceability\tEnergy\tKey\tLoudness\tMode\tSpeechiness\tAcousticness\tInstrumentalness\tValence\tLiveness\tTempo\tTime_Signature", file=file)
    r = requests.get("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks?fields=items(track(name,artists(name),album(name),duration_ms,popularity,explicit,id))", headers = headers)
    
    if(r.status_code != 200):
        print("You have a problem there fella, HTTP Error Code: " + str(r.status_code))
        if(r.status_code == 401):
            print("401s mean you were unauthorised, this is typically an API token problem. Refresh your token and reset the environment variable")
        exit()
    items = r.json()["items"]

    for i in range(len(items)):
        track = items[i]["track"]
        song_name = track["name"]
        album_name = track["album"]["name"]
        rank = 100 - i
        artist_array = track["artists"]
        artists = ""
        for i in range(len(artist_array)):
            if(i == len(artist_array) - 1):
                artists += artist_array[i]["name"]
            else:
                artists += artist_array[i]["name"] + ", "
        track_id = track["id"]
        duration = track["duration_ms"]
        explicit = track["explicit"]
        popularity = track["popularity"]

        features_request = requests.get("https://api.spotify.com/v1/audio-features/" + track_id, headers = headers)
        track_features = features_request.json()

        danceability = track_features["danceability"]
        energy = track_features["energy"]
        key = track_features["key"]
        loudness = track_features["loudness"]
        mode = track_features["mode"]
        speechiness = track_features["speechiness"]
        acousticness = track_features["acousticness"]
        instrumentalness = track_features["instrumentalness"]
        valence = track_features["valence"]
        liveness = track_features["liveness"]
        tempo = track_features["tempo"]
        time_signature = track_features["time_signature"]

        print(song_name + "\t" + album_name + "\t" + str(rank) + "\t" + str(artists) + "\t" + track_id + "\t" + str(duration) + "\t" + str(explicit) + "\t" + str(popularity) +
        "\t" + str(danceability) + "\t" + str(energy) + "\t" + str(key) + "\t" + str(loudness) + "\t" + str(mode) + "\t" + str(speechiness) + "\t" + str(acousticness) + "\t" + str(instrumentalness) + "\t" 
        + str(valence) + "\t" + str(liveness) + "\t" + str(tempo) + "\t" + str(time_signature), file = file)
    print("Done playlist: " + playlist)
    print("Time since we started: " + str(time.time() - start_time))
        


print("All done amigo")
print("Total Time: " + str(time.time() - start_time))
