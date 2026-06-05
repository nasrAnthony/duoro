(function () {
    const loader = document.querySelector("[data-site-loader]");

    if (!loader) {
        return;
    }

    if (document.documentElement.classList.contains("site-loader-skip")) {
        loader.remove();
        document.documentElement.classList.add("site-loader-complete");
        window.dispatchEvent(new CustomEvent("duoro:loader-complete"));
        return;
    }

    const minimumVisibleTime = 2050;
    const startedAt = performance.now();

    const finish = () => {
        const elapsed = performance.now() - startedAt;
        const delay = Math.max(0, minimumVisibleTime - elapsed);

        window.setTimeout(() => {
            loader.classList.add("is-loaded");
            document.documentElement.classList.add("site-loader-complete");
            window.dispatchEvent(new CustomEvent("duoro:loader-complete"));

            try {
                sessionStorage.setItem("duoro-loader-seen", "true");
            } catch (error) {
                // The loader can still complete if sessionStorage is unavailable.
            }

            window.setTimeout(() => {
                loader.remove();
            }, 460);
        }, delay);
    };

    if (document.readyState === "complete") {
        finish();
    } else {
        window.addEventListener("load", finish, { once: true });
    }
})();
