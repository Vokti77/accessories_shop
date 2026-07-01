// ;(function () {
//   const modal = new bootstrap.Modal(document.getElementById("modal"))

//   htmx.on("htmx:afterSwap", (e) => {
//     // Response targeting #dialog => show the modal
//     if (e.detail.target.id == "dialog") {
//       modal.show()
//     }
//   })

//   htmx.on("htmx:beforeSwap", (e) => {
//     // Empty response targeting #dialog => hide the modal
//     if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
//       modal.hide()
//       e.detail.shouldSwap = false
//     }
//   })

//   // Remove dialog content after hiding
//   htmx.on("hidden.bs.modal", () => {
//     document.getElementById("dialog").innerHTML = ""
//   })
// })()

function init_widgets_for_htmx_element(target) {
  // init other widgets

  // init modal dialogs
  if (target.tagName === 'DIALOG') {
      target.showModal();
      htmx.on('.close-dialog', 'click', function(event) {
          var dialog = htmx.find('dialog[open]');
          dialog.close();
          htmx.remove(dialog);
      });
  }
}

htmx.onLoad(init_widgets_for_htmx_element);