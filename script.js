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
  
// Send message to backend
fetch("/api/chat", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({ message: text })
})
.then(res => res.json())
.then(data => {
addMessage(data.reply, "ai");
})
.catch(err => {
addMessage("Oops! Couldn't reach the server. 😅", "ai");
console.error(err);
});

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", function (event) {
if (event.key === "Enter") {
sendMessage();
}
});
