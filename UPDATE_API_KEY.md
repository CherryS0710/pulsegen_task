# How to Update Your API Key

## Step-by-Step Instructions

### Option 1: Using a Text Editor (Recommended)

1. **Open the `.env` file** in the project root:
   - Using VS Code: Open the file `/Users/cherrysharma/Desktop/pulsegen.io/.env`
   - Using nano (terminal): `nano .env`
   - Using any text editor

2. **Find this line:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Replace it with your actual key:**
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   (Your key will start with `sk-` and be much longer)

4. **Save the file**

5. **Restart the backend server:**
   - Find the terminal where the backend is running
   - Press `Ctrl+C` to stop it
   - Run: `cd backend && source venv/bin/activate && uvicorn main:app --reload`

### Option 2: Using Terminal (Quick)

Run this command (replace `YOUR_ACTUAL_KEY_HERE` with your real key):

```bash
cd /Users/cherrysharma/Desktop/pulsegen.io
sed -i '' 's/OPENAI_API_KEY=your_openai_api_key_here/OPENAI_API_KEY=YOUR_ACTUAL_KEY_HERE/' .env
```

Then restart the backend.

## Getting Your API Key

If you don't have an API key:

1. Go to: https://platform.openai.com/api-keys
2. Sign in (or create an account)
3. Click **"Create new secret key"**
4. Give it a name (e.g., "Module Extraction Tool")
5. **Copy the key immediately** (you won't see it again!)
6. Paste it into your `.env` file

## Important Notes

- ✅ The key should start with `sk-`
- ✅ No quotes needed around the key
- ✅ No spaces around the `=` sign
- ✅ Must restart backend after changing `.env`
- ❌ Never commit `.env` to git (it's in `.gitignore`)

## Verify It's Working

After updating and restarting:
1. Go to http://localhost:3000
2. Enter a documentation URL
3. Click "Extract Modules"
4. If it works, you'll see modules extracted!


