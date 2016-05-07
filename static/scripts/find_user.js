function FindUserPage(base_uri) {
    this.base_uri = base_uri;
}
FindUserPage.prototype.getUserData = function (request, user_id, jqueryList) {
    var opts = {
        user_id: user_id
    };
    $.post({
        url: this.base_uri + request,
        data: JSON.stringify(opts),
        success: function(dataFromServer) {
            // empty the list
            jqueryList.empty();
            // add the fetched data
            for (var ix = 0; ix < dataFromServer.data.length; ix++) {
                var item = dataFromServer.data[ix].obj;
                var divID = ix + "_" + item.id;
                jqueryList.append("<li class='col-md-12 user_favorites' onclick='playSound(\"" + divID + "\", \"" + item.id + "\")'>" + createSoundListItem(item, divID) + "</li>");
            }
        },
        contentType:"application/json",
        dataType: 'json'
    });
};
FindUserPage.prototype.getList = function (user_id, listSel, apiResourceName) {
    // Check if the data is already fetched
    var $list = $(listSel);
    if ($list && $list.children().length > 0) {
        // already fetched the data, toggle the visibility
        console.log("not fetching " + listSel + " data");
        if ($(listSel + ":first-child").is(':visible')) {
            // hide the children
            $list.children().each(function() {
                $(this).hide();
            });
        }
        else {
            // redisplay this children
            $list.children().each(function() {
                $(this).show();
            });
        }
    }
    else {
        // fetch the data
        console.log("fetching the user's " + listSel + " data");
        this.getUserData(
            apiResourceName,
            user_id,
            $list
        );
    }
};
// Get the user's favorite tracks or toggle the user's favorite track visibility
FindUserPage.prototype.getUserFavorites = function(user_id, listSel) {
    this.getList(user_id, listSel, 'user_favorites');
};
// Get the user's favorite playlists or toggle their favorite playlist visibility
FindUserPage.prototype.getUserPlaylists = function(user_id, listSel) {
    this.getList(user_id, listSel, 'user_playlists');
};
FindUserPage.prototype.setUserVisibility = function(jqueryListItem, selUserClass, userDetailsSel, userMusicDiv, showUser) {
    if (showUser) {
        // Remove the selected class
        jqueryListItem.addClass(selUserClass);
        // Hide the user's details
        jqueryListItem.find(userDetailsSel).show();
        // Hide the user's tracks and playlists
        jqueryListItem.find(userMusicDiv).show();
    }
    else {
        // Add the selected class
        jqueryListItem.removeClass(selUserClass);
        // Show the user's details
        jqueryListItem.find(userDetailsSel).hide();
        // Show the user's tracks and playlists
        jqueryListItem.find(userMusicDiv).hide();
    }
};
FindUserPage.prototype.selectUser = function(divID, itemID) {
    console.log("selecting user " + itemID);
    var prevSelected = $("ul#fetched_friends li div.selectedUser");
    var selectedUser = $("#" + divID);
    var selUserClass = 'selectedUser',
        userDetailsClass = 'user_details',
        userDetailsSel = 'div.' + userDetailsClass,
        userMusicDiv = 'div.user_music';
    if (prevSelected.length > 0 && prevSelected != selectedUser) {
        console.log('hiding previous user');
        this.setUserVisibility(prevSelected, selUserClass, userDetailsSel, userMusicDiv, false);
    }
    console.log('showing this user');
    this.setUserVisibility(selectedUser, selUserClass, userDetailsSel, userMusicDiv, true);
};
// create a list item for a user
FindUserPage.prototype.createUserListItem = function(item, divID) {
    var favoritesSel = "#" + divID + " div.favorite_tracks ul";
    var playlistsSel = "#" + divID + " div.playlists ul";
    var div =   "<div id='" + divID + "'>" +
            "<div class='row'>" +
                "<div>" +
                    "<span>" +
                        "<a href='" + item.permalink_url + "' target='_blank'>" +
                            "<img src='"+ item.avatar_url + "' alt='" + item.username + " avatar '>" +
                            " " + item.username +
                        "</a>" +
                    "</span>" +
                    "<button class='btn btn-default' style='float: right' onclick='page.getUserPlaylists(\"" + item.id + "\", \"" + playlistsSel + "\"); return true;'>favorite playlists</button>" +
                    "<button class='btn btn-default' style='float: right' onclick='page.getUserFavorites(\"" + item.id + "\", \"" + favoritesSel + "\"); return true;'>favorite tracks</button>" +
                "</div>" +
            "<div class='col-md-6 user_details'>";
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
            "<div class='row user_music'>" +
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
};