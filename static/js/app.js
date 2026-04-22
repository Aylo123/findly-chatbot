// DOM ачаалсны дараа ажиллана
document.addEventListener("DOMContentLoaded", function () {

    const msgInput = document.getElementById("msg");
    const chatBox = document.getElementById("chat");
    const typing = document.getElementById("typing");

    // ENTER дарахад илгээх
    msgInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            send();
        }
    });

    // SEND function
    window.send = function () {
        let msg = msgInput.value;

        if (msg.trim() === "") return;

        // User message
        chatBox.innerHTML += "<p><b>Та:</b> " + msg + "</p>";

        // Typing харуулах
        typing.style.display = "block";

        fetch(`/chat?message=${msg}`)
            .then(res => res.json())
            .then(data => {

                setTimeout(() => {

                    typing.style.display = "none";

                    // 🔥 newline → <br>
                    let response = data.response.replace(/\n/g, "<br>");

                    // Bot response
                    chatBox.innerHTML += "<p><b>Findly:</b> " + response + "</p>";

                    // 🔥 Auto scroll
                    chatBox.scrollTop = chatBox.scrollHeight;

                }, 800);

            });

        // Input clear
        msgInput.value = "";
    };

});