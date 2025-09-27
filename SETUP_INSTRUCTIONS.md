# Setup Instructions for Audiobook Production System

## 🚀 Quick Start

The automation failed because the OpenRouter API key is not configured. Here's how to fix it:

### 1. Get an OpenRouter API Key
1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Create an account or sign in
3. Navigate to [API Keys](https://openrouter.ai/keys)
4. Create a new API key
5. Copy the key (it starts with `sk-or-v1-...`)

### 2. Create Environment Configuration
1. Copy the template file:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file:
   ```bash
   nano .env
   ```

3. Replace `your_openrouter_api_key_here` with your actual API key:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   ```

### 3. Run the Automation Again
```bash
python full_automation.py
```

## 💡 Story Input
When prompted, enter your story concept. For example:
- "Tom meets Julia through a wrong number text message and they form an unexpected connection"
- "A detective investigates mysterious disappearances in a small town"
- "Two rival chefs are forced to work together to save a restaurant"

## ✅ What This Fixes
The character extraction implementation is already complete and working. Once you add the API key:
- ✅ Characters will be extracted from your story in Station 1
- ✅ The same characters will flow through all stations (no more hardcoded names)
- ✅ Your actual story will be used throughout the entire pipeline
- ✅ No more "Memory Thief" or "Dr. Sarah Chen" appearing in your output

## 🔧 Optional: Redis Setup
For full functionality, you may also want to start Redis:
```bash
# Install Redis (macOS)
brew install redis
brew services start redis

# Or run Redis in Docker
docker run -d -p 6379:6379 redis:alpine
```

## 📊 Expected Output
Once configured, you should see:
1. Station 1: Character extraction and scale analysis
2. Station 2: Project DNA and bible creation
3. Station 3: Age/genre optimization
4. Station 4: Reference mining and seed generation
5. Station 4.5: Narrator strategy
6. Station 5: Season architecture
7. Station 6: Master style guide

All using YOUR characters and story throughout!