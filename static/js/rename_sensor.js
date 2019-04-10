// $( document ).ready(function() {
//
//     $(".fa-edit").click(function(e) {
//         e.stopPropagation();
//         $(this).parent().hide();
//         $(this).parent().closest("div").append("" +
//             "<div class=\"field has-addons has-text-centered\">\n" +
//             "  <div class=\"control\">\n" +
//             "    <input class=\"input\" type=\"text\" placeholder=\"nouveau nom\">\n" +
//             "  </div>\n" +
//             "  <div class=\"control\">\n" +
//             "    <a class=\"button is-success\">\n" +
//             "      <i class=\"fas fa-check\"></i>\n" +
//             "    </a>\n" +
//             "    <a class=\"button is-danger\" onclick=\"cancelRename()\">\n" +
//             "      <i class=\"fas fa-times\"></i>\n" +
//             "    </a>\n" +
//             "  </div>\n" +
//             "</div>");
//
//     });
//
// });

document.addEventListener("DOMContentLoaded", function (event) {

    var edits = document.getElementsByClassName('fa-edit');
    for (var i = 0; i < edits.length; i++) {

        var edit = edits[i];
        edit.onclick = function () {

            this.parentNode.style.display = 'none';
            this.parentNode.prepend("<div>test</div>");
        }
    }
});