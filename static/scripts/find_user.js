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
                jqueryList.append("<li class='col-md-12 user_favorites'>" + createSoundListItem(item, divID) + "</li>");
            }
            // Prevent the list item from shrinking when the track is clicked
            jqueryList.children('li').click(function(e) {
                playSound($(this).children("div").first().attr('id'), $(this).find("div.sound_list_item").first().attr('id'));
                return false;
            });
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

/**
 * Select a user from the list.
 *
 * If there is a previously selected user and that user is not equal to the currently
 * selected user OR the previous user is equal to the selected user and no button click
 * occurred
 *    Then hide the previously selected user
 *
 * If the selected user is not equal to the previously selected user and
 * 1. there was no button press or 2. the user is currently not expanded
 *    Then expand the user details
 *
 * Remove the "button clicked" class from the previously clicked button (if there was one)
 * Remove the "button clicked" class from the currently clicked button (if one was clicked)
 *
 * @param divID ID of the selected user
 */
FindUserPage.prototype.selectUser = function(divID) {
    var prevSelected = $("ul#fetched_friends li div.selectedUser");
    var selectedUser = $("#" + divID);
    var selUserClass = 'selectedUser',
        userDetailsClass = 'user_details',
        userDetailsSel = 'div.' + userDetailsClass,
        userMusicDiv = 'div.user_music';
    var hasPrev = (prevSelected.length > 0);
    var prevButton = prevSelected.find("button.btn-clicked");
    var prevBtnClicked = (prevButton.length > 0);
    var prevIsCur = (hasPrev && prevSelected.attr('id') == selectedUser.attr('id'));
    var curButton = selectedUser.find("button.btn-clicked");
    var curBtnClicked = (curButton.length > 0);

    //console.log("prev is cur " + prevIsCur + ", prevBtnClicked = " + prevBtnClicked + ", curBtnClicked = " + curBtnClicked);
    if (!prevIsCur || (prevIsCur && !prevBtnClicked)) {
        //console.log("removing prev user");
        this.setUserVisibility(prevSelected, selUserClass, userDetailsSel, userMusicDiv, false);
    }

    //console.log("visible details: " + selectedUser.find(userDetailsSel).is(":visible"));
    if (!prevIsCur && (!curBtnClicked || !selectedUser.find(userDetailsSel).is(":visible"))) {
        //console.log("showing user");
        this.setUserVisibility(selectedUser, selUserClass, userDetailsSel, userMusicDiv, true);
    }

    if (prevBtnClicked) {
        //console.log("removing attribute from prev sel");
        prevButton.removeClass("btn-clicked");
    }
    if (curBtnClicked) {
        //console.log("removing attribute from cur sel");
        curButton.removeClass("btn-clicked");
    }
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
                    "<button class='btn btn-default' style='float: right' onclick='page.getUserPlaylists(\"" + item.id + "\", \"" + playlistsSel + "\"); return true;'>playlists</button>" +
                    "<button class='btn btn-default' style='float: right' onclick='page.getUserFavorites(\"" + item.id + "\", \"" + favoritesSel + "\"); return true;'>favorite tracks</button>" +
                "</div>" +
            "<div class='user_details'>";
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
                "<div class='playlists col-md-5'>" +
                    "<h3>User playlists</h3>" +
                    "<ul></ul>" +
                "</div>" +
            "</div>" +
        "</div>";
    return div;
};