# NFL Prop Model V7.2.8 — Stage 2 Alternate-Market Analysis

- **Scope:** NFL Week 7, 2026 — Sunday only
- **Historical sample:** L10
- **Historical cutoff:** Completion of Week 6, 2026 (2026-10-19)
- **Stage 2 State ID:** `STATE-2-WEEK7-2026-SUN-L10-FD-PRICE-CORE-20261023`
- **Parent Stage 1 State ID:** `STATE-1-WEEK7-2026-SUN-L10-FD-OR-RETRY2-20261023`
- **Persisted State SHA:** `0fa735cd7edce2902f4dd54291ccc3231acfde0d`
- **FanDuel source:** `odds/nfl_player_props_latest.csv` (blob SHA `9569934e2541bda6ecae5e773b99121cb887028f`)

## Stage 2 result

- Locked Stage 1 records analyzed: **128**
- FanDuel alternate lines captured with listed prices: **1175**
- Records with a qualifying Core: **124**
- **Stage 3 context candidates: 106**
- Excluded from Stage 3: **22**

### Core / Floor / Ceiling rules

- **Core:** FanDuel Over odds from -350 to -150 inclusive; choose the price numerically closest to -250. If tied, choose the more negative price. A remaining tie is resolved by lower threshold for deterministic selection.
- **Floor:** Immediately lower available alternate threshold than Core.
- **Ceiling:** Immediately higher available alternate threshold than Core.
- Historical hit rate uses the locked Stage 1 L10 observations; an Over line hits only when the observation is strictly greater than the listed line. HR is descriptive, not a predicted probability.
- **Stage 3 narrowing rule:** carry forward a record only when Core exists and at least one of Floor/Core/Ceiling has HR ≥ 6/10. This is the operational viability screen used to apply the prompt's requirement to materially narrow the candidate set. No current-week context was used.
- No line movement, price movement, cross-book comparison, injury, weather, matchup, scheme, role, workload, current-season trend, or game-script research was performed.

## Band table — all 128 locked Stage 1 player-market records

