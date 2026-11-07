/* =========================================================
   湾区（广东）数字经济研究院 — 全站脚本（无动画版本，优化首屏加载）
   ========================================================= */
(function () {
  "use strict";

  /* ---------- 导航：滚动加深背景 ---------- */
  var header = document.querySelector(".site-header");
  function syncHeader() {
    if (!header) return;
    if (window.scrollY > 40) header.classList.add("is-solid");
    else header.classList.remove("is-solid");
  }
  window.addEventListener("scroll", syncHeader, { passive: true });
  syncHeader();

  /* ---------- 移动端菜单 ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.classList.remove("is-open");
        document.body.style.overflow = "";
      });
    });
  }

  /* ---------- 列表分页（研究院动态每页6篇 / 行业资讯每页4篇） ---------- */
  var grid = document.getElementById("news-grid") || document.getElementById("inews-grid");
  var prevBtn = document.getElementById("page-prev");
  var nextBtn = document.getElementById("page-next");
  if (grid && prevBtn && nextBtn) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll("[data-page]"));
    var perPage = parseInt(grid.getAttribute("data-perpage") || "6", 10);
    var curEl = document.getElementById("page-current");
    var totalEl = document.getElementById("page-total");
    var pages = Math.max(1, Math.ceil(cards.length / perPage));
    if (totalEl) totalEl.textContent = pages;
    var current = 1;
    function render() {
      cards.forEach(function (c, idx) {
        c.style.display = (Math.floor(idx / perPage) + 1 === current) ? "" : "none";
      });
      if (curEl) curEl.textContent = current;
      prevBtn.disabled = current === 1;
      nextBtn.disabled = current === pages;
    }
    prevBtn.addEventListener("click", function () {
      if (current > 1) { current--; render(); window.scrollTo({ top: 0 }); }
    });
    nextBtn.addEventListener("click", function () {
      if (current < pages) { current++; render(); window.scrollTo({ top: 0 }); }
    });
    render();
  }

  /* ---------- 页脚年份 ---------- */
  var year = document.getElementById("footer-year");
  if (year) year.textContent = new Date().getFullYear();
})();
