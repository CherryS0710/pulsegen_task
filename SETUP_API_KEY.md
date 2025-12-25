# Setting Up Your OpenAI API Key

## Quick Setup

1. **Edit the `.env` file** in the project root:
   ```bash
   nano .env
   # or use your preferred editor
   ```

2. **Replace the placeholder** with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. **Save the file**

4. **Restart the backend server** (if it's running):
   - Stop the current backend (Ctrl+C in the terminal)
   - Start it again with `./start-backend.sh` or `uvicorn main:app --reload`

## Getting an OpenAI API Key

If you don't have an API key yet:

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-`)
5. Paste it into your `.env` file

## Using Alternative API Providers

The system supports OpenAI-compatible APIs. To use a different provider:

1. Set `OPENAI_API_BASE` in `.env` to your provider's API endpoint
2. Set `OPENAI_API_KEY` to your provider's API key
3. Optionally set `OPENAI_MODEL` to the model name you want to use

Example for a different provider:
```
OPENAI_API_KEY=your-provider-key
OPENAI_API_BASE=https://api.your-provider.com/v1
OPENAI_MODEL=your-model-name
```

## Verification

After setting up your API key, test it by:
1. Making a request through the frontend at http://localhost:3000
2. Enter a documentation URL
3. Click "Extract Modules"

If you see an error about the API key, double-check:
- The `.env` file is in the project root (not in backend/)
- The key doesn't have quotes around it
- You've restarted the backend after changing the file


