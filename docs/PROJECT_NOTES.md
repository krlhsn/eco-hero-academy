# Project notes

## Purpose

Eco-Hero Academy is a local-first recycling education game. It combines short material guides with quizzes, adaptive review, saved player profiles and achievements.

## Included learning content

- Nine material categories: plastic, paper, glass, metal, electronics, food, cardboard, batteries and clothing
- Two fictional regional demonstration presets
- Five-question challenges using True/False and multiple-choice questions
- Review of up to two questions missed in the previous round
- Eco Advisor responses to common recycling questions
- Local profiles, scores, viewed-material tracking and badges
- A local top-ten leaderboard

## Application structure

The maintained implementation is divided into content, models, storage, game logic and terminal interface modules. The standalone `eco_hero_academy.py` file combines those parts for simple copy-and-run use.

Profile storage uses atomic file replacement and reports invalid saved data rather than silently replacing it. The application uses only the Python standard library.

## Accuracy and scope

The two named regional presets are fictional examples, not government or municipal datasets. Recycling guidance varies by location and collection facility. The material tips and facts are educational content and have not been independently verified as official local instructions. Users should check with their local collection provider, especially for batteries, electronics, light bulbs and other potentially hazardous items.
