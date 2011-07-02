function getNearbyLunchRemarks() {
    console.log("getting nearby restaurants")
    var coordinate =  { lon: 139.761146, lat : 35.670842 };
    navigator.geolocation.getCurrentPosition(
        function(pos){
            coordinate.lon = pos.coords.longitude;
            coodrinate.lat = pos.coords.latitude;
        },
        function(error){
            console.log("Your geolocation was not able to be retrieved!")
        }
    );

    $.getJSON(
        "http://lunkaku.appspot.com/list",
        coordinate,
        function(data, status){
            var items = [];
            $.each(data, function(key, val) {
                       items.push(
                           '<li>' +
                               '<a href="' + "url/comes/here" + '">' +
                               '<img src="' + val.image + '" />' +
                               '<p>' + val.content + '</p>' +
                               '</a>' +
                           '</li>'
                       );
            });
            var joined = items.join('');
            $('#result').html(joined);
    });
}
