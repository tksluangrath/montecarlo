
# Monte Carlo Simulator
author: Terrance Luangrath


## Synposis

A Python module for Monte Carlo Simulator simulations using three classes:

1. `Die`: Represents a die with customizable faces and weights.
2. `Game`: Simulates rolling one or more dice multiple times.
3. `Analyzer`: Computes statistical properties of game results.


### Installation

Using pip install, the package will download.

```python 
pip install montecarlo
```

### Import

```python
import montecarlo
```

### Quick Demonstration
```python
from montecarlo import Die, Game, Analyer

# 1. Create a 6-sided die and set weights
die = Die([1, 2, 3, 4, 5, 6])
die.change_weight(face=6, weight=2.0) # Make 6 twice as likely

# 2. Play a game: Roll 5 dice 100 times
game = Game(dice=[die] * 5) # Play with 5 identical die
game.play(rolls=100) # Roll each die 100 times

# 3. Analyze results
analyzer = Analyzer(game)

jackpot_count = analyzer.jackpot() # Count rolls where all dice show the same faces
face_distribution = analyzer.face_counts_per_roll() # Frequency of each face per rolls
combo_distribution = analyzer.combo_count()
permutation_distribution = analyzer.permutation_count()
```


## API description

### Die 

**Constructor**

`Die(faces)`

Initializes a `Die` object with distinct face values

- Parameters:
    - `faces` (`numpy.ndarray`): An array of face values (e.g., numbers, letters). Must be distinct values.
- Raises:
    - `IndexError`: If `faces` is not a NumPy array.
    - `ValueError`: If any values in `faces` are not distinct.

**Methods**

`change_weight(face_value, new_weight)`

Updates the weight associated of a specific face on the die. 

- Parameters:
    - `face_value` (`int`, `str`): The face need to update.
    - `new_weight` (`int`, `float`, `str`): The new weight value.
- Raises
    - `IndexError`: If `face_value` is not in the die.
    - `TypeError`: If the new weight is not a numeric type.
    - `ValueError`: If the new weight is invalid (e.g., negative or non-convertible). 

`get_data()`

Returns a copy of the die's current data.

- Returns:
    - `pandas.DataFrame`: A DataFrame with columns `Face` and `Weight`. 
    
`roll(dice_rolls = 1)`
Simulates rolling the die one or more time.

- Parameters:
    - `die_rolls` (`int`): Number of rolls to perform (default = 1).
- Returns:
    - `list`: A list of outcomes corresonding to each roll.
- Raises:
    - `TypeError`: If `dice_rolls` is not an integer.
    - `ValueError`: If `dice_rolls` is less than 1. 

### Game

**Constructor**

`Game(dice)`

Initalizes a new `Game` instance using a list of `Die` objects.

- Parameters:
    - `dice` (`list`): A list of `Die` objects. All dice must have the same set of faces.
- Raises:
    - `TypeError`: If any element in `dice` is not an instance of the `Die` class.
    - `ValueError`: If the dice do not have identical faces.
    
**Method**

`play(rolls)`

Plays the game by rolling all dice a specified numberf of times. Results are saved internally.

- Parameters:
    - `rolls` (`int`): The number of times each die should be rolled.
- Raises:
    - `TypeError`: If rolls is not an integer.
    - `ValueError`: If rolls is less than 1.
    
`show_results(form='wide')`

Returns the most recent game results.

- Parameters:
    - `form` (`str`): Format of the results
        - `wide` (default): Each die is a column; rows represent each roll.
        - `narrow`: A long-format DataFrame with roll number, die number, and outcome. 
- Returns:
    - `pandas.DataFrame`: A DataFrame of roll outcomes in specific format.
- Raises
    - `ValueError`: If no rolls have been performed or if an invalid format is requested. 
    
### Analyzer

**Constructor**

`Analyzer(game)`

Initializes the `Analyzer` with a `Game` object.

- Parameters:
    - `game` (`Game`): A previously played `Game` instance with results.
- Raises:
    - `ValueError`: If the input is not a valid `Game` object.
    
**Method**

`jackpot()`

Counts how many rolls resulted in a *jackpot*. All dice in a single roll showing the same face.

- Returns:
    - `int`: The number of jackpot rolls.
- Raises:
    - `RuntimeError`: If no results exist to analyze (i.e., game not played). 
    
`face_counts_per_roll()`

Calculates how many times each face appears in each roll.

- Returns:
    - `pandas.DataFrame`: A DataFrame in wide format showing counts.
- Raises:
    - `RuntimeError`: If no results exist to analyze (i.e., game not played).

`combo_count()`

Counts the frequency of each combination of faces rolled.

- Returns:
    - `pandas.DataFrame`: A MultiIndex DataFrame where each row is a unique combination and the value is the count of its occurence.
- Raises:
    - `RuntimeError`: If no results exist to analyze (i.e., game not played).

`permutation_count()`

Counts the frequency of each permutation of faes rolled, preserving order.

- Returns:
    - `pandas.DataFrame`: A MultiIndex Dataframe showing all unique permutations and their frequency.
- Raises:
    - `RuntimeError`: If no results exist to analyze (i.e., game not played).