# Fer's Blog

This is my personal blog/website built with [Jekyll](https://jekyllrb.com) and hosted on [GitHub Pages](https://pages.github.com/).

## Running Locally

### Prerequisites

- A Unix-like OS (Ubuntu, other Linux distributions, or macOS)
- Ruby (version 2.7.0 or higher; GitHub Pages currently uses Ruby 3.1.x)
- Git
- Bundler

### 1. Install Ruby and Required Packages

#### On Ubuntu/Debian systems:

```bash
sudo apt update
sudo apt install ruby-full build-essential zlib1g-dev
```

#### On macOS:

We recommend using `rbenv` to manage Ruby versions:

1. Install rbenv and ruby-build using Homebrew:
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install rbenv and ruby-build
brew update
brew install rbenv ruby-build
```

2. Set up rbenv in your shell:
```bash
# For zsh (macOS default since Catalina)
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc

# For bash
# echo 'eval "$(rbenv init - bash)"' >> ~/.bash_profile
# source ~/.bash_profile
```

3. Install and set Ruby 3.1.2:
```bash
rbenv install 3.1.2
rbenv global 3.1.2
```

4. Verify the installation:
```bash
ruby -v    # Should show ruby 3.1.2
which ruby # Should point to ~/.rbenv/versions/3.1.2/bin/ruby
```

### 2. Configure RubyGems Environment

Avoid installing gems with sudo by setting up a user-specific gem directory.

Add the following lines to your shell config file (`~/.bashrc` or `~/.zshrc`):

```bash
# Install RubyGems to ~/gems
export GEM_HOME="$HOME/gems"
export PATH="$HOME/gems/bin:$PATH"
```

Then apply the changes:
```bash
source ~/.bashrc   # or source ~/.zshrc
```

Verify setup:
```bash
echo $GEM_HOME     # Should be /home/youruser/gems
echo $PATH         # Should include /home/youruser/gems/bin
```

### 3. Install Bundler and Jekyll

Use gem to install both:
```bash
gem install bundler jekyll
```

Check installation:
```bash
bundler -v
jekyll -v
```

> Do not install Bundler using apt. That can lead to version conflicts and path issues.

### 4. Clone the Blog Repository

```bash
git clone https://github.com/ferjorosa/ferjorosa.github.io.git
cd ferjorosa.github.io
```

### 5. Configure Bundler to Use vendor/bundle

Set Bundler to install project-specific dependencies in a local folder:
```bash
bundle config set --local path 'vendor/bundle'
```

### 6. Install Project Dependencies

```bash
bundle install
```

This will install all gems into the `vendor/bundle` directory, keeping them isolated from other projects.

### 7. Serve the Site Locally

```bash
bundle exec jekyll serve
```

Visit your site at [http://localhost:4000](http://localhost:4000)

### Additional Options

Auto-reload on changes:
```bash
bundle exec jekyll serve --livereload
```

Show draft posts:
```bash
bundle exec jekyll serve --drafts
```

## Project Structure

```
├── _posts/        # Blog posts
├── _layouts/      # Page layouts
├── _includes/     # Reusable components
├── css/           # Stylesheets
├── js/            # JavaScript files
├── _config.yml    # Site configuration
├── Gemfile        # Ruby gem dependencies
├── Gemfile.lock   # Locked gem versions
└── vendor/bundle/ # Local gem installation directory
```

## Troubleshooting

### Command Not Found (e.g., jekyll, bundler)

Ensure your shell is reloaded and `$PATH` includes `~/gems/bin`:
```bash
source ~/.bashrc   # or source ~/.zshrc
```

Check:
```bash
which jekyll
which bundler
```

### Permissions or Conflicts

Double-check that you're not using sudo with gem.

### Reinstalling Gems

```bash
bundle clean --force
bundle install
```

### Using the Correct Ruby Version

Use a version manager like rbenv or rvm. To lock the Ruby version for the project:
```bash
echo "3.1.2" > .ruby-version
```

This setup ensures you're using project-local dependencies, avoiding permission issues, and staying aligned with GitHub Pages' environment.