var signature;
//once sketeched, signatures saved and submit button enabled
document.addEventListener("sketched", (evt) => {
  evt.preventDefault();
  signature = evt.detail.signature;
  document.querySelector("#myButton").disabled = false;
});

//Once submitted - sends to flask app and adds notifications
form.addEventListener("submit", (event) => {
  event.preventDefault();
  send_form();
  const startTime = performance.now();
  var data = {};
  //POSTS signatures and receives metadata
  fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formdata),
  })
    .then((response) => response.json())
    .then((jsonData) => createdashboard(jsonData))
    .catch((error) => {
      console.error("Error sending data to Flask server:", error);
    });
});
