# Publishing and maintaining this repository

The public repository is already published at:

https://github.com/krlhsn/ai-powered-community-recycling-guide

## Set up a local working copy

    git clone https://github.com/krlhsn/ai-powered-community-recycling-guide.git
    cd ai-powered-community-recycling-guide

## Make and verify changes

The project targets Python 3.10+ and has no third-party runtime dependencies.

    python -m unittest discover -s tests -v
    python main.py

After making changes:

    git add .
    git commit -m "Describe the change"
    git push

GitHub Actions automatically runs the test suite on Python 3.10, 3.11, 3.12, 3.13 and 3.14 for pushes to `main` and pull requests targeting `main`.

## Suggested GitHub About description

> A gamified Python recycling education project with material guides, adaptive quizzes, local profiles and achievement badges.
