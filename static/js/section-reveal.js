(function () {
    const sections = document.querySelectorAll(".reveal-section");

    if (!sections.length) {
        return;
    }

    let hasStarted = false;

    const startReveal = () => {
        if (hasStarted) {
            return;
        }

        hasStarted = true;

        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            sections.forEach((section) => section.classList.add("is-visible"));
            return;
        }

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                    } else {
                        entry.target.classList.remove("is-visible");
                    }
                });
            },
            {
                threshold: 0.22,
                rootMargin: "0px 0px -6% 0px",
            }
        );

        sections.forEach((section) => observer.observe(section));
    };

    if (document.documentElement.classList.contains("site-loader-complete")) {
        startReveal();
    } else {
        window.addEventListener("duoro:loader-complete", startReveal, { once: true });
    }
})();
