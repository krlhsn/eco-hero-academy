# Project notes

## Origin

This project began as a Code in Place 2025 final project named **AI-Powered Community Recycling Guide**, presented in the console as **Eco-Hero Academy**.

## Original feature set retained

- ASCII welcome art, challenge title, badge and trophy
- Nine general material categories: plastic, paper, glass, metal, electronics, food, cardboard, batteries and clothing
- Two region-style demonstration presets: Eco-City Standard and Greenburg Initiative
- Five-question challenge with True/False and multiple-choice items
- Retry of up to two previously missed questions in the next round
- Rule-based advisor responses for common recycling topics
- Local profiles, scores, viewed-material tracking and badges
- Local top-ten leaderboard

## Refactor changes

The original single-file program has been separated into `data`, `models`, `storage`, `engine` and `cli` modules. Persistence is now atomic and refuses to silently overwrite a corrupt data file. Input and profile values are validated. Game logic can be tested independently of terminal input. Sleep delays were removed so the program responds immediately.

## Accuracy and scope

The original material statements are retained as learning content, but they have not been independently verified in this refactor. The two named region presets are fictional examples and not local government datasets. The advisor is deterministic keyword matching rather than an AI model. No claim is made that this program can determine the correct disposal route for every locality or item.
