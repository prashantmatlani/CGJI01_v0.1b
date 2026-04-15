
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
        
        console.log("📤 Rendering to UI:", data.content)

        appendMessage("assistant", data.content.trim())
		
        let formatted = data.content.replace(/\n/g, "<br>")
        appendMessage("assistant", formatted)
        
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
    thinking.innerHTML = `<strong>Agent Jung:</strong><br><br>Thinking...`
    thinking.style.marginBottom = "20px"

    chatBox.appendChild(thinking)
}

function removeThinking(){
    const thinking = document.getElementById("thinking")
    if(thinking) thinking.remove()
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

    if(role === "user"){
        msg.innerHTML = `<span class="label-client">Client:</span><br><br>${text}`
        msg.className = "user-msg"
    } else {
        msg.innerHTML = `<span class="label-agent">Agent Jung:</span><br><br>${text}`
        msg.className = "ai-msg"
    }

    chatBox.appendChild(msg)

    chatBox.scrollTop = chatBox.scrollHeight
}


// Preserve Paragraph Breaks
function formatText(text){
    return text.replace(/\n/g, "<br>")
}

// End session
async function endSession(){

    console.log("🛑 Ending session")

    await fetch(window.location.origin + "/chat",{
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