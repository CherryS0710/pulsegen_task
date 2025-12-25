import os
import json
from pathlib import Path
from typing import List, Dict
import openai
from dotenv import load_dotenv

# Load .env from project root (two levels up from services/)
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class ModuleExtractor:
    """
    Uses LLM to extract product modules and submodules from documentation content.
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
    
    def _truncate_content(self, content: str, max_chars: int = 60000) -> str:
        """Truncate content to fit within token limits."""
        if len(content) <= max_chars:
            return content
        # Truncate but keep the beginning (usually most important)
        return content[:max_chars] + "\n\n[Content truncated to fit token limits...]"
    
    def _build_prompt(self, content: List[Dict[str, str]]) -> str:
        """Build the LLM prompt for module extraction."""
        content_text = "\n\n".join([
            f"Documentation from {item['url']}:\n{item['content']}"
            for item in content
        ])
        
        content_text = self._truncate_content(content_text)
        
        num_urls = len(content)
        url_list = ", ".join([item['url'] for item in content])
        
        prompt = f"""You are a Product Management AI assistant. Analyze the following product documentation from {num_urls} source{'s' if num_urls > 1 else ''} and extract the product modules and submodules.

IMPORTANT: You are analyzing documentation from {num_urls} different URL{'s' if num_urls > 1 else ''}:
{url_list}

Your task is to:
1. Analyze ALL the documentation provided from ALL {num_urls} source{'s' if num_urls > 1 else ''}
2. Identify distinct product modules (high-level feature areas) across ALL sources
3. For each module, identify submodules (specific features or capabilities) from ALL sources
4. Combine and merge related modules/submodules from different sources
5. Provide clear, concise descriptions suitable for Product Managers
6. Base your analysis strictly on the provided documentation - do not hallucinate features

Documentation Content from {num_urls} source{'s' if num_urls > 1 else ''}:
{content_text}

Return a JSON object with a "modules" key containing an array with the following structure:
{{
  "modules": [
    {{
      "module": "Module Name",
      "description": "High-level description of the module from a product perspective",
      "submodules": {{
        "Submodule Name": "Concise description of the submodule functionality"
      }}
    }}
  ]
}}

Guidelines:
- Analyze and extract modules from ALL {num_urls} documentation source{'s' if num_urls > 1 else ''} provided
- If the same module appears in multiple sources, merge them into one entry
- Modules should represent major functional areas of the product
- Submodules should be specific features or capabilities within each module
- Descriptions should be clear, professional, and PM-friendly
- Only include modules/submodules that are clearly mentioned or implied in the documentation
- Group related features logically across all sources
- Use consistent naming conventions
- If no clear modules can be identified, return {{"modules": []}}

Return ONLY valid JSON, no additional text or explanation."""
        
        return prompt
    
    async def extract_modules(self, content: List[Dict[str, str]]) -> List[Dict]:
        """
        Extract modules from documentation content using LLM.
        
        Args:
            content: List of dicts with 'url' and 'content' keys
            
        Returns:
            List of module dictionaries with module, description, and submodules
        """
        prompt = self._build_prompt(content)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Product Management AI assistant that extracts structured module information from product documentation. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            response_text = response.choices[0].message.content.strip()
            
            # Handle both JSON object and array responses
            try:
                parsed = json.loads(response_text)
                
                # Extract array from response
                if isinstance(parsed, dict):
                    # Look for common keys that might contain the array
                    for key in ['modules', 'data', 'result']:
                        if key in parsed and isinstance(parsed[key], list):
                            return parsed[key]
                    # If no array found, return empty
                    return []
                elif isinstance(parsed, list):
                    # Direct array response (fallback)
                    return parsed
                else:
                    return []
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                import re
                json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                
                # Last resort: try to find JSON array in the text
                array_match = re.search(r'(\[.*?\])', response_text, re.DOTALL)
                if array_match:
                    return json.loads(array_match.group(1))
                
                raise ValueError("Could not parse JSON from LLM response")
        
        except openai.RateLimitError as e:
            error_msg = "OpenAI API rate limit exceeded or quota exhausted. Please check your billing and usage at https://platform.openai.com/usage"
            print(f"Rate limit error: {str(e)}")
            raise Exception(error_msg)
        except openai.APIError as e:
            error_msg = f"OpenAI API error: {str(e)}"
            if "quota" in str(e).lower() or "insufficient_quota" in str(e):
                error_msg = "OpenAI API quota exceeded. Please check your billing and usage at https://platform.openai.com/usage. You may need to add payment method or upgrade your plan."
            print(f"API error: {str(e)}")
            raise Exception(error_msg)
        except Exception as e:
            error_str = str(e)
            if "quota" in error_str.lower() or "insufficient_quota" in error_str or "429" in error_str:
                error_msg = "OpenAI API quota exceeded. Please check your billing and usage at https://platform.openai.com/usage. You may need to add payment method or upgrade your plan."
            else:
                error_msg = f"Failed to extract modules: {error_str}"
            print(f"Error in LLM extraction: {error_str}")
            raise Exception(error_msg)

