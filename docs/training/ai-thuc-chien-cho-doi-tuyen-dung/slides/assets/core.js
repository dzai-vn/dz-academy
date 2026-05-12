(function () {
  const root = document.documentElement;
  const storageKey = "dz-template-theme";
  const systemThemeQuery = window.matchMedia("(prefers-color-scheme: dark)");
  const brandConfigs = {
    core: {
      label: "dz",
      logo: "dz-core.svg",
      logoAlt: "dz core master mark",
    },
    academy: {
      label: "dz-academy",
      logo: "dz-academy.svg",
      logoAlt: "dz academy master mark",
    },
    app: {
      label: "dz-app",
      logo: "dz-app.svg",
      logoAlt: "dz app master mark",
    },
    news: {
      label: "dz-news",
      logo: "dz-news.svg",
      logoAlt: "dz news master mark",
    },
  };

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
  }

  function getStoredTheme() {
    try {
      return localStorage.getItem(storageKey);
    } catch {
      return null;
    }
  }

  function setStoredTheme(theme) {
    try {
      localStorage.setItem(storageKey, theme);
    } catch {
      // ignore storage failures
    }
  }

  function resolveInitialTheme() {
    const explicit = root.getAttribute("data-theme");
    if (explicit === "dark" || explicit === "light") return explicit;

    const stored = getStoredTheme();
    if (stored === "dark" || stored === "light" || stored === "auto") return stored;

    return "auto";
  }

  function onMediaQueryChange(query, handler) {
    if (typeof query.addEventListener === "function") {
      query.addEventListener("change", handler);
      return;
    }

    if (typeof query.addListener === "function") {
      query.addListener(handler);
    }
  }

  function getEffectiveTheme(theme) {
    if (theme === "dark" || theme === "light") return theme;
    return systemThemeQuery.matches ? "dark" : "light";
  }

  function updateThemeControls(theme) {
    document.querySelectorAll("[data-theme-toggle]").forEach((toggle) => {
      const effectiveTheme = getEffectiveTheme(theme);
      const nextTheme = effectiveTheme === "dark" ? "light" : "dark";
      const icon = nextTheme === "dark" ? "☾" : "☀";

      toggle.dataset.nextTheme = nextTheme;
      toggle.setAttribute("aria-pressed", effectiveTheme === "dark" ? "true" : "false");
      toggle.setAttribute("aria-label", `Switch to ${nextTheme} theme`);
      toggle.setAttribute("title", `Switch to ${nextTheme} theme`);

      const iconNode = toggle.querySelector("[data-theme-icon]");
      if (iconNode) {
        iconNode.textContent = icon;
      }
    });
  }

  function bindThemeToggles(initialTheme) {
    let currentTheme = initialTheme;
    updateThemeControls(currentTheme);

    document.querySelectorAll("[data-theme-toggle]").forEach((toggle) => {
      toggle.addEventListener("click", () => {
        const nextTheme = toggle.dataset.nextTheme;
        if (nextTheme !== "dark" && nextTheme !== "light") return;

        currentTheme = nextTheme;
        applyTheme(currentTheme);
        setStoredTheme(currentTheme);
        updateThemeControls(currentTheme);
      });
    });

    onMediaQueryChange(systemThemeQuery, () => {
      const storedTheme = getStoredTheme();
      currentTheme = storedTheme === "dark" || storedTheme === "light" ? storedTheme : "auto";
      applyTheme(currentTheme);
      updateThemeControls(currentTheme);
    });
  }

  function initBrandSystem() {
    const context = root.getAttribute("data-brand-context") || "core";
    const config = brandConfigs[context] || brandConfigs.core;
    const assetBasePath = (root.getAttribute("data-brand-assets-path") || "../assets/01-logos/master").replace(/\/$/, "");
    const logoPath = `${assetBasePath}/${config.logo}`;

    document.querySelectorAll("[data-dz-brand-logo]").forEach((logo) => {
      logo.setAttribute("src", logoPath);
      logo.setAttribute("alt", config.logoAlt);
    });

    document.querySelectorAll("[data-dz-footer-brand]").forEach((node) => {
      node.textContent = config.label;
    });

    document.querySelectorAll("[data-dz-footer-owner]").forEach((node) => {
      node.textContent = "Vô Tận Đăng";
    });

    document.querySelectorAll("[data-dz-footer-site]").forEach((node) => {
      node.textContent = "dz-ai.vn";
    });
  }

  function initPagedShell() {
    const paged = document.querySelector("[data-dz-shell='paged']");
    if (!paged) return;

    const pages = Array.from(paged.querySelectorAll(".dz-page"));
    const prev = paged.querySelector("[data-dz-prev]");
    const next = paged.querySelector("[data-dz-next]");
    const indexLabel = paged.querySelector("[data-dz-page-index]");
    const progressBar = paged.querySelector("[data-dz-progress]");
    let index = 0;

    pages.forEach((page, pageIndex) => {
      if (!page.id) {
        page.id = `page-${pageIndex + 1}`;
      }
    });

    function getIndexFromHash() {
      const hash = window.location.hash.replace("#", "");
      if (!hash) return 0;
      const nextIndex = pages.findIndex((page) => page.id === hash);
      return nextIndex >= 0 ? nextIndex : 0;
    }

    function render() {
      pages.forEach((page, pageIndex) => {
        page.classList.toggle("is-active", pageIndex === index);
        page.setAttribute("aria-hidden", pageIndex === index ? "false" : "true");
      });

      if (prev) prev.disabled = index === 0;
      if (next) next.disabled = index === pages.length - 1;
      if (indexLabel) indexLabel.textContent = `${index + 1} / ${pages.length}`;
      if (progressBar) {
        progressBar.style.width = `${((index + 1) / pages.length) * 100}%`;
      }

      const activePage = pages[index];
      if (activePage) {
        history.replaceState(null, "", `#${activePage.id}`);
      }
    }

    function go(delta) {
      const nextIndex = Math.max(0, Math.min(index + delta, pages.length - 1));
      if (nextIndex === index) return;
      index = nextIndex;
      render();
    }

    if (prev) prev.addEventListener("click", () => go(-1));
    if (next) next.addEventListener("click", () => go(1));

    window.addEventListener("keydown", (event) => {
      const tagName = document.activeElement?.tagName;
      if (tagName === "INPUT" || tagName === "TEXTAREA" || document.activeElement?.isContentEditable) return;
      if (event.key === "ArrowLeft") go(-1);
      if (event.key === "ArrowRight") go(1);
    });

    window.addEventListener("hashchange", () => {
      const nextIndex = getIndexFromHash();
      if (nextIndex === index) return;
      index = nextIndex;
      render();
    });

    index = getIndexFromHash();
    render();
  }

  function initVerticalShell() {
    const shell = document.querySelector("[data-dz-shell='vertical']");
    if (!shell) return;

    const links = Array.from(shell.querySelectorAll(".dz-vertical__nav-link"));
    const sections = links
      .map((link) => document.querySelector(link.getAttribute("href")))
      .filter(Boolean);

    if (!sections.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const id = `#${entry.target.id}`;
          const link = links.find((item) => item.getAttribute("href") === id);
          if (!link) return;

          link.classList.toggle("is-active", entry.isIntersecting);
          if (entry.isIntersecting) {
            link.setAttribute("aria-current", "true");
          } else {
            link.removeAttribute("aria-current");
          }
        });
      },
      {
        rootMargin: "-25% 0px -55% 0px",
        threshold: 0.1,
      }
    );

    sections.forEach((section) => observer.observe(section));
  }

  const initialTheme = resolveInitialTheme();
  applyTheme(initialTheme);
  bindThemeToggles(initialTheme);
  initBrandSystem();
  initPagedShell();
  initVerticalShell();
})();
