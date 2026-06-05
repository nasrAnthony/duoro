(function () {
    const body = document.body;
    const nav = document.querySelector(".site-nav");
    const toggle = document.querySelector(".site-nav-toggle");
    const links = document.getElementById("site-nav-links");
    const scrim = document.querySelector(".site-nav-scrim");

    if (!body || !nav || !toggle || !links || !scrim) {
        return;
    }

    const closeMenu = () => {
        nav.classList.remove("site-nav-open");
        body.classList.remove("site-menu-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open navigation menu");
    };

    const openMenu = () => {
        nav.classList.add("site-nav-open");
        body.classList.add("site-menu-open");
        toggle.setAttribute("aria-expanded", "true");
        toggle.setAttribute("aria-label", "Close navigation menu");
    };

    toggle.addEventListener("click", () => {
        if (nav.classList.contains("site-nav-open")) {
            closeMenu();
            return;
        }

        openMenu();
    });

    scrim.addEventListener("click", closeMenu);

    window.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeMenu();
        }
    });
})();
