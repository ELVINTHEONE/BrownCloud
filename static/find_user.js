// Get the user's favorite tracks or toggle the user's favorite track visibility
function getUserFavorites(item, divID) {

}
// Get the user's favorite playlists or toggle their favorite playlist visibility
function getUserPlaylists(item, divID) {
    
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
    var div =   "<div id='" + divID + "'>" +
            "<div>" +
                "<span>" +
                    "<a href='" + item.permalink_url + "' target='_blank'>" +
                        "<img src='"+ item.avatar_url + "' alt='" + item.username + " avatar '>" +
                        " " + item.username +
                    "</a>" +
                "</span>" +
            "</div>" +
        "<div>";
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
    div += "</div></div>";
    return div;
}