from .die import Die
import pandas as pd
import numpy as np

class Game():
    
    def __init__(self, dice):
        """Initialize a Game with a list of dice.
        
        Input:
            dice (list): List of Die objects with identical faces.
        
        Raises:
            TypeError: If any element in dice is not a Die object.
            ValueError: If dice don't have identical faces.
        """
        if not isinstance(dice, list) or len(dice) < 1:
            raise ValueError('Must be a list of dice')
        
        # Check if all elements are Die class
        for die in dice:
            if not isinstance(die, Die):
                raise TypeError('All elements must be a Die object')
        
        # Check identical faces
        first = set(dice[0].get_data().index)
        for die in dice[1:]:
            if set(die.get_data().index) != first:
                raise ValueError('All dice must have identical faces')
        
        self.dice = dice
        self.results = None
        
    
    def play(self, rolls):
        """Play the game by rolling the dice.
        
        Input:
            rolls (int): Number of times to roll each die.
        
        Raises:
            TypeError: If rolls is not an integer.
            ValueError: If rolls is less than 1.
        """
        if not isinstance(rolls, int):
            raise TypeError('Number of rolls must be an integer.')
        if rolls < 1:
            raise ValueError('Number of rolls must be a positive integer.')
        
        # Create the list
        results = {}
        for i, die in enumerate(self.dice):
            results[i] = die.roll(rolls)

        self.results = pd.DataFrame(results)
        
    def show_results(self, form='wide'):
        """Show the most recent game results.
        
        Input:
            form (str): 'wide' or 'narrow' format.
            
        Returns:
            pandas.DataFrame: Results in requested format.
            
        Raises:
            ValueError: If no results available or invalid format.
        """
        if self.results is None:
            raise ValueError("Play the game first.")
        
        if form == 'wide':
            return self.results.copy()
        elif form == 'narrow':
            narrow_df = self.results.stack().reset_index()
            narrow_df.columns = ['Rolls', 'Die', 'Face']
            return narrow_df.set_index(['Rolls', 'Die'])
        else:
            raise ValueError('Format must be either \'wide\' or \'narrow\'')
        