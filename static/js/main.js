document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!confirm(form.dataset.confirm)) event.preventDefault();
    });
  });
  document.querySelectorAll("[data-auto-dismiss]").forEach((item) => {
    window.setTimeout(() => item.classList.add("fade-away"), 4500);
  });
});
