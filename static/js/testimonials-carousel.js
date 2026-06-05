const carousel = document.querySelector("[data-testimonial-carousel]");

if (carousel) {
    const track = carousel.querySelector(".testimonials-track");
    const slides = Array.from(carousel.querySelectorAll(".testimonial-card"));
    const prevButton = carousel.querySelector("[data-testimonial-prev]");
    const nextButton = carousel.querySelector("[data-testimonial-next]");
    const dotsWrap = carousel.querySelector(".testimonial-dots");
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let activeIndex = 0;
    let timerId;

    const dots = slides.map((_, index) => {
        const dot = document.createElement("button");
        dot.className = "testimonial-dot";
        dot.type = "button";
        dot.setAttribute("aria-label", `Show testimonial ${index + 1}`);
        dot.addEventListener("click", () => {
            showSlide(index);
            restart();
        });
        dotsWrap.appendChild(dot);
        return dot;
    });

    const showSlide = (index) => {
        activeIndex = (index + slides.length) % slides.length;
        track.style.transform = `translateX(-${activeIndex * 100}%)`;

        dots.forEach((dot, dotIndex) => {
            dot.classList.toggle("is-active", dotIndex === activeIndex);
            dot.setAttribute("aria-current", dotIndex === activeIndex ? "true" : "false");
        });
    };

    const next = () => showSlide(activeIndex + 1);
    const previous = () => showSlide(activeIndex - 1);

    const start = () => {
        if (reduceMotion) {
            return;
        }

        stop();
        timerId = window.setInterval(next, 5000);
    };

    const stop = () => {
        window.clearInterval(timerId);
    };

    const restart = () => {
        stop();
        start();
    };

    prevButton.addEventListener("click", () => {
        previous();
        restart();
    });

    nextButton.addEventListener("click", () => {
        next();
        restart();
    });

    carousel.addEventListener("mouseenter", stop);
    carousel.addEventListener("mouseleave", start);
    carousel.addEventListener("focusin", stop);
    carousel.addEventListener("focusout", start);

    showSlide(0);
    start();
}
