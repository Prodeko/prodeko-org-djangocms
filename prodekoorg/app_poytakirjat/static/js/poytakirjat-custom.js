
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("download-button").addEventListener("click", function () {
        var spinner = document.createElement("div");
        spinner.classList.add("loader");

        console.log(this);
        this.innerHTML = "";
        this.appendChild(spinner);
    })
});
