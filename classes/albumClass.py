from classes.playlistClass import playlistClass

class albumClass :

    def __init__(self,spotify):
        # Init elements #
        self.spotify=spotify
        self.reject_fields = [
            "available_markets",
            "external_urls",
            "href",
            "images",
            "album_type",
            "release_date_precision",
            "uri",
            "type",
        ]



    def get_new_album_ids(self,country=None,filter_by_your_top_genres='N',limit=20):
        """
        Get all the album ids from the last x new albums. It doesn't include single-only releases OR any genres you've marked as reject.
        """

        # If country is defined, it filter by country otherwise will search worldwide
        if country is None :
            new = self.spotify.new_releases(limit=limit)["albums"]["items"]
        else :
            new = self.spotify.new_releases(limit=limit, country=country.upper() )["albums"]["items"]


        new.sort(key=lambda x: x["release_date"], reverse=True)

        # Remove any albums that are single-only
        new_albums = [x for x in new if x["album_type"] == "album"]
        # print(new)

        # Remove any fields that we don't for the rest of the script
        for x in new_albums:
            for f in self.reject_fields:
                x.pop(f, None)

        # Filters the list of albums using an instance of ( playlistClass ) , first by user top genres, then by rejects list
        playlist = playlistClass(new_albums,self.spotify)

        # If user choose to filter by his top genres then .... FILTER BY YOUR TOP GENRES ( function filter_by_your_top_genres in playlistClass)
        # Upper force uppercase
        if filter_by_your_top_genres.upper() == 'Y' :
            playlist.filter_by_your_top_genres(new_albums)
        playlist.remove_rejects(new_albums)

        return playlist



    def get_track_ids_for_album(self,album_id):
        """
        Get the track ids for a single album.
        """
        # print(f"getting track ids for album {album_id}")
        album = self.spotify.album(album_id)

        # print(track_ids)
        return [x["id"] for x in album["tracks"]["items"]]

