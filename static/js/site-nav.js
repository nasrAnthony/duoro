(function () {
    const body = document.body;
    const header = document.querySelector(".site-header");
    const nav = document.querySelector(".site-nav");
    const toggle = document.querySelector(".site-nav-toggle");
    const links = document.getElementById("site-nav-links");
    const scrim = document.querySelector(".site-nav-scrim");

    if (!body || !header || !nav || !toggle || !links || !scrim) {
        return;
    }

    let ticking = false;

    const updateHeaderState = () => {
        ticking = false;
        header.classList.toggle("is-stuck", window.scrollY > 4);
    };

    const requestHeaderUpdate = () => {
        if (!ticking) {
            ticking = true;
            window.requestAnimationFrame(updateHeaderState);
        }
    };

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
    updateHeaderState();
    window.addEventListener("scroll", requestHeaderUpdate, { passive: true });

    window.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeMenu();
        }
    });
})();
