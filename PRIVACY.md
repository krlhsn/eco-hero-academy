# Privacy and local data notice

Eco-Hero Academy is a local terminal application. It does not connect to a remote AI service, database, analytics system or online leaderboard.

## Data stored

When a player saves a profile, the app stores the username, score, highest score, challenge count, viewed materials, advisor-use count, badges, missed-question review history and selected guide preset in `eco_hero_profiles.json`.

## Where it is stored

The JSON file is created in the current working directory on the computer where the app is run. The app does not upload or synchronize it. The leaderboard only reads profiles from that same file.

## User precautions

There are no passwords, access controls or encryption. Use a nickname rather than a real full name, and do not store sensitive personal information. Keep backups private. The `.gitignore` file excludes the runtime profile file from Git by default.
