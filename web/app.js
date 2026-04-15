
// Front-end JavaScript - app.js

console.log("🔥 app.js loaded")

//  Initial Trigger - Run Analysis
async function runAnalysis(){

    const inputBox = document.getElementById("initial_input")
    const text = inputBox.value

    console.log("🚀 Run Analysis:", text)

    if(!text) return

    if(!window.session_id){
        window.session_id = Math.random().toString(36).substring(7)
    }

    appendMessage("user", text)
    showThinking()

    inputBox.value = ""
	
	//document.querySelector("button").disabled = true
	document.querySelector('button[onclick="runAnalysis()"]').disabled = true
	
    await sendToBackend(text)
}

// Follow-up (loop) - Send
async function sendFollowup(){

    const inputBox = document.getElementById("followup_input")
    const text = inputBox.value

    console.log("📨 Follow-up:", text)

    if(!text) return

    appendMessage("user", text)
    showThinking()

    inputBox.value = ""

    await sendToBackend(text)
}

// Shared Backend Call
async function sendToBackend(text){
    
    //const API_URL = "http://localhost:8000/chat"
    const API_URL = window.location.origin + "/chat"
    
    console.log("📡 Sending to backend:", text)
    
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

        console.log("✅ RESPONSE:", data)

        //removeThinking()
		//appendMessage("assistant", data.content)
		
		// replace Thinking instead of removing
		updateThinking(data.content)

    }catch(err){
        console.error("❌ ERROR:", err)
        removeThinking()
        appendMessage("assistant", "Error: server not reachable")
    }
}

// Thinking UI
function showThinking(){
    const chatBox = document.getElementById("chat")

    const thinking = document.createElement("div")
    thinking.id = "thinking"
    thinking.className = "ai-msg"
    thinking.innerText = "Thinking..."

    chatBox.appendChild(thinking)
}


function updateThinking(text){
    const thinking = document.getElementById("thinking")
    if(thinking){
        thinking.innerText = text
        thinking.id = ""  // remove id so next thinking can be created fresh
    } else {
        appendMessage("assistant", text)
    }
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