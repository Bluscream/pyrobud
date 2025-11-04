# Pyrobud Documentation

This directory contains the documentation for Pyrobud, viewable at [https://bluscream.github.io/pyrobud](https://bluscream.github.io/pyrobud).

## Files

- **index.md** - Home page
- **dependencies.md** - Complete guide to module dependency management
- **quick-start.md** - Quick start guide for dependencies
- **implementation.md** - Technical implementation details

## Building Locally

To build and view the documentation locally:

```bash
# Install Jekyll (if not already installed)
gem install bundler jekyll

# Install dependencies
cd docs
bundle install

# Serve locally
bundle exec jekyll serve
```

Then visit http://localhost:4000/pyrobud/ in your browser.

## GitHub Pages

This documentation is automatically published to GitHub Pages when changes are pushed to the main branch.

The site uses the [Just the Docs](https://just-the-docs.github.io/just-the-docs/) theme for a clean, searchable documentation experience.

