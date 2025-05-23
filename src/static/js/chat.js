
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
    try {
        // Retrieve the context text for the given ingest_id (we don't show this content in the UI)
        const contextText = await retrieve_context(ingest_id); 

        if (!contextText) {
            callback("Failed to retrieve context text. Please try again.");
            return;
        }

        // LLM API call with the question and retrieved context (not shown in the UI)
        const response = await fetch('/api/llm/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                input_text: contextText,  // Use context text here
                question: question,
                model: model,
                api_key: apiKey
            }),
        });

        const data = await response.json();
        
        if (data.response) {
            callback(null, data.response);  // Callback with the result from LLM
        } else if (data.error) {
            callback(data.error);  // Callback with error message
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
        // Fetch the content for the given ingest_id but don't display it
        const retrieve_response = await fetch('/api/llm/v1/retrieve/get_content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ingest_id: ingestId
            }),
        });

        const content = await retrieve_response.json();

        if (content.text) {
            // Only return the context text to be used in LLM query
            return content.text; 
        } else if (content.error) {
            console.error(content.error); 
            return null;
        } else {
            console.error("Failed to retrieve content from the provided ingest ID.");
            return null;
        }
    } catch (err) {
        console.error(err);
        return null;  // Ensure we return null if there's an error
    }
}
