# SilverZim

SilverZim
F1 Educational Game w/ AI opponents

About
Users include new F1 fans & returning fans alike who want to refresh their understanding of the rules of this beloved sport. This application acts as a fun and informational way of doing this by incorporating a racing element to it for the user.

With 3 tutorial stages and more actual F1 circuits being added, the user first gets to grip with the environment and then, verses the reinforcement learning algorithm that acts as its opponents. While the user races to finish the stated amount of laps, the AI tries to catch up by continually searching for the optimum race line which is all conveniently recorded in a leaderboard alongside gameplay.

Why?
New fans often lose interest in the sport due to not understanding the basic rules so my solution focused on maximising the joy of learning. As I wanted to explore machine learning within the opponents, I used the NEAT (Neuro Evolution of Augmenting Topologies) library where continually testing different parameters in the configuration file was exciting.
This was my A-Level Computer Science coursework where my project & write-up obtained 69/70. Since being my first larger-scale project, I have learnt a lot since then. 
One being that through I had two main python files, it is likely bad practice to keep a lot of code within one main file for future maintainability reasons. Though I was able to collapse functions within vscode, this may impact readability for others and maintenance in the future. Also, it would've been useful to use version control software.

Expansions?
Improve maintainability, add more f1 circuits, fix bugs that come up after extended game play.

How to install & run the project
1. Download & unzip 'game-files' folder & open in editor e.g. vscode
2. Ensure libraries are installed: pygame, sys, neat, json
3. Locate MainF1.py file
4. Click run and in terminal, it will ask for a username. Then, hit enter & return to the pygame window. Game begins.

Final Note
- The cars do go the wrong direction in the RedBull Ring circuit.