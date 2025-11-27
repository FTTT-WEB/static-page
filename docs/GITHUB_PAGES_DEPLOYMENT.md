# GitHub Pages Deployment Guide

This guide will help you deploy your Jekyll site to GitHub Pages.

## Prerequisites

1. A GitHub account
2. A GitHub repository (create one if you haven't already)

## Setup Steps

### 1. Push Your Code to GitHub

If you haven't already, initialize git and push your code:

```bash
cd /Users/bird/Code/fttt/static-page
git init
git add .
git commit -m "Initial commit with Jekyll site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

### 2. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings**
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select **GitHub Actions** (not "Deploy from a branch")
5. The workflow will automatically run when you push to the `main` or `master` branch

### 3. Wait for Deployment

After pushing your code:
- GitHub Actions will automatically build and deploy your site
- You can check the progress in the **Actions** tab of your repository
- Once complete, your site will be available at:
  - `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

### 4. Custom Domain (Optional)

If you want to use a custom domain:
1. Go to **Settings** → **Pages**
2. Enter your custom domain in the **Custom domain** field
3. Configure your DNS records as instructed by GitHub

## Project Structure

Your Jekyll site is located in the `jekyll-site/` directory:
- `jekyll-site/_config.yml` - Jekyll configuration
- `jekyll-site/_layouts/` - Layout templates
- `jekyll-site/pages/` - Page content (Markdown files)
- `jekyll-site/assets/` - Static assets (images, CSS, JS)
- `jekyll-site/index.md` - Homepage

## How It Works

The GitHub Actions workflow (`.github/workflows/deploy.yml`) will:
1. Checkout your code
2. Set up Ruby and install dependencies from `jekyll-site/Gemfile`
3. Build the Jekyll site from the `jekyll-site/` directory
4. Deploy the built site to GitHub Pages

## Local Development

To test your site locally before deploying:

```bash
cd jekyll-site
bundle install
bundle exec jekyll serve
```

Then visit `http://localhost:4000` in your browser.

## Troubleshooting

### Build Fails

- Check the **Actions** tab for error messages
- Ensure all dependencies are listed in `jekyll-site/Gemfile`
- Verify that `_config.yml` is valid YAML

### Site Not Updating

- Wait a few minutes for GitHub Actions to complete
- Check that you pushed to the `main` or `master` branch
- Verify GitHub Pages is set to use **GitHub Actions** as the source

### Assets Not Loading

- Ensure asset paths in your templates use absolute paths starting with `/`
- Check that assets are in the `jekyll-site/assets/` directory
- Verify the `_config.yml` baseurl is set correctly (empty for root domain)

## Notes

- The site builds from the `jekyll-site/` subdirectory
- The workflow automatically handles the build and deployment
- Your site will be rebuilt automatically on every push to the main branch