| Market | Player | Team | Main line | Main HR | Alt lines | Floor (line / odds / HR) | Core (line / odds / HR) | Ceiling (line / odds / HR) | Stage 3 |
|---|---|---:|---:|---:|---:|---|---|---|---|
| Passing Yards | Aaron Rodgers | PIT | 229.5 | 6/10 | 9 | Over 175.0 / -470 / 9/10 | Over 200.0 / -250 / 8/10 | Over 225.0 / -132 / 6/10 | YES |
| Passing Yards | Tyler Shough | NO | 227.5 | 8/10 | 9 | Over 175.0 / -470 / 8/10 | Over 200.0 / -240 / 8/10 | Over 225.0 / -125 / 8/10 | YES |
| Passing Yards | Bryce Young | CAR | 253.5 | 6/10 | 10 | Over 200.0 / -450 / 7/10 | Over 225.0 / -240 / 6/10 | Over 250.0 / -130 / 6/10 | YES |
| Passing Yards | C.J. Stroud | HOU | 255.5 | 6/10 | 10 | Over 200.0 / -470 / 7/10 | Over 225.0 / -245 / 7/10 | Over 250.0 / -132 / 6/10 | YES |
| Passing Yards | Brock Purdy | SF | 240.5 | 6/10 | 11 | Over 175.0 / -580 / 9/10 | Over 200.0 / -300 / 8/10 | Over 225.0 / -166 / 6/10 | YES |
| Passing Yards | Joe Burrow | CIN | 260.5 | 5/10 | 10 | Over 200.0 / -500 / 9/10 | Over 225.0 / -275 / 7/10 | Over 250.0 / -152 / 6/10 | YES |
| Passing Yards | Kyler Murray | MIN | 205.5 | 5/10 | 9 | Over 150.0 / -550 / 9/10 | Over 175.0 / -270 / 6/10 | Over 200.0 / -136 / 5/10 | YES |
| Passing Yards | Daniel Jones | IND | 193.5 | 6/10 | 9 | Over 150.0 / -390 / 8/10 | Over 175.0 / -192 / 7/10 | Over 200.0 / +102 / 6/10 | YES |
| Passing Yards | Geno Smith | NYJ | 223.5 | 3/10 | 9 | Over 175.0 / -400 / 7/10 | Over 200.0 / -210 / 5/10 | Over 225.0 / -112 / 3/10 | YES |
| Passing Yards | Jacoby Brissett | ARI | 225.5 | 5/10 | 9 | Over 175.0 / -440 / 8/10 | Over 200.0 / -225 / 8/10 | Over 225.0 / -118 / 5/10 | YES |
| Passing Yards | Jared Goff | DET | 278.5 | 6/10 | 10 | Over 225.0 / -420 / 8/10 | Over 250.0 / -230 / 8/10 | Over 275.0 / -130 / 6/10 | YES |
| Passing Yards | Matthew Stafford | LA | 270.5 | 6/10 | 10 | Over 225.0 / -360 / 8/10 | Over 250.0 / -192 / 8/10 | Over 275.0 / -102 / 6/10 | YES |
| Passing Yards | Kirk Cousins | LV | 236.5 | 6/10 | 10 | Over 175.0 / -580 / 8/10 | Over 200.0 / -280 / 6/10 | Over 225.0 / -154 / 6/10 | YES |
| Passing Yards | Sam Darnold | SEA | 225.5 | 5/10 | 9 | Over 175.0 / -440 / 7/10 | Over 200.0 / -225 / 5/10 | Over 225.0 / -118 / 5/10 | YES |
| Passing Yards | Patrick Mahomes | KC | 218.5 | 7/10 | 9 | Over 175.0 / -350 / 9/10 | Over 200.0 / -188 / 7/10 | Over 225.0 / +102 / 6/10 | YES |
| Rushing Yards | Jaylen Warren | PIT | 63.5 | 6/10 | 10 | Over 40.0 / -490 / 9/10 | Over 50.0 / -250 / 6/10 | Over 60.0 / -144 / 6/10 | YES |
| Rushing Yards | Rico Dowdle | PIT | 29.5 | 6/10 | 11 | Over 15.0 / -490 / 8/10 | Over 20.0 / -275 / 8/10 | Over 25.0 / -174 / 7/10 | YES |
| Rushing Yards | Alvin Kamara | NO | 16.5 | 6/10 | 8 | Over 5.0 / -800 / 10/10 | Over 10.0 / -280 / 10/10 | Over 15.0 / -146 / 6/10 | YES |
| Rushing Yards | Chuba Hubbard | CAR | 70.5 | 4/10 | 10 | Over 50.0 / -350 / 5/10 | Over 60.0 / -205 / 4/10 | Over 70.0 / -122 / 4/10 | NO |
| Rushing Yards | Bucky Irving | TB | 65.5 | 4/10 | 11 | Over 40.0 / -550 / 9/10 | Over 50.0 / -270 / 6/10 | Over 60.0 / -154 / 5/10 | YES |
| Rushing Yards | Kenneth Gainwell | TB | 11.5 | 6/10 | 7 | Over 5.0 / -400 / 8/10 | Over 10.0 / -158 / 6/10 | Over 15.0 / +128 / 5/10 | YES |
| Rushing Yards | Woody Marks | HOU | 60.5 | 3/10 | 10 | Over 40.0 / -420 / 6/10 | Over 50.0 / -215 / 4/10 | Over 60.0 / -122 / 3/10 | YES |
| Rushing Yards | Cam Skattebo | NYG | 31.5 | 9/10 | 13 | Over 15.0 / -440 / 9/10 | Over 20.0 / -270 / 9/10 | Over 25.0 / -186 / 9/10 | YES |
| Rushing Yards | Christian McCaffrey | SF | 60.5 | 7/10 | 11 | Over 40.0 / -400 / 8/10 | Over 50.0 / -215 / 8/10 | Over 60.0 / -122 / 7/10 | YES |
| Rushing Yards | Derrick Henry | BAL | 85.5 | 7/10 | 10 | Over 60.0 / -400 / 9/10 | Over 70.0 / -240 / 8/10 | Over 80.0 / -152 / 7/10 | YES |
| Rushing Yards | Chase Brown | CIN | 47.5 | 7/10 | 11 | Over 30.0 / -420 / 8/10 | Over 40.0 / -192 / 7/10 | Over 50.0 / -102 / 7/10 | YES |
| Rushing Yards | Jonathan Taylor | IND | 70.5 | 5/10 | 10 | Over 50.0 / -340 / 7/10 | Over 60.0 / -198 / 7/10 | Over 70.0 / -122 / 5/10 | YES |
| Rushing Yards | Tony Pollard | TEN | 65.5 | 5/10 | 11 | Over 40.0 / -550 / 9/10 | Over 50.0 / -270 / 7/10 | Over 60.0 / -158 / 6/10 | YES |
| Rushing Yards | J.K. Dobbins | DEN | 50.5 | 5/10 | 12 | Over 30.0 / -400 / 10/10 | Over 40.0 / -210 / 7/10 | Over 50.0 / -120 / 5/10 | YES |
| Rushing Yards | RJ Harvey | DEN | 16.5 | 8/10 | 8 | Over 5.0 / -850 / 10/10 | Over 10.0 / -290 / 8/10 | Over 15.0 / -146 / 8/10 | YES |
| Rushing Yards | Jahmyr Gibbs | DET | 93.5 | 3/10 | 10 | Over 70.0 / -340 / 4/10 | Over 80.0 / -210 / 3/10 | Over 90.0 / -136 / 3/10 | NO |
| Rushing Yards | Ashton Jeanty | LV | 48.5 | 6/10 | 12 | Over 30.0 / -420 / 8/10 | Over 40.0 / -200 / 7/10 | Over 50.0 / -108 / 6/10 | YES |
| Rushing Yards | Blake Corum | LA | 35.5 | 6/10 | 11 | Over 20.0 / -470 / 6/10 | Over 25.0 / -275 / 6/10 | Over 30.0 / -182 / 6/10 | YES |
| Rushing Yards | Sean Tucker | TB | 7.5 | 6/10 | 0 | — | — | — | NO |
| Rushing Yards | Jordan Mason | MIN | 46.5 | 4/10 | 12 | Over 30.0 / -350 / 7/10 | Over 40.0 / -178 / 6/10 | Over 50.0 / +104 / 3/10 | YES |
| Rushing Yards | Aaron Jones | MIN | 40.5 | 7/10 | 12 | Over 25.0 / -350 / 9/10 | Over 30.0 / -245 / 9/10 | Over 40.0 / -122 / 7/10 | YES |
| Receiving Yards | Chris Olave | NO | 75.5 | 7/10 | 12 | Over 50.0 / -380 / 7/10 | Over 60.0 / -235 / 7/10 | Over 70.0 / -146 / 7/10 | YES |
| Receiving Yards | DK Metcalf | PIT | 58.5 | 3/10 | 13 | Over 30.0 / -600 / 8/10 | Over 40.0 / -300 / 5/10 | Over 50.0 / -180 / 4/10 | YES |
| Receiving Yards | Devaughn Vele | NO | 41.5 | 6/10 | 12 | Over 25.0 / -350 / 10/10 | Over 30.0 / -245 / 9/10 | Over 40.0 / -130 / 6/10 | YES |
| Receiving Yards | Pat Freiermuth | PIT | 30.5 | 6/10 | 11 | Over 15.0 / -450 / 9/10 | Over 20.0 / -275 / 7/10 | Over 25.0 / -182 / 7/10 | YES |
| Receiving Yards | Juwan Johnson | NO | 32.5 | 7/10 | 11 | Over 20.0 / -320 / 8/10 | Over 25.0 / -210 / 8/10 | Over 30.0 / -144 / 7/10 | YES |
| Receiving Yards | Tetairoa McMillan | CAR | 69.5 | 6/10 | 12 | Over 40.0 / -490 / 7/10 | Over 50.0 / -290 / 6/10 | Over 60.0 / -180 / 6/10 | YES |
| Receiving Yards | Jalen Coker | CAR | 66.5 | 3/10 | 12 | Over 40.0 / -450 / 7/10 | Over 50.0 / -260 / 5/10 | Over 60.0 / -158 / 4/10 | YES |
| Receiving Yards | Chris Godwin | TB | 41.5 | 2/10 | 12 | Over 25.0 / -360 / 7/10 | Over 30.0 / -250 / 6/10 | Over 40.0 / -130 / 2/10 | YES |
| Receiving Yards | Darren Waller | CAR | 22.5 | 7/10 | 11 | Over 10.0 / -400 / 8/10 | Over 15.0 / -235 / 7/10 | Over 20.0 / -152 / 7/10 | YES |
| Receiving Yards | Malik Nabers | NYG | 68.5 | 6/10 | 12 | Over 40.0 / -470 / 6/10 | Over 50.0 / -275 / 6/10 | Over 60.0 / -172 / 6/10 | YES |
| Receiving Yards | Nico Collins | HOU | 68.5 | 6/10 | 12 | Over 40.0 / -470 / 10/10 | Over 50.0 / -270 / 10/10 | Over 60.0 / -172 / 6/10 | YES |
| Receiving Yards | Isaiah Likely | NYG | 47.5 | 4/10 | 11 | Over 30.0 / -380 / 6/10 | Over 40.0 / -188 / 4/10 | Over 50.0 / -102 / 4/10 | YES |
| Receiving Yards | Jaylin Noel | HOU | 27.5 | 6/10 | 13 | Over 15.0 / -310 / 7/10 | Over 20.0 / -205 / 6/10 | Over 25.0 / -144 / 6/10 | YES |
| Receiving Yards | Dalton Schultz | HOU | 31.5 | 6/10 | 11 | Over 20.0 / -310 / 8/10 | Over 25.0 / -200 / 8/10 | Over 30.0 / -132 / 6/10 | YES |
| Receiving Yards | Xavier Hutchinson | HOU | 13.5 | 8/10 | 9 | — | Over 5.0 / -245 / 9/10 | Over 10.0 / -158 / 8/10 | YES |
| Receiving Yards | Kayshon Boutte | HOU | 10.5 | 10/10 | 8 | — | Over 5.0 / -225 / 10/10 | Over 10.0 / -128 / 10/10 | YES |
| Receiving Yards | Drake London | ATL | 82.5 | 4/10 | 11 | Over 60.0 / -310 / 6/10 | Over 70.0 / -192 / 5/10 | Over 80.0 / -130 / 4/10 | YES |
| Receiving Yards | George Kittle | SF | 68.5 | 6/10 | 12 | Over 40.0 / -470 / 7/10 | Over 50.0 / -270 / 7/10 | Over 60.0 / -172 / 7/10 | YES |
| Receiving Yards | Ja'Marr Chase | CIN | 79.5 | 4/10 | 11 | Over 50.0 / -490 / 7/10 | Over 60.0 / -290 / 6/10 | Over 70.0 / -180 / 6/10 | YES |
| Receiving Yards | Tee Higgins | CIN | 65.5 | 5/10 | 12 | Over 40.0 / -400 / 8/10 | Over 50.0 / -240 / 8/10 | Over 60.0 / -152 / 5/10 | YES |
| Receiving Yards | Mike Gesicki | CIN | 22.5 | 6/10 | 10 | Over 10.0 / -450 / 9/10 | Over 15.0 / -250 / 7/10 | Over 20.0 / -152 / 6/10 | YES |
| Receiving Yards | Justin Jefferson | MIN | 72.5 | 4/10 | 11 | Over 50.0 / -330 / 5/10 | Over 60.0 / -210 / 4/10 | Over 70.0 / -132 / 4/10 | NO |
| Receiving Yards | Josh Downs | IND | 42.5 | 5/10 | 12 | Over 25.0 / -360 / 8/10 | Over 30.0 / -250 / 8/10 | Over 40.0 / -136 / 5/10 | YES |
| Receiving Yards | Garrett Wilson | NYJ | 62.5 | 5/10 | 12 | Over 40.0 / -400 / 7/10 | Over 50.0 / -225 / 6/10 | Over 60.0 / -132 / 5/10 | YES |
| Receiving Yards | Greg Dulcich | MIA | 21.5 | 8/10 | 11 | Over 10.0 / -360 / 10/10 | Over 15.0 / -215 / 10/10 | Over 20.0 / -136 / 8/10 | YES |
| Receiving Yards | Mason Taylor | NYJ | 20.5 | 8/10 | 10 | Over 10.0 / -400 / 8/10 | Over 15.0 / -215 / 8/10 | Over 20.0 / -130 / 8/10 | YES |
| Receiving Yards | Jerry Jeudy | CLE | 20.5 | 6/10 | 10 | Over 10.0 / -310 / 9/10 | Over 15.0 / -192 / 8/10 | Over 20.0 / -125 / 6/10 | YES |
| Receiving Yards | Elic Ayomanor | TEN | 14.5 | 7/10 | 9 | — | Over 5.0 / -275 / 9/10 | Over 10.0 / -174 / 9/10 | YES |
| Receiving Yards | Trey McBride | ARI | 63.5 | 6/10 | 10 | Over 40.0 / -470 / 8/10 | Over 50.0 / -245 / 7/10 | Over 60.0 / -144 / 6/10 | YES |
| Receiving Yards | Troy Franklin | DEN | 14.5 | 6/10 | 8 | Over 5.0 / -330 / 7/10 | Over 10.0 / -188 / 7/10 | Over 15.0 / -114 / 6/10 | YES |
| Receiving Yards | Elijah Higgins | ARI | 12.5 | 6/10 | 9 | — | Over 5.0 / -320 / 6/10 | Over 10.0 / -158 / 6/10 | YES |
| Receiving Yards | Christian Watson | GB | 75.5 | 5/10 | 12 | Over 50.0 / -340 / 6/10 | Over 60.0 / -215 / 6/10 | Over 70.0 / -138 / 5/10 | YES |
| Receiving Yards | Tucker Kraft | GB | 49.5 | 4/10 | 11 | Over 30.0 / -400 / 7/10 | Over 40.0 / -205 / 6/10 | Over 50.0 / -112 / 4/10 | YES |
| Receiving Yards | Sam LaPorta | DET | 49.5 | 7/10 | 12 | Over 30.0 / -420 / 9/10 | Over 40.0 / -210 / 9/10 | Over 50.0 / -114 / 7/10 | YES |
| Receiving Yards | Brock Bowers | LV | 70.5 | 4/10 | 11 | Over 50.0 / -320 / 7/10 | Over 60.0 / -192 / 6/10 | Over 70.0 / -120 / 4/10 | YES |
| Receiving Yards | Tre Tucker | LV | 40.5 | 7/10 | 13 | Over 25.0 / -310 / 9/10 | Over 30.0 / -225 / 7/10 | Over 40.0 / -122 / 7/10 | YES |
| Receiving Yards | Michael Mayer | LV | 30.5 | 6/10 | 10 | Over 15.0 / -500 / 7/10 | Over 20.0 / -300 / 7/10 | Over 25.0 / -188 / 6/10 | YES |
| Receiving Yards | Davis Allen | LA | 8.5 | 6/10 | 7 | — | Over 5.0 / -186 / 7/10 | Over 10.0 / -102 / 6/10 | YES |
| Receiving Yards | Jaxon Smith-Njigba | SEA | 92.5 | 7/10 | 10 | Over 60.0 / -470 / 10/10 | Over 70.0 / -290 / 10/10 | Over 80.0 / -192 / 8/10 | YES |
| Receiving Yards | Cooper Kupp | SEA | 24.5 | 6/10 | 12 | Over 10.0 / -450 / 9/10 | Over 15.0 / -270 / 7/10 | Over 20.0 / -168 / 6/10 | YES |
| Receiving Yards | Tory Horton | SEA | 11.5 | 6/10 | 8 | — | Over 5.0 / -260 / 8/10 | Over 10.0 / -138 / 6/10 | YES |
| Receiving Yards | Kyle Pitts | ATL | 34.5 | 6/10 | 12 | Over 20.0 / -360 / 6/10 | Over 25.0 / -245 / 6/10 | Over 30.0 / -162 / 6/10 | YES |
| Receiving Yards | Puka Nacua | LA | 96.5 | 5/10 | 10 | Over 70.0 / -360 / 9/10 | Over 80.0 / -240 / 5/10 | Over 90.0 / -154 / 5/10 | YES |
| Receptions | Chris Olave | NO | 5.5 | 7/10 | 9 | Over 4.0 / -750 / 7/10 | Over 5.0 / -310 / 7/10 | Over 6.0 / -154 / 6/10 | YES |
| Receptions | DK Metcalf | PIT | 4.5 | 3/10 | 8 | Over 3.0 / -850 / 6/10 | Over 4.0 / -310 / 3/10 | Over 5.0 / -136 / 2/10 | YES |
| Receptions | Devaughn Vele | NO | 4.5 | 5/10 | 7 | Over 3.0 / -450 / 6/10 | Over 4.0 / -182 / 5/10 | Over 5.0 / +124 / 3/10 | YES |
| Receptions | Juwan Johnson | NO | 3.5 | 7/10 | 8 | Over 2.0 / -1100 / 9/10 | Over 3.0 / -310 / 7/10 | Over 4.0 / -125 / 3/10 | YES |
| Receptions | Pat Freiermuth | PIT | 3.5 | 4/10 | 7 | Over 2.0 / -700 / 8/10 | Over 3.0 / -225 / 4/10 | Over 4.0 / +114 / 2/10 | YES |
| Receptions | Darnell Washington | PIT | 2.5 | 5/10 | 6 | — | Over 2.0 / -310 / 5/10 | Over 3.0 / -102 / 1/10 | NO |
| Receptions | Jalen Coker | CAR | 5.5 | 4/10 | 9 | Over 4.0 / -440 / 4/10 | Over 5.0 / -194 / 4/10 | Over 6.0 / +104 / 2/10 | NO |
| Receptions | Tetairoa McMillan | CAR | 5.5 | 3/10 | 9 | Over 4.0 / -440 / 5/10 | Over 5.0 / -192 / 3/10 | Over 6.0 / +110 / 1/10 | NO |
| Receptions | Chris Godwin | TB | 4.5 | 3/10 | 7 | Over 3.0 / -490 / 6/10 | Over 4.0 / -192 / 3/10 | Over 5.0 / +116 / 2/10 | YES |
| Receptions | Cade Otton | TB | 3.5 | 4/10 | 8 | Over 3.0 / -400 / 4/10 | Over 4.0 / -166 / 2/10 | Over 5.0 / +134 / 1/10 | NO |
| Receptions | Tommy Tremble | CAR | 1.5 | 6/10 | 5 | Over 1.0 / -1100 / 6/10 | Over 2.0 / -210 / 5/10 | Over 3.0 / +154 / 2/10 | YES |
| Receptions | Malik Nabers | NYG | 5.5 | 5/10 | 9 | Over 4.0 / -550 / 7/10 | Over 5.0 / -250 / 5/10 | Over 6.0 / -130 / 3/10 | YES |
| Receptions | Isaiah Likely | NYG | 5.5 | 4/10 | 9 | Over 4.0 / -440 / 5/10 | Over 5.0 / -205 / 4/10 | Over 6.0 / -102 / 3/10 | NO |
| Receptions | Nico Collins | HOU | 4.5 | 4/10 | 8 | Over 3.0 / -900 / 6/10 | Over 4.0 / -320 / 4/10 | Over 5.0 / -140 / 2/10 | YES |
| Receptions | Dalton Schultz | HOU | 3.5 | 6/10 | 7 | Over 2.0 / -850 / 9/10 | Over 3.0 / -250 / 6/10 | Over 4.0 / +100 / 3/10 | YES |
| Receptions | Kayshon Boutte | HOU | 1.5 | 7/10 | 4 | — | Over 1.0 / -300 / 7/10 | Over 2.0 / +146 / 4/10 | YES |
| Receptions | Foster Moreau | HOU | 1.5 | 6/10 | 4 | — | Over 1.0 / -350 / 6/10 | Over 2.0 / +122 / 0/10 | YES |
| Receptions | Xavier Hutchinson | HOU | 1.5 | 8/10 | 4 | — | Over 1.0 / -290 / 8/10 | Over 2.0 / +152 / 6/10 | YES |
| Receptions | Drake London | ATL | 5.5 | 3/10 | 9 | Over 4.0 / -750 / 4/10 | Over 5.0 / -310 / 3/10 | Over 6.0 / -154 / 3/10 | NO |
| Receptions | George Kittle | SF | 5.5 | 3/10 | 10 | Over 4.0 / -450 / 6/10 | Over 5.0 / -210 / 3/10 | Over 6.0 / -106 / 2/10 | YES |
| Receptions | Jahan Dotson | ATL | 1.5 | 6/10 | 6 | Over 1.0 / -1200 / 6/10 | Over 2.0 / -210 / 3/10 | Over 3.0 / +154 / 0/10 | YES |
| Receptions | Ja'Marr Chase | CIN | 6.5 | 6/10 | 10 | Over 5.0 / -700 / 7/10 | Over 6.0 / -320 / 6/10 | Over 7.0 / -172 / 4/10 | YES |
| Receptions | Tee Higgins | CIN | 5.5 | 4/10 | 8 | Over 3.0 / -1000 / 7/10 | Over 4.0 / -320 / 6/10 | Over 5.0 / -146 / 4/10 | YES |
| Receptions | Mike Gesicki | CIN | 2.5 | 5/10 | 6 | — | Over 2.0 / -350 / 5/10 | Over 3.0 / -114 / 2/10 | NO |
| Receptions | Justin Jefferson | MIN | 5.5 | 4/10 | 9 | Over 4.0 / -600 / 4/10 | Over 5.0 / -270 / 4/10 | Over 6.0 / -132 / 2/10 | NO |
| Receptions | Josh Downs | IND | 3.5 | 5/10 | 7 | Over 3.0 / -440 / 5/10 | Over 4.0 / -172 / 3/10 | Over 5.0 / +130 / 1/10 | NO |
| Receptions | T.J. Hockenson | MIN | 4.5 | 2/10 | 8 | Over 3.0 / -490 / 5/10 | Over 4.0 / -205 / 2/10 | Over 5.0 / +108 / 2/10 | NO |
| Receptions | Garrett Wilson | NYJ | 5.5 | 5/10 | 9 | Over 4.0 / -500 / 6/10 | Over 5.0 / -225 / 5/10 | Over 6.0 / -110 / 2/10 | YES |
| Receptions | Mason Taylor | NYJ | 2.5 | 7/10 | 6 | Over 2.0 / -470 / 7/10 | Over 3.0 / -160 / 4/10 | Over 4.0 / +152 / 2/10 | YES |
| Receptions | Greg Dulcich | MIA | 2.5 | 6/10 | 6 | Over 1.0 / -1450 / 10/10 | Over 2.0 / -250 / 6/10 | Over 3.0 / +122 / 3/10 | YES |
| Receptions | Wan'Dale Robinson | TEN | 4.5 | 6/10 | 8 | Over 3.0 / -440 / 6/10 | Over 4.0 / -174 / 6/10 | Over 5.0 / +124 / 4/10 | YES |
| Receptions | Jerry Jeudy | CLE | 1.5 | 9/10 | 5 | Over 1.0 / -900 / 9/10 | Over 2.0 / -172 / 6/10 | Over 3.0 / +188 / 2/10 | YES |
| Receptions | Trey McBride | ARI | 7.5 | 6/10 | 10 | Over 5.0 / -600 / 9/10 | Over 6.0 / -300 / 9/10 | Over 7.0 / -158 / 6/10 | YES |
| Receptions | Jaylen Waddle | DEN | 4.5 | 4/10 | 8 | Over 3.0 / -650 / 5/10 | Over 4.0 / -245 / 4/10 | Over 5.0 / -110 / 1/10 | NO |
| Receptions | Courtland Sutton | DEN | 2.5 | 5/10 | 6 | Over 2.0 / -580 / 5/10 | Over 3.0 / -178 / 3/10 | Over 4.0 / +142 / 2/10 | NO |
| Receptions | Marvin Mims | DEN | 1.5 | 7/10 | 4 | — | — | — | NO |
| Receptions | Elijah Higgins | ARI | 1.5 | 6/10 | 6 | — | — | — | NO |
| Receptions | Sam LaPorta | DET | 4.5 | 8/10 | 9 | Over 3.0 / -1000 / 8/10 | Over 4.0 / -330 / 8/10 | Over 5.0 / -154 / 3/10 | YES |
| Receptions | Christian Watson | GB | 4.5 | 4/10 | 8 | Over 3.0 / -850 / 6/10 | Over 4.0 / -290 / 4/10 | Over 5.0 / -130 / 3/10 | YES |
| Receptions | Tucker Kraft | GB | 4.5 | 5/10 | 8 | Over 3.0 / -670 / 6/10 | Over 4.0 / -250 / 5/10 | Over 5.0 / -114 / 2/10 | YES |
| Receptions | Isaac TeSlaa | DET | 1.5 | 6/10 | 4 | — | — | — | NO |
| Receptions | Brock Bowers | LV | 6.5 | 3/10 | 9 | Over 4.0 / -800 / 7/10 | Over 5.0 / -330 / 6/10 | Over 6.0 / -168 / 3/10 | YES |
| Receptions | Tre Tucker | LV | 3.5 | 7/10 | 7 | Over 2.0 / -800 / 7/10 | Over 3.0 / -245 / 7/10 | Over 4.0 / +106 / 3/10 | YES |
| Receptions | Davis Allen | LA | 0.5 | 7/10 | 3 | — | Over 1.0 / -250 / 5/10 | Over 2.0 / +188 / 1/10 | NO |
| Receptions | Jaxon Smith-Njigba | SEA | 6.5 | 7/10 | 9 | Over 5.0 / -670 / 8/10 | Over 6.0 / -310 / 7/10 | Over 7.0 / -154 / 6/10 | YES |
| Receptions | Travis Kelce | KC | 4.5 | 3/10 | 7 | Over 3.0 / -490 / 4/10 | Over 4.0 / -192 / 3/10 | Over 5.0 / +116 / 2/10 | NO |
| Receptions | AJ Barner | SEA | 2.5 | 6/10 | 6 | Over 2.0 / -490 / 6/10 | Over 3.0 / -158 / 2/10 | Over 4.0 / +154 / 1/10 | YES |
| Receptions | Cooper Kupp | SEA | 2.5 | 4/10 | 5 | — | Over 2.0 / -320 / 4/10 | Over 3.0 / -104 / 3/10 | NO |
| Receptions | Puka Nacua | LA | 8.5 | 5/10 | 10 | Over 6.0 / -670 / 6/10 | Over 7.0 / -320 / 5/10 | Over 8.0 / -178 / 5/10 | YES |

