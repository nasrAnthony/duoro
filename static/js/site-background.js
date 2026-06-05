(function () {
    const background = document.getElementById("site-background");

    if (!background) {
        return;
    }

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    let ticking = false;

    const update = () => {
        ticking = false;

        if (reducedMotion.matches) {
            background.style.setProperty("--site-bg-back-y", "0px");
            background.style.setProperty("--site-bg-front-y", "0px");
            return;
        }

        const frameHeight = background.offsetHeight || window.innerHeight;
        const progress = Math.min(Math.max(window.scrollY / frameHeight, 0), 1);
        const backOffset = Math.round(progress * frameHeight * 0.32);
        const frontOffset = Math.round(progress * frameHeight * 0.1);

        background.style.setProperty("--site-bg-back-y", `${backOffset}px`);
        background.style.setProperty("--site-bg-front-y", `${frontOffset}px`);
    };

    const requestUpdate = () => {
        if (!ticking) {
            ticking = true;
            window.requestAnimationFrame(update);
        }
    };

    update();
    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);
    reducedMotion.addEventListener("change", requestUpdate);
})();
