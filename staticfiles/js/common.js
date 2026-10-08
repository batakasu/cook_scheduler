const main = document.querySelector("main");
const pageTopButton = document.getElementById("page-top");

main.addEventListener("scroll", function () {
    if (main.scrollTop > (main.clientHeight * 0.8)) {
        pageTopButton.style.display = "block";
    } else {
        pageTopButton.style.display = "none";
    }
});

pageTopButton.addEventListener("click", function () {
    main.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});