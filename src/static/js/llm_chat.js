// async function sendToLLM(ingest_id, question, callback) {
//     const text = await retrieve_context(ingest_id);

//     try {
//         const response = await fetch('/llm_chat', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ text, query: question }),
//         });

//         const data = await response.json();
//         if (data.status === "success" && data.data && data.data.response) {
//             callback(null, data.data.response);
//         } else {
//             callback("No valid response from LLM");
//         }
//     } catch (err) {
//         console.error(err);
//         callback("LLM call failed");
//     }
// }

//     function handleLLMSubmit(ingestId) {
//         const question = document.getElementById('chat-input').value.trim();
//         const responseBox = document.getElementById('chat-response');
//         responseBox.innerText = 'Thinking...';

//         if (!question) {
//             responseBox.innerText = 'Please enter a question.';
//             return;
//         }

//         sendToLLM(ingestId, question, (err, answer) => {
//             if (err) {
//                 responseBox.innerText = `Error: ${err}`;
//             } else {
//                 responseBox.innerText = answer;
//             }
//         });
//     }

//     async function retrieve_context(ingestId) {
//         try {
//             const response = await fetch(`/read_text/${ingestId}`);

//             if (!response.ok) {
//                 throw new Error("Failed to fetch context");
//             }

//             const text = await response.text();
//             console.log("Context text:", text);
//             return text;
//         } catch (err) {
//             console.error("Error retrieving context:", err);
//             return '';
//         }
//     }

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
        const response = await fetch('http://192.168.10.137:9000/api/btr_qa_follow_up', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,   // send API key in header or body depending on your backend
            },
            body: JSON.stringify({ 
                text, 
                query: question,
                model // include model name here
            }),
        });

        const data = await response.json();
        if (data.status === "success" && data.data && data.data.response) {
            callback(null, data.data.response);
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