## Exclusions from Stage 3

- **Justin Jefferson — Receiving Yards (MIN)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Darnell Washington — Receptions (PIT)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Jalen Coker — Receptions (CAR)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Tetairoa McMillan — Receptions (CAR)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Cade Otton — Receptions (TB)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Isaiah Likely — Receptions (NYG)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Drake London — Receptions (ATL)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Mike Gesicki — Receptions (CIN)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Justin Jefferson — Receptions (MIN)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Josh Downs — Receptions (IND)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **T.J. Hockenson — Receptions (MIN)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Jaylen Waddle — Receptions (DEN)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Courtland Sutton — Receptions (DEN)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Marvin Mims — Receptions (DEN)**: No available FanDuel alternate has Over odds in the inclusive -350 to -150 Core band.
- **Elijah Higgins — Receptions (ARI)**: No available FanDuel alternate has Over odds in the inclusive -350 to -150 Core band.
- **Isaac TeSlaa — Receptions (DET)**: No available FanDuel alternate has Over odds in the inclusive -350 to -150 Core band.
- **Davis Allen — Receptions (LA)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Travis Kelce — Receptions (KC)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Cooper Kupp — Receptions (SEA)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Chuba Hubbard — Rushing Yards (CAR)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Jahmyr Gibbs — Rushing Yards (DET)**: No Floor/Core/Ceiling band reaches 6/10 historical hits; no band meets the 60% historical evidence floor.
- **Sean Tucker — Rushing Yards (TB)**: No available FanDuel alternate has Over odds in the inclusive -350 to -150 Core band.

