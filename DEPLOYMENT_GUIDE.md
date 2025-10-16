# MCQ Generator - Vercel Deployment Guide

This guide will help you deploy your MCQ Generator Flask application to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Git installed on your system
3. Your project files ready for deployment

## Deployment Steps

### 1. Prepare Your Repository

Make sure your project has the following files:
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function entry point
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `.gitignore` - Git ignore file

### 2. Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit for Vercel deployment"
```

### 3. Push to GitHub

Create a new repository on GitHub and push your code:

```bash
git remote add origin https://github.com/yourusername/mcq-generator.git
git branch -M main
git push -u origin main
```

### 4. Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it's a Python project
5. Configure environment variables (see step 5 below)
6. Click "Deploy"

#### Option B: Deploy via Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from your project directory:
   ```bash
   vercel
   ```

4. Follow the prompts to configure your deployment

### 5. Set Environment Variables

In your Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variable:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your Google Gemini API key
   - **Environment**: Production, Preview, Development

### 6. Verify Deployment

1. Your app will be available at `https://your-project-name.vercel.app`
2. Test the file upload and MCQ generation functionality
3. Check that downloads work properly

## Important Notes

### File Storage Limitations

- Vercel serverless functions have a 50MB payload limit
- Files are stored temporarily in memory/temp directories
- Consider using external storage (AWS S3, Cloudinary) for production

### API Key Security

- Never commit API keys to your repository
- Use environment variables for sensitive data
- The hardcoded key in the code is for local development only

### Performance Considerations

- Serverless functions have execution time limits
- Large files may cause timeouts
- Consider implementing file size limits in your frontend

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **Template Not Found**: Ensure templates are in the correct directory structure
3. **API Key Issues**: Verify environment variables are set correctly
4. **File Upload Issues**: Check file size limits and allowed extensions

### Debugging

1. Check Vercel function logs in the dashboard
2. Use `vercel logs` command for CLI debugging
3. Test locally with `vercel dev` before deploying

## Local Development

To test your Vercel deployment locally:

```bash
vercel dev
```

This will run your app locally with Vercel's serverless environment.

## Custom Domain (Optional)

1. In Vercel dashboard, go to your project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Follow the DNS configuration instructions

## Support

- Vercel Documentation: [vercel.com/docs](https://vercel.com/docs)
- Flask Documentation: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- Google Gemini AI Documentation: [ai.google.dev](https://ai.google.dev)

---

Your MCQ Generator is now deployed and ready to use! 🎉
