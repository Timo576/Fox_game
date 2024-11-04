# Fox_game

Code to mess around with strategies for AlexCheddar's fox game.
Conclusion: strategy does not matter. 

# Sa-to-ri's explanation:

"I think this should be a generally correct argument:

We have n remaining tiles and want to calculate the probability of a specific tile landing on a specific square:

Let's say we place our first tile on the square, then the probability is easy: 1/n

On the other hand, if we decide to place our second tile on the square, the probability is:
((n - 1)/n)*(1/(n - 1)) = 1*(n - 1)/n*(n - 1) = 1/n

So far so good, but what about placing it third:
((n - 1)/n)*((n - 2)/(n - 1))*(1/(n - 2)) = 1*(n - 1)*(n - 2)/n*(n - 1)*(n - 2) = 1/n

The general rule is that if we place our m:th tile on the square, the probability is:

(n - 1)/n)*((n - 2)/(n - 1))* ... *((n - m)/(n - (m - 1)))*(1/(n - m))

Note that the divisors and the dividends are all multiplied together, and that you get pairs of all (n - 1) ... (n - m). The only unpaired dividend is 1 and the only unpaired divisor is n, always giving you the result 1/n after cancellation.

The conclusion we can draw from this, is that for any board state, the probability of placing any specific tile on any specific square is always 1/n (and it does not matter if you place it as your first, third or last tile)."

# Code stuffs
Code should run in between 10s and 10 mins depending on how complex your strategy is and what initial board you are using.
To set an initial board set the values in the initial board array like in the diagonal rule set.
Then change the number of starting f's, o's, and x's. to match.

To set a strategy create a function that takes as input a tile order (np array of strings F, O and X), the initial board (np array of strings Blank, F, O and X) and the number of starting f's o's and x's.
You may not look at the tile order, it is only used to update the value of the board (choices must be based on number of current F,O,X's).
Ensure you always place the tile, rather than throwing it out if theres is no matching places.

Yes it could be optimized a ton, I didn't see the point.
