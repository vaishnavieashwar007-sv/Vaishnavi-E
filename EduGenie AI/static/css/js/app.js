// Send request to FastAPI backend
async function sendRequest(task, text) {
    let endpoint;
    let body;

    switch (task) {

        case "qa":
            endpoint = API_ENDPOINTS.qa;
            body = {
                question: text
            };
            break;

        case "explain":
            endpoint = API_ENDPOINTS.explain;
            body = {
                text: text
            };
            break;

        case "quiz":
            endpoint = API_ENDPOINTS.quiz;
            body = {
                text: text,
                count: 3
            };
            break;

        case "summary":
        case "summarize":
            endpoint = API_ENDPOINTS.summary;
            body = {
                text: text,
                style: "concise"
            };
            break;

        case "recommendations":
            endpoint = API_ENDPOINTS.recommendations;
            body = {
                topic: text,
                level: "beginner",
                weeks: 6
            };
            break;

        default:
            throw new Error("Invalid task selected.");
    }

    return fetch(endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });
}