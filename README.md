# Spring-2025-ACM-Project-Hub
## Project Hub Overview

snAkeCM is a project developed by the Spring 2025 USF ACM Project Hub team. In this project, we’re building our own version of the classic Snake game using Python. However, rather than simply recreating Snake, we’re challenging ourselves to add new, member-suggested twists like walls that switch between being barriers and open paths to make the game more interesting.

This project is designed to help students learn by doing. Instead of traditional workshops, our role is to guide you as you collaborate through Discord and GitHub. By working on this project together, you’ll gain hands-on experience in coding, teamwork, and making documentation.

Our end goal is to showcase the project in a final event where you can present your work. This isn’t just about making a game; it’s about building a project that demonstrates your skills and looks great on your resume, boosting your internship chances and paving the way for future Project Hubs.

## Documentation

**Gabriel** <br />
https://github.com/Marquibaa <br />
In this branch, among the changes made from the first ever version of the game, there are:
- Before starting the game, you have to write your name, and your score is shown in the top right of the screen. After you lose, your name and score gets stored in a json file so it can be used or shown later. At the same time, your name and score gets printed in the terminal whenever you die as well.
- Now, if you go you go out of bounds, you get teleported to the other side of the board.
- Bug fixes include that now apples do not spawn in your body, and you don't kill yourself by moving more than once per frame, since the snake only moves once per frame.

**Tima** <br />
https://github.com/tubermucas <br />
"Resume", "Restart", "Change BG", "Music On/Off", "Exit"
- Pause menu: Now the user can press ESC to stop the game and a menu will show up with options: Resume - unpause the game, Restart - start the game over with a score 0, Change Bg (Background) - by pressing ENTER the background changes, Music On/Off - the music turns on and off by pressing ENTER, Exit - for now it quits the game completely, for the future it is supposed to send the user back to the main menu (main menu is not implemented yet).
- ScoreBoard: The screen is divided into two parts: a black rectangle on top with the current user's score and the play area itself.
- Font: The chosen font for all text in the game is Press Start 2P.

**Sean** <br />
- Main Menu: Menu to select modes before starting the game and title screen
- Difficulty modes in classic mode: Changes speed settings to match assigned difficulty within classic mode
- Death blocks (not included into final due to breaking game): Blocks that would kill the player upon contact, spawned until 5 were on the map at which point the oldest one in the group would change position.

**Minh** <br />
https://github.com/CodingMinh <br />
Speed up and teleporting apple for challenge mode
- In challenge mode, if your score (the number of apples eaten) is >= 10 and < 15, you significantly speed up
- If your score is >= 15 and < 20, the apples randomly teleport every 10 seconds (gotta go fast lol)

**Joshua** <br />
https://github.com/Agentscreator <br />
"Background Themes", "Background Music"
- Background Themes: Selected and implemented five unique background designs that players can change using ESC: ☘️ Forest ⛅️ Desert 🌊 Ocean ⛰️ Mountain 🌌 Space
- Background Music: Added background music to give the game a music for the game https://youtu.be/PzxywNLeDrg?list=RDPzxywNLeDrg