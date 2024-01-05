var counterContainer = document.querySelector(".website-counter");

async function httpGetAsync() {
    fetch("https://43klfv7ft5.execute-api.us-east-1.amazonaws.com/updateVisitorCount", {
        mode: "cors"
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log(data);
            counterContainer.innerHTML = data;
        })
        .catch(error => console.error(error));
}

httpGetAsync();