## Stage 3 Context Candidate Set

Only the following 106 player-market records are eligible for Stage 3. The complete list, player IDs, exact historical records, and full alternate-line inventory are stored in the persisted Stage 2 State.

### Passing Yards (15)

Aaron Rodgers (PIT); Tyler Shough (NO); Bryce Young (CAR); C.J. Stroud (HOU); Brock Purdy (SF); Joe Burrow (CIN); Kyler Murray (MIN); Daniel Jones (IND); Geno Smith (NYJ); Jacoby Brissett (ARI); Jared Goff (DET); Matthew Stafford (LA); Kirk Cousins (LV); Sam Darnold (SEA); Patrick Mahomes (KC)

### Rushing Yards (18)

Jaylen Warren (PIT); Rico Dowdle (PIT); Alvin Kamara (NO); Bucky Irving (TB); Kenneth Gainwell (TB); Woody Marks (HOU); Cam Skattebo (NYG); Christian McCaffrey (SF); Derrick Henry (BAL); Chase Brown (CIN); Jonathan Taylor (IND); Tony Pollard (TEN); J.K. Dobbins (DEN); RJ Harvey (DEN); Ashton Jeanty (LV); Blake Corum (LA); Jordan Mason (MIN); Aaron Jones (MIN)

### Receiving Yards (42)

