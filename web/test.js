SendPost = (data) => {
    body_data = JSON.stringify(data);
    fetch("/requests/single-download", {
        method: "POST",
        headers: {'Content-Type': 'application/json', "Content-Length": body_data.length},
        body: body_data
    }).then(res => {
        console.log("Request Complete! response: ", res)
    });
};

//TODO rename this
TestButton = () => {
    url_paragraph = document.getElementById("video-url");

    data = {url: url_paragraph.innerHTML};
    SendPost(data);
};