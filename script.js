const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

function addMessage(text, sender) {
const message = document.createElement("div");
message.classList.add("message", sender);
message.textContent = text;

chatBox.appendChild(message);
chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
const text = userInput.value.trim();

if (text === "") return;

addMessage(text, "user");

userInput.value = "";

// Fake AI response for now
setTimeout(() => {
addMessage("I'm still learning! Soon I'll be connected to my Python brain. 🤖", "ai");
}, 700);
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", function (event) {
if (event.key === "Enter") {
sendMessage();
}
});
