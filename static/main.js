function _getInputVal(prefix, id) {
    return $.trim($("input#" + prefix + "_" + id).val());
}
function _getCheckedRadioVal(divId) {
    var checked = $(divId + " input[type=radio]:checked");
    return $.trim(checked.val());
}
function getOptions(prefix) {
    if (prefix == 'track') {
        var opts = {
            query: _getInputVal(prefix, "search"),
            tags: _getInputVal(prefix, "tags"),
            visibility: _getCheckedRadioVal("#" + prefix + "_visibility"),
            license: _getCheckedRadioVal("#" + prefix + "_license"),
            bpmFrom: _getInputVal(prefix, "bpm_from"),
            bpmTo: _getInputVal(prefix, "bpm_to"),
            durationFrom: _getInputVal(prefix, "duration_from"),
            durationTo: _getInputVal(prefix, "duration_to"),
            createdAtFrom: _getInputVal(prefix, "created_at_from"),
            createdAtTo: _getInputVal(prefix, "created_at_to"),
            genres: _getInputVal(prefix, "genres"),
            type: _getCheckedRadioVal("#" + prefix + "_type")
        };
        return opts;
    }
    else {
        opts = {
            query: _getInputVal(prefix, "search")
        };
        return opts;
    }
}
function removeLastComma(str) {
    var s = str.trim();
    var ix = s.lastIndexOf(",");
    return s.substring(0, ix);
}
function _getSoundCloudPlayerIFrame(track_id) {
    var widgetParams = '&color=ff6600&auto_play=false';
    return '<iframe class="sc_iframe" src="http://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F' + track_id + widgetParams + '"></iframe>';
}
// Embed the SoundCloud player or toggle its visibility
function playSound(div_id, track_id) {
    var embed = $("#" + div_id + " div.sc_player_embed span.sc_player");
    if (embed.children("iframe").length == 0) {
        // Add the player since it's not there yet
        embed.append(_getSoundCloudPlayerIFrame(track_id));
    }
    else {
        // Toggle the visibility of the player
        (embed.is(':visible') ? embed.hide() : embed.show());
    }
}
// Get the user's favorite tracks or toggle the user's favorite track visibility
function getUserFavorites(item, divID) {

}
// create a list item for a track/playlist
function createSoundListItem(item, divID) {
    return "<div id='" + divID + "'>" +
                "<div>" +
                    "<h3>" + item.title + "</h3>" +
                    "<p>" + item.description + "</p>"  +
                "</div>" +
                "<div>" +
                    "<span>" +
                        "User " +
                        "<a href='" + item.user.permalink_url + "' target='_blank'>" +
                            item.user.username + " " +
                            "<img src='"+ item.user.avatar_url + "' alt='" + item.user.username + " avatar '>" +
                        "</a>" +
                    "</span><br />" +
                    "<span>Created: " + item.created_at + "</span><br />" +
                    "<span>Genre: " + item.genre + "</span><br />" +
                    "<span>Tags: " + item.tag_list + "</span>" +
                "</div>" +
                "<div class='sc_player_embed'>"+
                    "<span class='sc_player'></span>" +
                "</div>" +
            "</div>";
}
// create a list item for a user
function createUserListItem(item, divID) {
    var div =   "<div id='" + divID + "'>" +
                    "<div style='width:50%; float:left'>" +
                        "<span>" +
                            "<a href='" + item.permalink_url + "' target='_blank'>" +
                            "<img src='"+ item.avatar_url + "' alt='" + item.username + " avatar '>" +
                            " " + item.username +
                            "</a>" +
                        "</span>" +
                    "</div>" +
                    "<div style='width:50%; float:right'>";
    if (item.description)
        div +=  "<span> About: " + item.description + "</span><br />";
    if (item.full_name)
        div += "<span>Real Name: " + item.full_name + "</span><br />";
    div += "<span>Favorite Track Count: " + item.public_favorites_count + "</span><br />";
    if (item.website && item.website_title)
        div += "<span>Website: <a href='" + item.website + "'>" + item.website_title + "</a></span><br />";
    if (item.city)
        div += "<span>City: " + item.city + "</span><br />";
    if (item.country)
        div += "<span>Country: " + item.country + "</span><br />";
    div += "</div></div>";
    return div;
}
// query for friends (aka users) tracks and playlists
function fetchAndAddToList(url, prefix, jqueryList) {
    var options = getOptions(prefix);
    if (options.query.length > 0) {
        // reload the data based on the query string
        $.post({
            url: url, //base_uri + 'friends'/'tracks'/'playlists'
            data: JSON.stringify(options),
            success: function(dataFromServer) {
                // empty the list
                jqueryList.empty();
                // add the fetched data
                var playSound = (prefix != 'friend');
                for (var ix = 0; ix < dataFromServer.data.length; ix++) {
                    var item = dataFromServer.data[ix].obj;
                    var divID = ix + "_" + (playSound ? item.user.id : item.id) + "_" + item.id;
                    if (playSound) {
                        jqueryList.append("<li style='float:left;' onclick='playSound(\"" + divID + "\", \"" + item.id + "\"); return true;'>" + createSoundListItem(item, divID) + "</li>");
                    }
                    else {
                        jqueryList.append("<li style='width:50%' onclick='getUserFavorites(\"" + divID + "\", \"" + item.id + "\"); return true;'>" + createUserListItem(item, divID) + "</li>");
                    }
                }
            },
            contentType:"application/json",
            dataType: 'json'
        });
    }
}
