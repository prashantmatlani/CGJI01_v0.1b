
// Front-end JavaScript - app.js

console.log("app.js loaded")

// -------------------------------
// GLOBAL STATE
// -------------------------------
window.conversationStarted = false

// Global memory store for agents
window.agentMemory = {}

// ---------------------------------------------------------
// INITIAL TRIGGER - Fire (Start Conversation; Run Analysis)
// ---------------------------------------------------------
//async function runAnalysis(){
async function fire(){

    const inputBox = document.getElementById("initial_input")
    const text = inputBox.value

    //console.log("🚀 Run Analysis:", text)

    if(!text) return

    // Create session once
    if(!window.session_id){
        window.session_id = Math.random().toString(36).substring(7)
    }

    // Mark conversation started
    window.conversationStarted = true

    // UI changes
    switchToConversationMode()

    // Show user message
    appendMessage("user", text)

    // Show "Thinking..."
    showThinking()

    inputBox.value = ""

    // Disable Run Analysis permanently after first use
    //document.querySelector('button[onclick="runAnalysis()"]').disabled = true

    await sendToBackend(text)
}


// -----------------------------------------------------
// FUEL - FOLLOW-UP (Continue Conversation; Send button)
// -----------------------------------------------------
//async function sendFollowup(){
async function fuel(){

    //const inputBox = document.getElementById("followup_input")
    const inputBox = document.getElementById("main_input")
    const text = inputBox.value

    //console.log("📨 Follow-up:", text)

    if(!text) return

    // Show user message
    appendMessage("user", text)

    // Show "Thinking..."
    showThinking()

    inputBox.value = ""

    await sendToBackend(text)
}

// -----------------
// UI Mode Switcher
// -----------------
function switchToConversationMode(){

    const inputBox = document.getElementById("main_input")

    // Change placeholder
    inputBox.placeholder = "Continue..."

    // Replace Fire → Fuel
    const fireBtn = document.getElementById("fire_btn")

    const fuelBtn = document.createElement("button")
    fuelBtn.innerText = "Fuel"
    fuelBtn.id = "fuel_btn"
    fuelBtn.onclick = fuel

    fireBtn.replaceWith(fuelBtn)

    // Show End Session button
    document.getElementById("end_btn").style.display = "inline-block"
}

// -------------------------------
// BACKEND CALL (SHARED) - PASS AGENT FROM BACKEND TO FRONTEND
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

        const data = await res.json()

        //removeThinking()

        // Format text (single line breaks)
        const formatted = data.content.replace(/\n+/g, "<br>")

        // Update thinking, prevents duplicate messages
        //updateThinking(formatted)
		updateThinking(data.content, data.agent)

        // 🔥 HANDLE CHOICE TYPE
        if(data.type === "choice"){
            renderChoices(data.choices)
        }

        // 🔥 Store agent memory if present
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
            container.remove() // remove after click
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
function updateThinking(text, agent="jung"){

    let thinking = document.getElementById("thinking")

    const formatted = text.replace(/\n+/g, "<br>")

    // Convert agent id → display name
    const agentName = formatAgentName(agent)

    if(!thinking){
        const chatBox = document.getElementById("chat")

        thinking = document.createElement("div")
        thinking.className = "ai-msg"

        chatBox.appendChild(thinking)
    }

    thinking.innerHTML = `
        <span class="label-agent">Agent ${agentName}:</span>
        <br><br>
        ${formatted}
    `

    thinking.id = ""
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
// FORMAT AGENT NAME
// -------------------------------
function formatAgentName(agent){

    const map = {
        jung: "Jung",
        dream: "Dream",
        shadow: "Shadow",
        myth: "Myth",
        epistemic: "Epistemic",
        bpsy: "BPsy",
        jred: "JRed",
        synthesis: "Synthesis"
    }

    return map[agent] || agent
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

// ---------------------------------------------------------
// ENTER(SEND ACTION) & SHIFT+ENTER(INSERT NEW LINE) CONTROL
// ---------------------------------------------------------
document.getElementById("main_input").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault()

        if (window.conversationStarted) {
            fuel()
        } else {
            fire()
        }
    }
})