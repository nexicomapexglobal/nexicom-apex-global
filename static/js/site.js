document.addEventListener("DOMContentLoaded", () => {
    const menuButton = document.querySelector(".menu-btn");
    const header = document.querySelector(".header");
    const nav = document.querySelector("nav");

    const closeNavigation = () => {
        header?.classList.remove("open");
        nav?.classList.remove("open");
        menuButton?.setAttribute("aria-expanded", "false");
    };

    menuButton?.addEventListener("click", () => {
        header?.classList.toggle("open");
        nav?.classList.toggle("open");

        const isOpen = nav?.classList.contains("open") || false;
        menuButton.setAttribute("aria-expanded", String(isOpen));
    });

    nav?.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", closeNavigation);
    });

    document.addEventListener("click", event => {
        if (
            nav?.classList.contains("open") &&
            !nav.contains(event.target) &&
            !menuButton?.contains(event.target)
        ) {
            closeNavigation();
        }
    });

    const updateHeader = () => {
        header?.classList.toggle("scrolled", window.scrollY > 18);
    };

    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });

    const revealElements = document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        revealObserver.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.1,
                rootMargin: "0px 0px -40px 0px"
            }
        );

        revealElements.forEach(element => revealObserver.observe(element));
    } else {
        revealElements.forEach(element => element.classList.add("visible"));
    }

    const counters = document.querySelectorAll("[data-counter]");

    const animateCounter = element => {
        const rawValue = element.dataset.counter || "0";
        const numberMatch = rawValue.match(/[\d,]+/);
        const target = numberMatch
            ? Number(numberMatch[0].replace(/,/g, ""))
            : 0;

        const prefix = numberMatch
            ? rawValue.slice(0, numberMatch.index)
            : "";

        const suffix = numberMatch
            ? rawValue.slice(
                  (numberMatch.index || 0) + numberMatch[0].length
              )
            : "";

        if (!Number.isFinite(target) || target <= 0) {
            element.textContent = rawValue;
            return;
        }

        const duration = 1250;
        const startTime = performance.now();

        const update = currentTime => {
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(target * eased);

            element.textContent =
                prefix +
                current.toLocaleString("en-IN") +
                suffix;

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                element.textContent = rawValue;
            }
        };

        requestAnimationFrame(update);
    };

    if ("IntersectionObserver" in window) {
        const counterObserver = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        counterObserver.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.4 }
        );

        counters.forEach(counter => counterObserver.observe(counter));
    } else {
        counters.forEach(animateCounter);
    }

    document.querySelectorAll('a[href^="#"], a[href^="/#"]').forEach(link => {
        link.addEventListener("click", event => {
            const href = link.getAttribute("href") || "";
            const hashIndex = href.indexOf("#");

            if (hashIndex === -1) {
                return;
            }

            const targetId = href.slice(hashIndex);

            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (!target) {
                return;
            }

            event.preventDefault();

            const headerHeight = header?.offsetHeight || 0;
            const targetPosition =
                target.getBoundingClientRect().top +
                window.scrollY -
                headerHeight -
                18;

            window.scrollTo({
                top: targetPosition,
                behavior: "smooth"
            });
        });
    });

    const backToTop = document.createElement("button");
    backToTop.type = "button";
    backToTop.className = "back-to-top";
    backToTop.setAttribute("aria-label", "Back to top");
    backToTop.textContent = "↑";
    document.body.appendChild(backToTop);

    const toggleBackToTop = () => {
        backToTop.classList.toggle("show", window.scrollY > 650);
    };

    toggleBackToTop();
    window.addEventListener("scroll", toggleBackToTop, { passive: true });

    backToTop.addEventListener("click", () => {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
});