Chris Olave (NO); DK Metcalf (PIT); Devaughn Vele (NO); Pat Freiermuth (PIT); Juwan Johnson (NO); Tetairoa McMillan (CAR); Jalen Coker (CAR); Chris Godwin (TB); Darren Waller (CAR); Malik Nabers (NYG); Nico Collins (HOU); Isaiah Likely (NYG); Jaylin Noel (HOU); Dalton Schultz (HOU); Xavier Hutchinson (HOU); Kayshon Boutte (HOU); Drake London (ATL); George Kittle (SF); Ja'Marr Chase (CIN); Tee Higgins (CIN); Mike Gesicki (CIN); Josh Downs (IND); Garrett Wilson (NYJ); Greg Dulcich (MIA); Mason Taylor (NYJ); Jerry Jeudy (CLE); Elic Ayomanor (TEN); Trey McBride (ARI); Troy Franklin (DEN); Elijah Higgins (ARI); Christian Watson (GB); Tucker Kraft (GB); Sam LaPorta (DET); Brock Bowers (LV); Tre Tucker (LV); Michael Mayer (LV); Davis Allen (LA); Jaxon Smith-Njigba (SEA); Cooper Kupp (SEA); Tory Horton (SEA); Kyle Pitts (ATL); Puka Nacua (LA)

