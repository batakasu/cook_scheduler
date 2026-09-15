const pageTopButton = document.getElementById("page-top");

window.addEventListener("scroll", function () {
    if (window.scrollY > (window.innerHeight + 100)) {
        pageTopButton.style.display = "block";
    } else {
        pageTopButton.style.display = "none";
    }
});

pageTopButton.addEventListener("click", function () {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});