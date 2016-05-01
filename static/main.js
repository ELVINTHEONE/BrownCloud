// create a list item for a track/playlist
function createSoundListItem(item, divID) {
    var div =   "<div id='" + divID + "'>" +
                "<div>" +
                    "<h3>" + item.title + "</h3>";
    if (item.description)
        div += "<p>" + item.description + "</p>";
    div += "</div>" +
                "<div>" +
                    "<span>" +
                        "User " +
                        "<a href='" + item.user.permalink_url + "' target='_blank'>" +
                            item.user.username + " " +
                            "<img src='"+ item.user.avatar_url + "' alt='" + item.user.username + " avatar '>" +
                        "</a>" +
                    "</span><br />" +
                    "<span>Created: " + item.created_at + "</span><br />";
    if (item.genre)
        div += "<span>Genre: " + item.genre + "</span><br />";
    if (item.tag_list)
        div += "<span>Tags: " + item.tag_list + "</span>";
    div += "</div>" +
                "<div class='sc_player_embed'>"+
                    "<span class='sc_player'></span>" +
                "</div>" +
            "</div>";
    return div;
}