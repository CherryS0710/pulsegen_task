# Troubleshooting Guide

## Common Errors and Solutions

### Error: "insufficient_quota" or "You exceeded your current quota"

**What it means:** Your OpenAI API key is valid, but you've either:
- Exceeded your usage limit
- Don't have billing set up
- Need to add payment method

**Solutions:**

1. **Check your OpenAI account:**
   - Go to https://platform.openai.com/usage
   - Check your usage and limits
   - Verify billing is set up

2. **Add payment method:**
   - Go to https://platform.openai.com/account/billing
   - Add a payment method
   - Set up usage limits if needed

3. **Check your plan:**
   - Free tier has very limited usage
   - You may need to upgrade to a paid plan

4. **Use an alternative API provider:**
   - The system supports OpenAI-compatible APIs
   - See "Using Alternative Providers" below

### Error: "invalid_api_key"

**Solution:** Update your `.env` file with a valid API key. See `UPDATE_API_KEY.md`

### Error: "Site cannot be reached"

**Solution:** Make sure both servers are running:
- Backend on port 8000
- Frontend on port 3000

See `QUICKSTART.md` for startup instructions.

### Error: "Failed to crawl any of the provided URLs"

**Possible causes:**
- URLs are not accessible (require authentication)
- URLs are invalid or broken
- Network/timeout issues

**Solutions:**
- Verify URLs are publicly accessible
- Check URLs in a browser first
- Try a different documentation URL

## Using Alternative API Providers

If you're having quota issues with OpenAI, you can use alternative providers that offer OpenAI-compatible APIs:

### Option 1: Use a Different Provider

Update your `.env` file:

```bash
# Example for Anthropic Claude (if they support OpenAI-compatible API)
OPENAI_API_KEY=your-anthropic-key
OPENAI_API_BASE=https://api.anthropic.com/v1
OPENAI_MODEL=claude-3-sonnet-20240229

# Example for other providers
OPENAI_API_KEY=your-provider-key
OPENAI_API_BASE=https://api.your-provider.com/v1
OPENAI_MODEL=your-model-name
```

### Option 2: Local LLM (Advanced)

For local development, you can use:
- **Ollama** - Run models locally
- **LM Studio** - Local model server
- **vLLM** - Local inference server

Set in `.env`:
```
OPENAI_API_BASE=http://localhost:11434/v1  # Ollama default
OPENAI_MODEL=llama2
```

### Option 3: Free/Cheap Alternatives

- **Groq** - Fast inference, free tier available
- **Together AI** - Pay-as-you-go
- **Anyscale** - OpenAI-compatible endpoints

## Getting Help

1. Check the error message in the frontend
2. Check backend terminal for detailed logs
3. Verify your `.env` file configuration
4. Test your API key directly with OpenAI's API

## Testing Your API Key

You can test if your API key works:

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

If you get a 401, the key is invalid.
If you get a 429, you have quota issues.
If you get a 200, the key works!


