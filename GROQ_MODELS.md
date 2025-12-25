# Groq Model Reference

## Currently Available Models

The model `llama-3.1-70b-versatile` has been decommissioned. Here are the currently available Groq models:

### Recommended Models

1. **llama-3.1-8b-instant** (Currently Set)
   - Fast, efficient model
   - Good for general tasks
   - Lower cost

2. **llama-3.3-70b-versatile**
   - More powerful than 8b version
   - Better for complex reasoning
   - Higher cost

3. **mixtral-8x7b-32768**
   - Mixture of Experts model
   - Good balance of speed and quality
   - Supports longer context

4. **gemma-7b-it**
   - Google's Gemma model
   - Good for instruction following

## How to Change Models

Edit your `.env` file and change the `OPENAI_MODEL` line:

```bash
OPENAI_MODEL=llama-3.1-8b-instant
```

Then restart the backend server.

## Check Available Models

You can check which models are currently available by visiting:
https://console.groq.com/docs/models

Or check the Groq API documentation for the latest list.

## Current Configuration

Your current model is set to: **llama-3.1-8b-instant**

This model should work for module extraction tasks. If you need more powerful reasoning, consider switching to `llama-3.3-70b-versatile` (if available) or `mixtral-8x7b-32768`.