### Receptions (31)

Chris Olave (NO); DK Metcalf (PIT); Devaughn Vele (NO); Juwan Johnson (NO); Pat Freiermuth (PIT); Chris Godwin (TB); Tommy Tremble (CAR); Malik Nabers (NYG); Nico Collins (HOU); Dalton Schultz (HOU); Kayshon Boutte (HOU); Foster Moreau (HOU); Xavier Hutchinson (HOU); George Kittle (SF); Jahan Dotson (ATL); Ja'Marr Chase (CIN); Tee Higgins (CIN); Garrett Wilson (NYJ); Mason Taylor (NYJ); Greg Dulcich (MIA); Wan'Dale Robinson (TEN); Jerry Jeudy (CLE); Trey McBride (ARI); Sam LaPorta (DET); Christian Watson (GB); Tucker Kraft (GB); Brock Bowers (LV); Tre Tucker (LV); Jaxon Smith-Njigba (SEA); AJ Barner (SEA); Puka Nacua (LA)

## Validation and lock

- [x] Exact persisted Stage 1 State reloaded and validated.
- [x] All 128 Stage 1 records and locked L10 observations preserved.
- [x] All 1175 valid FanDuel alternate lines with prices captured and scored against locked L10.
- [x] Core prices all fall within the inclusive -350 to -150 band.
- [x] Floor/Core/Ceiling selected by the stated rules.
- [x] No cross-book or line-movement analysis.
- [x] No detailed current-week context research.
- [x] Stage 1 qualification status and historical evidence unchanged.
- [x] Stage 2 State persisted, reloaded, and validated.

**STOP — Stage 2 is complete. Wait for explicit user instruction before Stage 3.**
