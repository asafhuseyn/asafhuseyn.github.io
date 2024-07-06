---
layout: post
title: "Did You Know You Can Use GitHub to Host Your Site for Free?"
date: 2024-07-03
categories: blog
---

# Did You Know You Can Use GitHub to Host Your Site for Free?

In this guide, I'll walk you through how to use GitHub Pages to host your personal website or simple blog for free. Based on my experiences, I'll explain the process with examples.

## Contents

1. [What is GitHub Pages?](#what-is-github-pages)
2. [Step 1: Creating a Repository](#step-1-creating-a-repository)
3. [Step 2: Enabling GitHub Pages](#step-2-enabling-github-pages)
4. [Step 3: Creating a Static Site with Jekyll](#step-3-creating-a-static-site-with-jekyll)
5. [Using GitHub Gist](#using-github-gist)
6. [GitHub Actions and the Publishing Process](#github-actions-and-the-publishing-process)
7. [Step 4a: Purchasing a Domain (with Cloudflare)](#step-4a-purchasing-a-domain-with-cloudflare)
8. [Step 4b: Purchasing a Domain (with iCloud+)](#step-4b-purchasing-a-domain-with-icloud)
9. [Step 5: Connecting a Custom Domain](#step-5-connecting-a-custom-domain)
10. [Step 6a: Setting Up a Custom Email Address (Optional)](#step-6a-setting-up-a-custom-email-address-optional)
11. [Step 6b: Setting Up a Custom Email Address with iCloud+ (Optional)](#step-6b-setting-up-a-custom-email-address-with-icloud-optional)
12. [Conclusion](#conclusion)

## What is GitHub Pages?

GitHub Pages is a free service that lets you publish static web pages directly from your GitHub repositories. It's perfect for personal websites, project pages, and blogs.

### Advantages:

- Free hosting
- Easy setup and management
- Integration with Git and GitHub
- Support for Jekyll static site generator
- Ability to use a custom domain
- SSL certificate support

## Step 1: Creating a Repository

1. Log in to your GitHub account.
2. Click the "New repository" button.
3. Name the repository `<username>.github.io` (e.g., `asafhuseyn.github.io`).
4. Set the repository to "Public". Note: If you're using a free GitHub account, you must make your repository public to use GitHub Pages. If you have a GitHub Pro or higher account, you can use GitHub Pages with private repositories.
5. Click the "Create repository" button.

## Step 2: Enabling GitHub Pages

1. Go to the settings of your newly created repository.
2. Click the "Pages" section in the left menu.
3. Under the "Source" section, select the "main" or "master" branch.
4. Click the "Save" button.

Your site should now be live at `https://<username>.github.io`.

## Step 3: Creating a Static Site with Jekyll

GitHub Pages works seamlessly with Jekyll, a Ruby-based static site generator. With Jekyll, you can easily add new pages and blog posts.

### Creating a New Page with Jekyll

- On your local machine, navigate to your repository folder:

```bash
git clone https://github.com/<username>/<username>.github.io.git
cd <username>.github.io
```

- Create a new Markdown file:

```markdown
---
layout: default
title: "About Me"
---
# Hello, I'm a developer!
```

- Add new blog posts to the `_posts` folder. The blog post file name format should be: `YYYY-MM-DD-title.md`.

Example:

```markdown
---
layout: post
title: "My First Blog Post"
date: 2024-07-03
---
This is my first blog post!
```

- Push the changes to GitHub:

```bash
git add .
git commit -m "Added new page and blog post"
git push origin main
```

Note: 
* Jekyll supports themes, and you will need to configure the `_config.yml` file accordingly. 
* To keep things simple, I did not delve into more detailed topics like creating categories. You can check my repository example at [asafhuseyn.github.io](https://asafhuseyn.github.io).

## Using GitHub Gist

GitHub Gist is a great way to share and manage your code snippets. While you can use Markdown code blocks to share code on your Jekyll site, Gists are better for more complex or frequently updated code. To use Gists on your Jekyll site:

1. Create a Gist: https://gist.github.com
2. Copy the ID of the created Gist.
3. Add it to your Jekyll page as follows:

```liquid
{% gist GIST_ID %}
```

This method allows you to manage and update your code examples centrally.

## GitHub Actions and the Publishing Process

GitHub Pages uses GitHub's CI/CD tool, GitHub Actions, to automatically build and publish your site. This process usually works smoothly and requires no intervention. Here's how it works:

1. When you push changes to the main branch (usually `main` or `master`), GitHub Actions are triggered automatically.
2. GitHub Actions build your Jekyll site and push the results to the `gh-pages` branch.
3. This process typically takes a few minutes.

To monitor this process:

1. Go to the "Actions" tab in your GitHub repository.
2. You can see the latest workflows and their status.
3. If there are any errors, you can check the details here.

## Step 4a: Purchasing a Domain (with Cloudflare)

1. Create a Cloudflare account (if you don't have one).
2. Use Cloudflare's domain registration service to purchase your desired domain name.

## Step 4b: Purchasing a Domain (with iCloud+)

1. On your iPhone or iPad, go to Settings > [Your Name] > iCloud > iCloud+ > Custom Email Domain.
2. Tap "Add Domain".
3. To purchase a new domain, tap "Buy a new domain" and follow the instructions to purchase your desired domain name.

## Step 5: Connecting a Custom Domain

1. Go to your DNS settings and add the following A records for `@`:
   - 185.199.108.153
   - 185.199.109.153
   - 185.199.110.153
   - 185.199.111.153

2. (Optional) Add the following AAAA records for `@` to support IPv6:
   - 2606:50c0:8000::153
   - 2606:50c0:8001::153
   - 2606:50c0:8002::153
   - 2606:50c0:8003::153

3. Go to the settings of your GitHub repository, click on the "Pages" section, and enter your custom domain name (e.g., example.com) in the "Custom domain" field.

## Step 6a: Setting Up a Custom Email Address (Optional)

To create a custom email address with your domain:

1. Choose an email service provider (Google Workspace, Zoho Mail, etc.).
2. Follow your provider's instructions to add MX records to your DNS settings.
3. Example MX records:
   
```
MX  @  10  mx1.mailserver.com
MX  @  20  mx2.mailserver.com
```

4. In your email service provider's admin panel, create a new email address (e.g., `contact@example.com`).

## Step 6b: Setting Up a Custom Email Address with iCloud+ (Optional)

If you purchased your domain through iCloud+, you don't need to configure DNS settings. Just create an email address:

1. On your iPhone or iPad, go to Settings > [Your Name] > iCloud > iCloud+ > Custom Email Domain.
2. Select your domain.
3. Tap "Add Email Address".
4. Enter the desired email address (e.g., `contact@`, `info@`, etc.).
5. Tap "Done".

You can use this address for email, iMessage, and FaceTime.

## Conclusion

In this guide, I've tried to cover the basic steps you can take with GitHub Pages.

*I explained the steps through Cloudflare because it's my favorite and Apple collaborates with it, but you can use any registrar as the steps will be the same. For specific information on any topic, feel free to reach out to me.*
