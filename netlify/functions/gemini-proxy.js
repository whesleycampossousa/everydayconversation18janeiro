exports.handler = async function (event, context) {
    if (event.httpMethod !== "POST") {
        return { statusCode: 405, body: "Method Not Allowed" };
    }

    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: "Server Error: API Key not configured." })
        };
    }

    try {
        const requestBody = JSON.parse(event.body || "{}");
        const userText = requestBody.userText;
        const systemPrompt = requestBody.systemPrompt;
        const sentenceText = requestBody.sentenceText;
        const audio = requestBody.audio;

        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${apiKey}`;

        let payload = null;

        if (audio && sentenceText) {
            if (typeof sentenceText !== "string" || sentenceText.length < 2 || sentenceText.length > 400) {
                return { statusCode: 400, body: JSON.stringify({ error: "Invalid sentenceText." }) };
            }
            if (!audio.data || typeof audio.data !== "string") {
                return { statusCode: 400, body: JSON.stringify({ error: "Invalid audio data." }) };
            }

            const maxBase64Length = 8 * 1024 * 1024;
            if (audio.data.length > maxBase64Length) {
                return { statusCode: 413, body: JSON.stringify({ error: "Audio too large." }) };
            }

            const pronunciationSystemPrompt = [
                "You are a pronunciation evaluator for short English sentences.",
                "Compare the student audio to the expected sentence.",
                "Return JSON only with this schema:",
                "{\"mistakeWords\":[\"word1\",\"word2\"],\"notes\":\"\"}.",
                "Rules:",
                "- mistakeWords must be lowercase words from the expected sentence, no punctuation.",
                "- If no clear mistakes or unsure, return an empty array.",
                "- notes is optional, max 120 chars, pt-BR."
            ].join(" ");

            payload = {
                contents: [
                    {
                        role: "user",
                        parts: [
                            { text: `Expected sentence: \"${sentenceText}\"` },
                            {
                                inlineData: {
                                    mimeType: audio.mimeType || "audio/webm",
                                    data: audio.data
                                }
                            }
                        ]
                    }
                ],
                systemInstruction: { parts: [{ text: pronunciationSystemPrompt }] },
                generationConfig: {
                    responseMimeType: "application/json",
                    temperature: 0.2
                }
            };
        } else if (userText && systemPrompt) {
            payload = {
                contents: [{ parts: [{ text: userText }] }],
                systemInstruction: { parts: [{ text: systemPrompt }] },
                generationConfig: { responseMimeType: "application/json" }
            };
        } else {
            return { statusCode: 400, body: JSON.stringify({ error: "Invalid request body." }) };
        }

        const response = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorText = await response.text();
            return {
                statusCode: response.status,
                body: JSON.stringify({ error: `Gemini API Error: ${errorText}` })
            };
        }

        const data = await response.json();
        return {
            statusCode: 200,
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            }
        };
    } catch (error) {
        console.error("Function Error:", error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
