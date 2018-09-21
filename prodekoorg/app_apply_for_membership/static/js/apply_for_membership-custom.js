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

        $.ajax({
            url: "apply/",
            type: "POST",
            data: formData,
            contentType: false, // Indicates 'multipart/form-data'
            success: function (data) {
                console.log(data);
                console.log("success");
                document.write(data);
            },

            // Re-renders the same page with error texts.
            error: function (xhr, errmsg, err) {
                console.log(xhr)
                if(xhr.status === 599) {
                    $("#form-apply-wrapper").replaceWith(xhr.responseText);
                }
            }
        });
    });
});