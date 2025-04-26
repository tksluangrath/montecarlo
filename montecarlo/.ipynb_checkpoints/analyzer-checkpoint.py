from .game import Game
import numpy as np
import pandas as pd

class Analyzer():
    
    def __init__(self, game):
        """Initialize the Analyzer class with a Game object.
        
        Inputs:
            game: A Game object to analyze.
            
        Raises:
            ValueError: If input is not a Game object.
        """
        if not isinstance(game, Game):
            raise ValueError('Input must be a Game object.')
        self.game = game
        self.results = None
        
    def _check_results(self):
        """Private method to check if results are available."""
        if self.game.results is None:
            raise ValueError("No game results available. Play the game first.")
        self.results = self.game.show_results()
    
    
    def jackpot(self):
        """Count the number of jackpot rolls (all faces are identical).
        
        Returns:
            int: Number of jackpot.
        
        Raises:
            ValueError: If no game was play.
        """
        self._check_results()
        return int((self.results.nunique(axis=1) == 1).sum())
    
    
    def face_counts_per_roll(self):
        """Count occurrences of each face in each rolls.
        
        Returns:
            pd.DataFrame: Wide format with roll numbers, face counts
            
        Raises:
            ValueError: If no game was play
        """
        self._check_results()
        counts_df = self.results.apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)
        face_order = self.game.dice[0].get_data().index.tolist()
        return counts_df.reindex(columns = face_order, fill_value = 0)
        
        
    def combo_count(self):
        """Count distinct combination of faces.
        
        Returns:
            pd.DataFrame: MultiIndex of combinations with counts.
        
        Raises:
            ValueError: If no game was play.
        """
        self._check_results()    
        combos = self.game.results.apply(lambda row: tuple(sorted(row)), axis=1)
        counts = combos.value_counts().reset_index()
        counts.columns = ['Combination', 'Counts']
        counts = counts.set_index('Combination')
        counts.index = pd.MultiIndex.from_tuples(counts.index, 
                                                 names=[f'{i}' for i in range(self.game.results.shape[1])]
                                                )
        return counts
    
    
    def permutation_count(self):
        """Count distinct permutations of faces.
        
        Returns:
            pd.DataFrame: MultiIndex of permutations with counts.
            
        Raises:
            ValueError: If no game was play.
        """
        self._check_results()
        perms = self.game.results.apply(lambda row: tuple(row), axis=1)
        counts = perms.value_counts().rename('Counts').to_frame()
        counts.index = pd.MultiIndex.from_tuples(
            counts.index,
            names=[f'{i}' for i in range(self.game.results.shape[1])])
        return counts