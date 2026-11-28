// Theme toggle + mobile menu (runs on every page). OWNER: R4.
(function () {
  var themeBtn = document.getElementById("theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var current = document.documentElement.getAttribute("data-theme") || "light";
      var next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem("lc-theme", next); } catch (e) { /* private mode */ }
    });
  }

  var mobileBtn = document.getElementById("mobile-toggle");
  var drawer = document.getElementById("mobile-drawer");
  if (mobileBtn && drawer) {
    mobileBtn.addEventListener("click", function () {
      var isOpen = drawer.classList.toggle("open");
      mobileBtn.setAttribute("aria-expanded", isOpen);
      drawer.setAttribute("aria-hidden", !isOpen);
    });
  }
})();
