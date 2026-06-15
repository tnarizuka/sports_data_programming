(function () {
  function downloadFilename(link) {
    try {
      var url = new URL(link.getAttribute("href"), window.location.href);
      return url.pathname.split("/").pop() || "source";
    } catch (error) {
      return "source";
    }
  }

  function enableSourceDownloads() {
    var selector = [
      "a.btn-download-notebook-button[href]",
      "a.btn-download-source-button[href]"
    ].join(",");

    document.querySelectorAll(selector).forEach(function (link) {
      link.setAttribute("download", downloadFilename(link));
      link.removeAttribute("target");
      link.setAttribute("rel", "noopener");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enableSourceDownloads);
  } else {
    enableSourceDownloads();
  }
})();
