// Bookshelf Practice App: two small helpers. The pages work without this file.

// 1. Show times in the reader's own time zone (the server sends UTC).
document.querySelectorAll("time[datetime]").forEach((element) => {
  const when = new Date(element.getAttribute("datetime"));
  if (!Number.isNaN(when.getTime())) {
    element.title = element.textContent;
    element.textContent = when.toLocaleString(undefined, {
      year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
    });
  }
});

// 2. Ask before risky actions (cancel an order, reset all data).
document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!window.confirm(form.dataset.confirm)) {
      event.preventDefault();
    }
  });
});
