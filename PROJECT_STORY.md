# Building Eco-Hero Academy: Making Recycling Easier to Explore

Recycling sounds straightforward until you have to answer a very ordinary question: *Can this actually go in the recycling bin?* The answer can depend on the material, contamination, and the rules of the place collecting it. A simple list of materials does not always help someone understand those differences.

That practical problem shaped **Eco-Hero Academy**, a small Python learning game built around recycling guides, short challenges, progress and an interactive terminal experience. I wanted the project to make environmental learning something a person could actively explore, rather than just scroll past.

## From reading a tip to trying it out

The application brings several learning activities together. It has guides for nine material categories, including plastic, paper, glass, metal, electronics, food, cardboard, batteries and clothing. Each guide can include a tip, things to keep out of the recycling stream and a fun fact.

But reading information is only one part of learning. Eco-Hero Academy also has five-question challenges using true/false and multiple-choice questions. When someone misses a question, the application can bring up to two missed questions into the next round. That small feature changes the experience: getting something wrong is not simply the end of a score. It can become a reason to revisit the topic.

There is also an **Eco Advisor** for common questions about things like batteries, plastic film, food waste and electronics. It is rule-based: it matches a question to prepared guidance. It is not a live AI service, and it cannot replace local waste-management advice.

## Making progress feel personal

Players can create a profile, save their progress, collect badges and see a leaderboard. The application stores this information locally in a JSON file, so progress remains on the same computer between sessions. The leaderboard is local too; it does not compare players across the internet.

I kept the implementation lightweight. The maintained application is separated into modules for content, models, storage, game logic and the terminal interface. There is also a standalone version for someone who prefers to run one complete Python file. The project uses only the Python standard library.

That structure matters because a learning game is more than a set of questions. Content, scoring, saved progress and the way a person moves through the application all need to work together. Keeping those responsibilities separate makes the code easier to inspect and change.

## The detail that needs care: local recycling rules

One important limitation is that recycling guidance is not universal. A material accepted by one facility may be rejected by another. The project includes two named regional presets, but they are fictional demonstrations, not official municipal programmes or verified local rules.

For the same reason, the Eco Advisor tells users to check their local collection provider, especially for batteries, electronics, light bulbs and other items that may need special handling. I would rather make that boundary clear than make a simple application sound more authoritative than it is.

## What I learned while building it

This project helped me think about learning as a sequence: introduce an idea, let someone practise it, show why an answer was right or wrong, and give them another chance to improve. It also made me pay attention to the less visible parts of an application, such as saving progress safely and handling invalid or incomplete saved data without silently overwriting it.

Most importantly, the project reminded me that an educational tool has to communicate uncertainty as well as information. A recycling tip is only useful when its scope is clear.

## What comes next

There is room to improve the learning content through careful review against current, location-specific guidance. A future version could also make the experience more accessible to people who do not use a terminal. Those would be new steps, not features that this version already has.

For now, Eco-Hero Academy is a local Python project that combines material guides, quizzes, review, profiles and achievements in one place. Its goal is modest: help someone become a little more curious and thoughtful about what happens to everyday materials.

---

**Project:** [Eco-Hero Academy on GitHub](https://github.com/krlhsn/eco-hero-academy)
**Course context:** Stanford Code in Place, Fall 2025
**Author:** Kamrul Hassan
