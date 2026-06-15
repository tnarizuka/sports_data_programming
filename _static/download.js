(function () {
  function notebookFilename(link) {
    try {
      var url = new URL(link.getAttribute("href"), window.location.href);
      return url.pathname.split("/").pop() || "notebook.ipynb";
    } catch (error) {
      return "notebook.ipynb";
    }
  }

  function enableNotebookDownloads() {
    var selector = [
      'a.btn-download-notebook-button[href$=".ipynb"]',
      'a.btn-download-source-button[href$=".ipynb"]'
    ].join(",");

    document.querySelectorAll(selector).forEach(function (link) {
      link.setAttribute("download", notebookFilename(link));
      link.removeAttribute("target");
      link.setAttribute("rel", "noopener");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enableNotebookDownloads);
  } else {
    enableNotebookDownloads();
  }
})();
