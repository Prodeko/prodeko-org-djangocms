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


    function removeReceiptName(e) {
        e.target.parentElement.previousElementSibling.value = "";
        $(e.target.parentElement).remove();
    }

    function showFileName(e) {
        var input = e.srcElement;
        var filename = input.files[0].name;

        var span = document.createElement("span");
        span.classList.add("form-text", "receipt-name", "pr-2");
        span.innerHTML = `<i id="removeReceptIcon" class="fas fa-times fa-lg pr-2" style="color: #b12321; vertical-align: middle;"></i> ${filename}`;
        span.firstElementChild.addEventListener("click", removeReceiptName);

        parent = input.parentNode;
        if (parent.children.length > 2) {
            parent.removeChild(parent.children[2]);
        }
        parent.appendChild(span);
    }

    document.getElementById("id_receipt").addEventListener("change", showFileName); 


    var formApply = $("#form_apply");
    formApply.on("submit", function (e) {
        e.preventDefault();
        formData = new FormData((formApply).get(0));

        $.ajax({
            url: "",
            type: "POST",
            data: formData,
            contentType: false, // Indicates 'multipart/form-data'
            processData: false,
            success: function (data) {
                document.write(data);
            },

            // Re-renders the same page with error texts.
            error: function (xhr, errmsg, err) {
                if (xhr.status === 599) {
                    $("#form-apply-wrapper").replaceWith(xhr.responseText);
                    document.getElementById("id_receipt").addEventListener("change", showFileName);
                }
            }
        });
    });
});