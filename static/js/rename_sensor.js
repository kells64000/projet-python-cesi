$( document ).ready(function() {

    $(".fa-edit").click(function(e) {
        e.stopPropagation();
        $(this).parent().hide();
        $(this).parent().closest("div").append("" +
            "<div class=\"field has-addons has-text-centered\">\n" +
            "  <div class=\"control\">\n" +
            "    <input class=\"input\" type=\"text\" placeholder=\"nouveau nom\">\n" +
            "  </div>\n" +
            "  <div class=\"control\">\n" +
            "    <a class=\"button is-success\">\n" +
            "      <i class=\"fas fa-check\"></i>\n" +
            "    </a>\n" +
            "    <a class=\"button is-danger\" onclick=\"cancelRename()\">\n" +
            "      <i class=\"fas fa-times\"></i>\n" +
            "    </a>\n" +
            "  </div>\n" +
            "</div>");

    });

});

function cancelRename() {

    var edits = $('.fa-edit').parent();

    edits.each(function(e) {

        console.log(e);

    });
}
