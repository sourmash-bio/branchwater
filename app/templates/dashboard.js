function prepare_dashboard(route, formdata) {
      //Once data submitted, add notification and send data to flask app

        if (!form.checkValidity()) {
          form.reportValidity(); // native browser popup
          document.getElementById("myButton").disabled = false;
          return;
        }

        document.querySelector("#myButton").disabled = true;

        // Create a new <nav> element
        const navElement = document.createElement("nav");
        navElement.classList.add(
          "navbar",
          "navbar-expand-lg",
          "navbar-light",
          "bg-light"
        );
        navElement.style.textAlign = "center"; // Add the text-align style

        // Create a new <p> element and add it to the <nav> element
        const paragraphElement = document.createElement("h2");
        paragraphElement.contentEditable = true; // Make the text editable
        paragraphElement.textContent =
          "Do not navigate from page. The query may take up to 5 minutes!"; // Set the initial text content
        navElement.appendChild(paragraphElement);
        // Add an event listener to the <p> element to handle text changes
        paragraphElement.addEventListener("input", (event) => {
          console.log(`New text: ${event.target.textContent}`);
        });
        // Add the <nav> element to the DOM
        dashboard.appendChild(navElement);

        const startTime = performance.now();
        var data = {};

        const MAX_NB_RETRY = 5;
        const RETRY_DELAY_MS = 200;

        async function fetchRetry(input, init) {
            let retryLeft = MAX_NB_RETRY;
            while (retryLeft > 0){
                try {
                    return await fetch(input, init);
                }
                catch (err) {
                    // TODO: callback to update UI with retry count?
                    await sleep(RETRY_DELAY_MS)
                }
                finally {
                    retryLeft -= 1;
                }
            }
            throw new Error(`Too many retries`);
        }

        function sleep(delay){
            return new Promise((resolve) => setTimeout(resolve, delay));
        }

        //Do fetch request to proper route and create dashboard
        fetchRetry(route, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formdata),
        })
          .then((response) =>  {
            // TODO: update UI to say we have the results
            console.log("got the data!")
            return response.json()
          })
          .then((jsonData) => {
            // TODO: update UI to say we are generating graphs
            console.log("preparing the graphs!")
            createdashboard(jsonData, paragraphElement, navElement)
          })
          .catch((error) => {
            // TODO: update UI to say request failed =(
            console.log("oops, request failed =(")
            console.error("Error sending data to Flask server:", error);
          });
}
