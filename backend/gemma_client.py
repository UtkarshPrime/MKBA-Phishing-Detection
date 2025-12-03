import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GemmaClient:
    def __init__(self, model_name="gemma3n:e4b", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_generate = f"{base_url}/api/generate"
        self.api_chat = f"{base_url}/api/chat"

    def is_available(self):
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(self.base_url)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def _generate(self, prompt, system_prompt=None):
        """Helper to call the generation API."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(self.api_generate, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            logger.error(f"Error calling Gemma: {e}")
            return f"Error: Unable to get response from Gemma. {str(e)}"

    def analyze_email(self, content):
        """Analyze email content for phishing using Gemma."""
        system_prompt = (
            "You are a cybersecurity expert. Analyze the email for phishing risks. "
            "Classify as 'phishing' if there are clear malicious indicators (e.g., spoofing, urgent requests for credentials, suspicious links). "
            "Classify as 'legitimate' if it appears to be normal communication, even if brief or generic. "
            "Classify as 'suspicious' ONLY if there are specific red flags but no definitive proof of phishing. "
            "Do NOT flag emails as suspicious solely due to brevity, generic greetings, or lack of context unless accompanied by other threats. "
            "\n\nExamples from our database:"
            "\n- Legitimate: 'Hello, your order #12345 has been shipped and will arrive tomorrow.' (Normal business notification)"
            "\n- Legitimate: 'Meeting scheduled for 2pm tomorrow. Please confirm attendance.' (Standard internal communication)"
            "\n- Legitimate: 'Weekly Newsletter: Check out our latest updates on security protocols.' (Regular newsletter)"
            "\n- Phishing: 'URGENT: Your account will be suspended! Click here to verify immediately.' (Urgency + Threat)"
            "\n- Phishing: 'You have won $1000000! Click to claim your prize now!!!' (Too good to be true)"
            "\n- Phishing: 'Your payment method has expired. Update it here: http://bit.ly/update123' (Suspicious link + Urgency)"
            "\n\nFormat response as JSON: {'classification': 'phishing'/'suspicious'/'legitimate', 'confidence': 0-100, 'explanation': '...'}"
        )
        
        prompt = f"Email Content:\n\n{content}\n\nAnalysis:"
        
        response_text = self._generate(prompt, system_prompt)
        
        # Attempt to parse JSON from the response. Models sometimes wrap code in backticks.
        try:
            # Clean up potential markdown formatting
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            logger.warning("Failed to parse JSON from Gemma response. Returning raw text.")
            return {
                "classification": "unknown",
                "confidence": 0,
                "explanation": response_text
            }

    def analyze_url_context(self, url, features):
        """Provide context on why a URL might be suspicious based on its features."""
        feature_summary = ", ".join([f"{k}: {v}" for k, v in features.items() if v])
        
        prompt = (
            f"I have a URL: {url}\n"
            f"Extracted features: {feature_summary}\n"
            "As a security expert, explain why these features might indicate a phishing attempt "
            "or why it looks safe. Be concise."
        )
        return self._generate(prompt)

    def chat(self, message, history=None, context=None):
        """Chat with the user about security topics, with optional context."""
        messages = []
        
        # Add system message with context if available
        system_content = "You are a helpful cybersecurity assistant. Keep your responses summarized, concise, and use simple, easy-to-understand language. Avoid technical jargon where possible. "
        if context:
            if context.get('url'):
                system_content += f"\nThe user is currently analyzing this URL: {context['url']}. "
            if context.get('email'):
                system_content += f"\nThe user is currently analyzing this Email content: {context['email']}. "
            system_content += "If the user asks about 'this' or 'it', refer to the above content."
            
        # Ollama supports a 'system' role in the messages list for some models, 
        # or we can prepend it to the first message. Let's try adding a system message.
        messages.append({"role": "system", "content": system_content})

        if history:
            messages.extend(history)
        
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_chat, json=payload)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return "I'm having trouble connecting to my brain right now. Please try again later."
