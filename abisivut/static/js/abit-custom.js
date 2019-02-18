$(document).ready( function() {
    console.log("Penis");

    $(window).on("load", function() {
        $('#loading').fadeOut(400);
    });

    document.getElementById("video").onloadeddata = function () {
        $(this).fadeIn();
    };

    $("#errormsg").hide();

    $("body").on("scroll", function () {
        var anchor = $("#rieha").offset().top + 100;
        if ($("body").scrollTop() > anchor || $(document).scrollTop() > anchor) {
            $("header").css("text-shadow", "none");
            $("#header-background").fadeIn("slow");
            $("header a").css("color", "lightblue");
        } else {
            $("header").css("text-shadow", "0 2px 10px rgba(0, 0, 0, 0.8");
            $("header a").css("color", "white");
            $("#header-background").fadeOut("slow");
        }
    });
});