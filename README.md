# werfen - how to use functions to see stats

in stats.ipynb run the code blocks in the sections IMPORTS and INIT

Use the functions (with different names possibly) in the section STATS or make use of the following functions:

## Use of Functions

```python
winrate_name = winrate('Name')
``` 

<span style="color:orange">Name</span> must exactly match (including captilization) one of the names in the array players which can be accessed by

```python
players
``` 
<span style="color:green">Function Output (here: winrate_name):</span> list containing:
- dataframe containting teampartners, number of games and wins with them, as well as the resulting winrate playing together
- dataframe containting opponents, number of games and wins against them, as well as the resulting winrate against them
- overall winrate of player (float)
- list of cup_hit_rate each game (only for games on which that metric was recorded)

---

```python
total_games('Name')
``` 
<span style="color:orange">Name</span> must exactly match (including captilization) one of the names in the array players 

<span style="color:green">Function Output:</span> total number of games played by 'Name' (int)

---

```python
total_tournaments('Name')
``` 
<span style="color:orange">Name</span> must exactly match (including captilization) one of the names in the array players 

<span style="color:green">Function Output:</span> total number of tournaments played by 'Name' (int)

---

```python
fenster_winrate()
``` 
<span style="color:green">Function Output:</span> overall winrate on the window side (float)

---

```python
ranks('Name')
``` 
<span style="color:orange">Name</span> must exactly match (including captilization) one of the names in the array players 

<span style="color:green">Function Output:</span> plot of ranks in tournatment of 'Name's team over time

