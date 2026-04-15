
// Front-end JavaScript - app.js

console.log("app.js loaded")

// -------------------------------
// INITIAL TRIGGER (Run Analysis)
// -------------------------------
async function runAnalysis(){

    const inputBox = document.getElementById("initial_input")
    const text = inputBox.value

    console.log("🚀 Run Analysis:", text)

    if(!text) return

    // Create session once
    if(!window.session_id){
        window.session_id = Math.random().toString(36).substring(7)
    }

    // Show user message
    appendMessage("user", text)

    // Show "Thinking..."
    showThinking()

    inputBox.value = ""

    // Disable Run Analysis permanently after first use
    document.querySelector('button[onclick="runAnalysis()"]').disabled = true

    await sendToBackend(text)
}


// -------------------------------
// FOLLOW-UP (Send button)
// -------------------------------
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


// -------------------------------
// BACKEND CALL (SHARED)
// -------------------------------
async function sendToBackend(text){

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

        //const data = await res.json()

        //console.log("✅ RESPONSE:", data)
        
        const data = await res.json()

        removeThinking()

        // Format text (single line breaks)
        const formatted = data.content.replace(/\n+/g, "<br>")

        // Render agent response
        appendMessage("assistant", formatted)

        // 🔥 HANDLE CHOICE TYPE
        if(data.type === "choice"){
            renderChoices(data.choices)
        }
        
        
        // Replace "Thinking..." with formatted response
        updateThinking(data.content)
        
        // Store agent memory if present
        if(data.agent_log){
            const agent = data.agent_log.agent
            window.agentMemory[agent] = data.agent_log.history
            updateAgentBox(agent, data.agent_log.history)
        }
        
        
    }catch(err){
        console.error("❌ ERROR:", err)
        removeThinking()
        appendMessage("assistant", "Error: server not reachable")
    }
}

// -------------------------------
// NEXT AGENT SELECTION
// -------------------------------

function renderChoices(choices){

    const chatBox = document.getElementById("chat")

    const container = document.createElement("div")
    container.className = "choice-container"

    choices.forEach(choice => {
        const btn = document.createElement("button")

        btn.innerText = choice.label
        btn.className = "choice-btn"

        btn.onclick = () => {
            handleAgentSelection(choice.id)
            container.remove() // remove buttons after click
        }

        container.appendChild(btn)
    })

    chatBox.appendChild(container)
    chatBox.scrollTop = chatBox.scrollHeight
}

// -------------------------------
// HANDLE NEXT AGENT SELECTION
// -------------------------------

function handleAgentSelection(agentId){

    console.log("🧭 Selected agent:", agentId)

    // Send agent selection as special message
    sendToBackend(`__agent__:${agentId}`)

    showThinking()
}

// -------------------------------
// SHOW "THINKING..."
// -------------------------------
function showThinking(){

    const chatBox = document.getElementById("chat")

    const thinking = document.createElement("div")
    thinking.id = "thinking"
    thinking.className = "ai-msg"

    thinking.innerHTML = `
        <span class="label-agent">Agent Jung:</span>
        <br><br>
        Thinking...
    `

    chatBox.appendChild(thinking)
}


// -------------------------------
// REPLACE "THINKING..." WITH RESPONSE
// -------------------------------
function updateThinking(text){

    const thinking = document.getElementById("thinking")

    // Format text (preserve paragraphs)
    //const formatted = text.replace(/\n/g, "<br><br>")
    const formatted = text.replace(/\n+/g, "<br>")

    if(thinking){
        thinking.innerHTML = `
            <span class="label-agent">Agent Jung:</span>
            <br><br>
            ${formatted}
        `
        thinking.id = ""  // remove id so next cycle works cleanly
    }
}


// -------------------------------
// REMOVE THINKING (fallback)
// -------------------------------
function removeThinking(){
    const thinking = document.getElementById("thinking")
    if(thinking) thinking.remove()
}


// -------------------------------
// RENDER USER MESSAGE ONLY
// -------------------------------
function appendMessage(role, text){

    const chatBox = document.getElementById("chat")

    const msg = document.createElement("div")

    if(role === "user"){
        msg.innerHTML = `
            <span class="label-client">Client:</span>
            <br><br>
            ${text}
        `
        msg.className = "user-msg"
    }

    // ❗ IMPORTANT:
    // We DO NOT render assistant here anymore
    // Assistant is handled ONLY via updateThinking()

    chatBox.appendChild(msg)

    chatBox.scrollTop = chatBox.scrollHeight
}


// -------------------------------
// UPDATE AGENT BOX
// -------------------------------

function updateAgentBox(agent, history){

    const box = document.getElementById(agent)
    if(!box) return

    let html = ""

    history.forEach(entry => {
        if(entry.role === "client"){
            html += `<b>Client:</b> ${entry.text}<br><br>`
        } else {
            html += `<b>Agent:</b> ${entry.text}<br><br>`
        }
    })

    box.innerHTML = html
}


// -------------------------------
// END SESSION
// -------------------------------
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