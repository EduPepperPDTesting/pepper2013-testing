function EmbedEdivate() {}

EmbedEdivate.prototype.embed = function(element_name, assest_id) {
    var firstName = '';
    var lastName = '';
    var email = '';
    var secret = '';
    $.get("/user-info", function(data) {
        firstName = data.first_name;
        lastName = data.last_name;
        email = data.email;
        secret = data.secret;
    });
    if (email && secret) {
        var hash = md5(email + secret);
        var embed_code = '<iframe frameborder="0" scrolling="no" width="800" height="450" src="https://www.pd360.com/partners/EmbeddedPlayer/player.cfm?ncesid=12345&group=MantecaUnified&email=';
        embed_code += email;
        embed_code += '&fname=';
        embed_code += firstName;
        embed_code += '&lname=';
        embed_code += lastName;
        embed_code += '&md5=';
        embed_code += hash;
        embed_code += '&contentid=';
        embed_code += assest_id;
        embed_code += '"></iframe>';
        $('#' + element_name).append(embed_code);
    }
};
