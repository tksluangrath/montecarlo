import numpy as np
import pandas as pd

class Die():
    
    def __init__(self, faces):
        """Initialize the Die class
        
        Input:
            faces (numpy.ndarray): Array of faces with distinct values.
            
        Raises:
            TypeError: If input is not a Numpy array.
            ValueError: If values are not distinct.
        """
        # Check if faces is a NumPy array
        if not isinstance(faces, np.ndarray):
            raise TypeError('Must be a NumPy array')
        
        # Check if all values are distinct
        if len(np.unique(faces)) != len(faces):
            raise ValueError('All values in the array must be distinct')
            
        # Initializes weights
        weights = np.ones_like(faces, dtype=float)
        
        # Create private dataframe
        self.dataframe = pd.DataFrame({'weights':weights}, index = faces)
        
    
    def change_weight(self, face_value, new_weight):
        """Change weight of a specific face.
        
        Input:
            face_value (int): The face need to update.
            new_weight (int, float, str): The new weight value.
        
        Raises:
            IndexError: If face_value is not in the die.
            TypeError: If the new weight is not a numeric type.
            ValueError: If the new weight is invalid.
        """
        # Check for existing faces
        if face_value not in self.dataframe.index:
            raise IndexError(f'Face value, {face_value}, is not found')

        # Handle numeric weights
        if isinstance(new_weight, (int, float)):
            self.dataframe.loc[face_value, 'weights'] = float(new_weight)
        # Handle string weights
        elif isinstance(new_weight, str):
            try:
                self.dataframe.loc[face_value, 'weights'] = float(new_weight)
            except ValueError:
                raise TypeError('Weight must be numeric (int or float)')
        else:
            raise TypeError(f'Weights must be numeric (int or float)')
            
    
    def roll(self, dice_rolls=1):
        """Roll the dice one or more times.
        
        Input:
            dice_rolls (int): Number of times to roll the die (default = 1).
            
        Returns:
            list: Outcomes of each roll.
        
        Raises:
            TypeError: If times is not an integer.
            ValueError: If times is less than 1.
        """
        # Validate input
        if not isinstance(dice_rolls, int):
            raise TypeError("Number of rolls must be an integer.")
        if dice_rolls < 1:
            raise ValueError("Number of rolls must be positive.")
        
        # Get weighted probobality                     
        weights = self.dataframe['weights'].values
        normalized_weights = weights / weights.sum()
        
        # Perform random rolls
        outcomes = np.random.choice(
            self.dataframe.index.values,
            size=dice_rolls,
            p=normalized_weights
        )
        
        return list(outcomes)
    
    def get_data(self):
        """Returns a copy of the die's current dataframe.
            
        Returns:
            pandas.DataFrame: Copy of the die's faces and weights
        """
        return self.dataframe.copy()