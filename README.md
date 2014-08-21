### Soccer games and standings processing

A simple python3 tool for importing and exporting soccer standings and game results.

#### Example game data

    Season: 2008
    Competition: SuperLiga
    Stage: elimination
    Round: Final

    3/29/2008; FC Dallas; 3-1 (aet); Chivas Guadalajara; Laredo, TX; Alex Prus; 130000
    Ruben Luna 3, Ruben Luna 10, Hugo Sanchez 92; Chicharito 19
    FC Dallas: Matt Jordan, Chris Gbandi, Clarence Goodson, George John, Zach Loyd, Brek Shea, Oscar Pareja, Leonel Alvarez, Ronnie O'Brien, Jason Kreis, Carlos Ruiz
    Source: FC Dallas Media Guide


#### Example statistical data

    Season: 2012
    Competition: Major League Soccer
    Stage: regular
    Key: player; games_played; goals; assists

    Chris Wondolowski; 28; 14; 3
    Thierry Henry; 22; 8; 9
    Osvaldo Alonso; 30; 3; 4


Stats are defined using a key that takes arbitrary fields. 
Some fields are automatically processed (birthdate, eg)


#### Example standing data

     Season: 2013
     Competition: North American Soccer League (2011-)
     Stage: Clausura

     Key: team; games; wins; ties; losses; points; goals_for; goals_against
     
     New York Cosmos; 14; 7; 3; 4; etc.


Standings are formatted very much like statistics.