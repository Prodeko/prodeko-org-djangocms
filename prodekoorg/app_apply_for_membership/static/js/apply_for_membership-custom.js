$(document).ready(function () {

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    var formApply = $("#form_apply");
    formApply.on("submit", function (e) {
        e.preventDefault();
        formData = JSON.stringify(formApply.serializeArray());
        console.log(formData)

        $.ajax({
            url: "apply/",
            type: "POST",
            data: formData,
            contentType: false, // Indicates 'multipart/form-data'
            success: function (data) {
                $("#form-apply-wrapper").replaceWith("Success!");
                console.log(data);
                console.log("success");
            },

            // Re-renders the same page with error texts.
            error: function (xhr, errmsg, err) {
                console.log(xhr)
                $("#form-apply-wrapper").replaceWith(xhr.responseText);
            }
        });
    });
});