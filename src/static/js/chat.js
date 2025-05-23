
window.handleLLMSubmit = function(ingestId) {
    const question = document.getElementById('chat-input').value.trim();
    const responseBox = document.getElementById('chat-response');
    const apiKey = document.getElementById('llm-api-key').value.trim();
    const model = document.getElementById('llm-model').value;


    console.log("Ingest ID:", ingestId);
    console.log("Question:", question);
    console.log("API Key:", apiKey);
    console.log("Model:", model);


    responseBox.innerText = 'Thinking...';

    if (!question) {
        responseBox.innerText = 'Please enter a question.';
        return;
    }
    if (!apiKey) {
        responseBox.innerText = 'Please enter your API key.';
        return;
    }

    sendToLLM(ingestId, question, apiKey, model, (err, answer) => {
        if (err) {
            responseBox.innerText = `Error: ${err}`;
        } else {
            responseBox.innerText = answer;
        }
    });
};



async function sendToLLM(ingest_id, question, apiKey, model, callback) {
    const text = await retrieve_context(ingest_id);

    try {
        const response = await fetch('/api/llm/v1/chat/completions', {  // Updated endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                input_text: text, 
                question: question,
                model: model,
                api_key: apiKey
            }),
        });
        const data = await response.json();
        if (data.response) {  // Updated response check
            callback(null, data.response);
        } else if (data.error) {
            callback(data.error);
        } else {
            callback("No valid response from LLM");
        }
    } catch (err) {
        console.error(err);
        callback("LLM call failed");
    }
}
async function retrieve_context(ingestId) {
    try {
        // Instead of fetch, get the text from UI element
        const text = document.querySelector('.result-text').value;
        
        console.log("Context text from UI element:", text);
        return text;
    } catch (err) {
        console.error("Error retrieving context:", err);
        return '';
    }
}
