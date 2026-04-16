


// Front-end JavaScript - app.js

console.log("🔥 app.js loaded")

async function chat(){

    console.log("🚀 chat() triggered")

    const inputBox = document.getElementById("input")
    const chatBox = document.getElementById("chat")

    const text = inputBox.value

    console.log("Input box:", inputBox)
    console.log("User text:", text)

    if(!text) return

    const API_URL = "http://localhost:8000/chat"

    // generate session id if not exists
    if(!window.session_id){
        window.session_id = Math.random().toString(36).substring(7)
    }

    // append user message
    appendMessage("user", text)

	console.log("📡 Sending to backend:", text)
	
    // 🔥 SHOW LOADING
    const thinkingMsg = document.createElement("div")
    thinkingMsg.className = "ai-msg"
    thinkingMsg.innerText = "Thinking..."
    thinkingMsg.id = "thinking"

    chatBox.appendChild(thinkingMsg)   // ✅ FIXED

    inputBox.value = ""

    try{
        const res = await fetch(API_URL,{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                session_id: window.session_id,
                message: text
            })
        })
		
		
        const data = await res.json()

        console.log("✅ API RESPONSE:", data)

        // 🔥 REMOVE "Thinking..."
        removeThinking()

        // append AI response
        appendMessage("assistant", data.content)

    }catch(err){
        console.error("❌ FETCH ERROR:", err)
        removeThinking()
        appendMessage("assistant", "Error: Could not reach server")
    }
}


// remove thinking safely
function removeThinking(){
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

    console.log("🛑 Ending session")

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