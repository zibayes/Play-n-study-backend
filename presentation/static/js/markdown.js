let width = $("#content").width() - 35;
document.querySelectorAll(".fromMarkdown").forEach((elem) => elem.innerHTML = elem.textContent.replace("img", "img style=\"max-width:" + width + "px;\""));
