# YouTube Comment Sentiment Analysis

A simple tool that tells you if YouTube comments are happy, sad, or neutral! 🎥

## What This Tool Does

- Enter any YouTube video URL
- See how people feel about the video (happy 😊, neutral 😐, or sad 😢)
- Watch the results update in real-time
- See actual comments and how they were rated

## How to Use

1. **Get Started**
   - Download or clone this project
   - Get a YouTube API key from [Google Cloud Console](https://console.cloud.google.com)
   - Copy `.env.example` to `.env` and add your API key

2. **Set Up**
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate it
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   
   # Install needed packages
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```bash
   python app.py
   ```
   Then open your browser and go to: `http://localhost:5000`

## Deploy on Render

1. **Create a Render Account**
   - Sign up at [Render](https://render.com)
   - Connect your GitHub repository

2. **Configure Environment Variables**
   - Go to your service settings
   - Add your `YOUTUBE_API_KEY` in the Environment Variables section

3. **Deploy**
   - Render will automatically detect the Python project
   - It will use the `requirements.txt` and `render.yaml` for configuration
   - The app will be deployed and you'll get a URL

## Features

- 🎯 Easy to use - just paste a YouTube URL
- 📊 See results in a nice pie chart
- 🔄 Auto-refresh every 1-5 minutes
- 💬 See real comments and how they were rated
- 📱 Works on phones and computers

## What You Need

- Python 3.7 or newer
- YouTube API key
- Internet connection

## Need Help?

If something's not working:
1. Make sure your API key is correct
2. Check if the video has public comments
3. Make sure you're not over your daily API limit
4. For deployment issues:
   - Check if all files are committed to GitHub
   - Verify your environment variables are set
   - Check the deployment logs on Render

## Want to Help?

Feel free to:
- Report bugs
- Suggest new features
- Make the code better
- Share with others

## License

This project is open source and free to use! 🎉 