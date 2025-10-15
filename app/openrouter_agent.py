import httpx
import json
import asyncio
from typing import Dict, Any, List
from app.config import settings


class OpenRouterAgent:
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.base_url = "https://openrouter.ai/api/v1"
        # Make embeddings optional to avoid dependency issues
        self.embeddings = None
        # Disabled embeddings to avoid PyTorch/NumPy compatibility issues
        # try:
        #     from langchain_huggingface import HuggingFaceEmbeddings
        #     self.embeddings = HuggingFaceEmbeddings(
        #         model_name="sentence-transformers/all-MiniLM-L6-v2"
        #     )
        # except ImportError:
        #     # Embeddings not available, but OpenRouter still works
        #     pass
        
        # Available models on OpenRouter
        self.available_models = {
            "qwen-72b": "qwen/qwen-2.5-72b-instruct:free",
            "grok-4": "x-ai/grok-4-fast:free",
            "llama-3b": "meta-llama/llama-3.2-3b-instruct:free",
            "gpt-4o": "openai/gpt-4o-2024-08-06",
            "claude-3-haiku": "anthropic/claude-3-haiku"
        }
    
    async def process_message(self, user_input: str, model_name: str = "qwen-72b", max_tokens: int = 3000) -> str:
        """Process a user message using OpenRouter with rate limiting and retry logic"""
        max_retries = 3
        base_delay = 2.0  # Base delay in seconds
        
        for attempt in range(max_retries):
            try:
                # Add delay between requests to avoid rate limiting
                if attempt > 0:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    await asyncio.sleep(delay)
                
                # Get the actual model ID
                model_id = self.available_models.get(model_name, self.available_models["qwen-72b"])
                
                # Create system message based on model
                system_message = self._get_system_message(model_name)
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/your-repo",
                    "X-Title": "Audiobook Production System"
                }
                
                data = {
                    "model": model_id,
                    "messages": [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_input}
                    ],
                    "temperature": 0.7,
                    "max_tokens": max_tokens
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=60.0
                    )
                    
                    # Handle rate limiting specifically
                    if response.status_code == 429:
                        if attempt < max_retries - 1:
                            continue  # Retry with exponential backoff
                        else:
                            raise Exception(f"Rate limited after {max_retries} attempts")
                    
                    response.raise_for_status()
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    continue  # Retry on rate limit
                else:
                    return f"I'm sorry, I encountered an error: {str(e)}"
            except Exception as e:
                if attempt < max_retries - 1:
                    continue  # Retry on other errors
                else:
                    return f"I'm sorry, I encountered an error: {str(e)}"
        
        return f"I'm sorry, I encountered an error after {max_retries} attempts"
    
    def _get_system_message(self, model_name: str) -> str:
        """Get appropriate system message for each model"""
        system_messages = {
            "qwen-72b": "You are Qwen2.5 72B, an advanced AI assistant with excellent reasoning capabilities. Provide helpful, accurate, and detailed responses.",
            "grok-4": "You are Grok-4, an advanced AI assistant with excellent reasoning capabilities. Provide helpful, accurate, and detailed responses.",
            "llama-3b": "You are Llama 3.2 3B, an advanced AI assistant with excellent reasoning capabilities. Provide helpful, accurate, and detailed responses.",
            "gpt-4o": "You are GPT-4o, an advanced AI assistant with excellent reasoning capabilities. Provide helpful, accurate, and detailed responses.",
            "claude-3-haiku": "You are Claude 3 Haiku, an advanced AI assistant with excellent reasoning capabilities. Provide helpful, accurate, and detailed responses."
        }
        return system_messages.get(model_name, system_messages["qwen-72b"])
    
    async def generate(self, prompt: str, model: str = "qwen-72b", 
                      max_tokens: int = 3000, temperature: float = 0.7) -> str:
        """Generate response using specified model (for Station agents) with rate limiting"""
        import asyncio
        
        max_retries = 5
        base_delay = 2  # Start with 2 seconds
        
        for attempt in range(max_retries):
            try:
                # Use the full model ID if provided, otherwise map from friendly names
                if "/" not in model:
                    model_id = self.available_models.get(model, model)
                else:
                    model_id = model
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/your-repo",  # Optional
                    "X-Title": "Audiobook Production System"  # Optional
                }
                
                data = {
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=60.0
                    )
                    response.raise_for_status()
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    # Rate limit hit - exponential backoff
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)  # Exponential backoff: 2, 4, 8, 16, 32 seconds
                        print(f"⚠️  Rate limit hit. Waiting {delay}s before retry {attempt + 1}/{max_retries}...")
                        await asyncio.sleep(delay)
                        continue
                    else:
                        raise Exception(f"OpenRouter rate limit exceeded after {max_retries} retries. Please wait before continuing.")
                else:
                    # Other HTTP error
                    raise Exception(f"OpenRouter API error: {str(e)}")
            except Exception as e:
                error_msg = str(e)
                if "402 Payment Required" in error_msg:
                    # Try with a free model as fallback
                    print("⚠️ Payment required for selected model, switching to free model...")
                    free_model_id = "qwen/qwen-2.5-72b-instruct:free"
                    data["model"] = free_model_id
                    
                    try:
                        async with httpx.AsyncClient() as client:
                            response = await client.post(
                                f"{self.base_url}/chat/completions",
                                headers=headers,
                                json=data,
                                timeout=60.0
                            )
                            response.raise_for_status()
                            result = response.json()
                            return result["choices"][0]["message"]["content"]
                    except Exception as fallback_error:
                        raise Exception(f"OpenRouter API error (free model also failed): {str(fallback_error)}")
                else:
                    raise Exception(f"OpenRouter API error: {str(e)}")
    
    def get_available_models(self) -> Dict[str, str]:
        """Get list of available models"""
        return self.available_models


# Global OpenRouter agent instance (lazy initialization)
openrouter_agent = None

def get_openrouter_agent():
    """Get the global OpenRouter agent instance, creating it if needed"""
    global openrouter_agent
    if openrouter_agent is None:
        openrouter_agent = OpenRouterAgent()
    return openrouter_agent
