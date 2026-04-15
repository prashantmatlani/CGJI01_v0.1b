

// Front-end JavaSscript - app.js

console.log("🔥 app.js loaded")

async function chat(){
    console.log("🚀 chat triggered")

    const res = await fetch("http://localhost:8000/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            session_id:"test123",
            message:"hello"
        })
    })

    const data = await res.json()
    console.log("✅ RESPONSE:", data)
}


function removeLastMessage(){
    const thinking = document.getElementById("thinking")
    if(thinking) thinking.remove()
}

// Chat Renderer

function appendMessage(role, text){

const chatBox = document.getElementById("chat")

const msg = document.createElement("div")

msg.className = role === "user" ? "user-msg" : "ai-msg"

msg.innerText = text

chatBox.appendChild(msg)

chatBox.scrollTop = chatBox.scrollHeight
}

// End session

async function endSession(){
    await fetch("http://localhost:8000/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            session_id: window.session_id,
            message: "end session"
        })
    })
    window.session_id = null
    document.getElementById("chat").innerHTML = ""
}