function getUserData(request, user_id, jqueryList) {
    var base_uri = "http://brown-cloud.herokuapp.com/";
    var opts = {
        user_id: user_id
    };
    $.post({
        url: base_uri + request,
        data: JSON.stringify(opts),
        success: function(dataFromServer) {
            // empty the list
            jqueryList.empty();
            // add the fetched data
            for (var ix = 0; ix < dataFromServer.data.length; ix++) {
                var item = dataFromServer.data[ix].obj;
                var divID = ix + "_" + item.id;
                jqueryList.append("<li class='col-md-6' onclick='playSound(\"" + divID + "\", \"" + item.id + "\"); return true;'>" + createSoundListItem(item, divID) + "</li>");
            }
        },
        contentType:"application/json",
        dataType: 'json'
    });
}
// Get the user's favorite tracks or toggle the user's favorite track visibility
function getUserFavorites(user_id, ulID) {
    getUserData(
        'user_favorites',
        user_id,
        $("ul." + ulID)
    );
}
// Get the user's favorite playlists or toggle their favorite playlist visibility
function getUserPlaylists(user_id, ulID) {
    getUserData(
        'user_playlists',
        user_id,
        $("ul." + ulID)
    );
}
function selectUser(item, divID) {
    var prevSelected = $("ul#fetched_friends li.selectedUser");
    var selUserClass = 'selectedUser';
    if (prevSelected.length > 0) {
        // Remove the selected class and the buttons
        prevSelected.removeClass(selUserClass);
    }
    var selectedUser = $("#" + divID);
    selectedUser.addClass(selUserClass);
}
// create a list item for a user
function createUserListItem(item, divID) {
    var favoritesSel = "#" + divID + " ul.favorite_tracks";
    var playlistsSel = "#" + divID + " ul.favorite_playlists";
    var div =   "<div id='" + divID + "'>" +
            "<div class='row'>" +
                "<div class='col-md-6'>" +
                    "<span>" +
                        "<a href='" + item.permalink_url + "' target='_blank'>" +
                            "<img src='"+ item.avatar_url + "' alt='" + item.username + " avatar '>" +
                            " " + item.username +
                        "</a>" +
                    "</span>" +
                    "<input type=['button'] style='float: right' value='favorite tracks' onclick='getUserFavorites(\"" + item.id + "\", \"" + favoritesSel + "\")'/><br />" +
                    "<input type=['button'] style='float: right' value='favorite playlists' onclick='getUserPlaylists(\"" + item.id + "\", \"" + playlistsSel + "\")'/><br />" +
                "</div>" +
            "<div class='col-md-6'>";
        if (item.description)
            div +=  "<span> About: " + item.description + "</span><br />";
        if (item.full_name)
            div += "<span>Real Name: " + item.full_name + "</span><br />";
        if (item.public_favorites_count > 0)
            div += "<span>Favorite Track Count: " + item.public_favorites_count + "</span><br />";
        div += "<span>Tracks Created: " + item.track_count + "</span><br />";
        div += "<span>Playlists Created: " + item.playlist_count + "</span><br />";
        div += "<span>Followers: " + item.followers_count + "</span><br />";
        div += "<span>Following: " + item.followings_count + "</span><br />";
        if (item.website && item.website_title)
            div += "<span>Website: <a href='" + item.website + "'>" + item.website_title + "</a></span><br />";
        if (item.city)
            div += "<span>City: " + item.city + "</span><br />";
        if (item.country)
            div += "<span>Country: " + item.country + "</span><br />";
        div +=  "</div>" +
            "</div>" +
            "<div class='row'>" +
                "<div class='favorite_tracks col-md-6'>" +
                    "<h3>Favorite tracks</h3>" +
                    "<ul></ul>" +
                "</div>" +
                "<div class='playlists col-md-6'>" +
                    "<h3>User playlists</h3>" +
                    "<ul></ul>" +
                "</div>" +
            "</div>" +
        "</div>";
    return div;
}