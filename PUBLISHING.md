# Publishing this repository to GitHub

The intended repository name is `ai-powered-community-recycling-guide`.

1. Create a **public, empty** repository under the GitHub account `krlhsn` with that name. Do not initialize it with a README, license or `.gitignore`; those files are already included here.
2. From this folder, run:

       git init -b main
       git add .
       git commit -m "Initial release: Eco-Hero Academy 2.0"
       git remote add origin https://github.com/krlhsn/ai-powered-community-recycling-guide.git
       git push -u origin main

3. Enable GitHub Actions if GitHub asks for permission. The workflow in `.github/workflows/tests.yml` will run tests on Python 3.10 through 3.14.

The short GitHub About description can be:

> A gamified Python recycling education project with material guides, adaptive quizzes, local profiles and achievement badges.
