import unittest
import numpy as np
import pandas as pd
from montecarlo.die import Die
from montecarlo.game import Game
from montecarlo.analyzer import Analyzer


class DieTestSuite(unittest.TestCase):
    
    def test_01_init_valid(self):
        """Test initialization with valid numeric and string faces."""
        # Valid input (numeric)
        faces_numeric = np.array([1, 2, 3, 4, 5, 6])
        dice = Die(faces_numeric)
        
        # Valid input (strings)
        faces_strings = np.array(['a', 'b', 'c', 'd'])
        dice = Die(faces_strings)
        
    def test_02_init_invalid_array(self):
        """Test initialization with invalid data types (should raise TypeError)."""
        # Invalid input (failed array)
        faces_list = [1, 2, 3, 4, 5, 6]
        with self.assertRaises(TypeError):
            dice = Die(faces_list)
    
    def test_03_init_invalid_distinct(self):
        """Test initialization with non-distinct values (should raise ValueError)."""
        # Invalid input (non-distinct values)
        with self.assertRaises(ValueError):
            dice = Die(np.array([1, 2, 2, 3]))
    
    def test_04_change_weight_valid_input(self):
        """Test changing weight with valid numeric input."""
        die = Die(np.array([1, 2, 3]))
        die.change_weight(2, 1.5) # Valid float
        self.assertEqual(die.dataframe.loc[2, 'weights'], 1.5)
        
        die.change_weight(1, 2)  # Valid integer
        self.assertEqual(die.dataframe.loc[1, 'weights'], 2.0)
        
    def test_05_change_weight_valid_string_input(self):
        """Test changing weight with valid string intput."""
        die = Die(np.array([1, 2, 3]))
        die.change_weight(2, "2") # String integer
        self.assertEqual(die.dataframe.loc[2, 'weights'], 2.0)
        
        die.change_weight(1, "1.5") # String float
        self.assertEqual(die.dataframe.loc[1, 'weights'], 1.5)
    
    def test_06_change_weight_invalid_face(self):
        """Test changing weight on non-existing face."""
        die = Die(np.array([1, 2, 3]))
        with self.assertRaises(IndexError):
            die.change_weight(10, 2)
            
    def test_07_invalid_datatypes(self):
        """Test changing weight with non-numeric values."""
        die = Die(np.array([1, 2, 3]))
        with self.assertRaises(TypeError):
            die.change_weight(3, "3..14")
            
    def test_08_roll_valid(self):
        """Test rolls with valid integer input."""
        die = Die(np.array([1, 2, 3]))
        
        # Test default roll
        result = die.roll()
        self.assertEqual(len(result), 1)
        
        # Test multiple rolls
        results = die.roll(10)
        self.assertEqual(len(results), 10)
        
    def test_09_roll_invalid(self):
        """Test rolls with invalid input."""
        die = Die(np.array([1, 2, 3]))
        
        with self.assertRaises(TypeError):
            die.roll("ten") # String input
        with self.assertRaises(TypeError):
            die.roll(2.0) # Float input
        with self.assertRaises(ValueError):
            die.roll(0) # Non-positive integer input
        with self.assertRaises(ValueError):
            die.roll(-1) # Negative integer input
    
    
    def test_10_get_data(self):
        """Test get_data() method."""
        faces = [1, 2, 3]
        die = Die(np.array([1, 2, 3]))
        die.change_weight(1, 0.4)
        df = die.get_data()
        
        # Verify Structure
        self.assertEqual(df.shape, (3, 1))
        self.assertTrue(np.array_equal(df.index.values, faces))
        self.assertTrue(np.array_equal(df['weights'].values, [0.4, 1.0, 1.0]))
        
        
class GameTestSuite(unittest.TestCase):
    
    def test_01_init(self):
        """Test initalization with valid input."""
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        
        game = Game([die1, die2])
        self.assertEqual(len(game.dice), 2)
    
    def test_02_mismatch_faces(self):
        """Test initalization with mismatch die object."""
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array(['A', 'B', 'C', 'D']))
        
        with self.assertRaises(ValueError):
            Game([die1, die2])
    
    def test_03_invalid_die_type(self):
        """Test initalization with non-Die object."""
        die1 = Die(np.array([1, 2, 3]))
        
        with self.assertRaises(TypeError):
            Game([die1, "die2"])
            
    def test_04_empty_list(self):
        """Test initalization with empty list."""
        with self.assertRaises(ValueError):
            Game([])
    
    def test_05_play_valid(self):
        """Test play() with valid rolls."""
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game1 = Game([die1, die2])
        
        game1.play(3)
        
    def test_06_play_invalid(self):
        """Test play() with invaild roll counts."""
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game1 = Game([die1, die2])
        
        with self.assertRaises(ValueError):
            game1.play(0)
            
        with self.assertRaises(ValueError):
            game1.play(-1)
            
        with self.assertRaises(TypeError):
            game1.play(3.14)
            
        with self.assertRaises(TypeError):
            game1.play("5")
            
    def test_07_show_results_wide_format(self):
        """Test show_results() with wide format."""
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game1 = Game([die1, die2])
        game1.play(3)
            
        results = game1.show_results('wide')
        
        # Verify structure
        self.assertIsInstance(results, pd.DataFrame)
        self.assertEqual(results.shape, (3, 2))
        
        # Verify all values are valid faces
        vaild_faces = {1, 2, 3, 4, 5, 6}
        for die in results.columns:
            self.assertTrue(all(face in vaild_faces for face in results[die]))
        
    def test_08_show_results_narrow_format(self):
        """Test show_results() with narrow format."""
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game1 = Game([die1, die2])
        game1.play(3)
        
        results = game1.show_results('narrow')
        
        # Verify structure
        self.assertIsInstance(results, pd.DataFrame)
        self.assertEqual(results.shape, (6, 1))
        
        # Verify all values are valid faces
        vaild_faces = {1, 2, 3, 4, 5, 6}
        for die in results.columns:
            self.assertTrue(all(face in vaild_faces for face in results[die]))
            
    def test_09_show_results_no_play(self):
        """ Test show_results() with 0 play."""
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game1 = Game([die1, die2])
        
        with self.assertRaises(ValueError):
            game1.show_results('wide')
            
        with self.assertRaises(ValueError):
            game1.show_results('narrow')
            
    def test_10_show_results_invalid(self):
        """Test show_results() with invalid input."""
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game1 = Game([die1, die2])
        game1.play(3)
        
        with self.assertRaises(ValueError):
            game1.show_results(4)
            
    def test_11_show_results_default(self):
        """Test show_results() with default format (wide)."""
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game1 = Game([die1, die2])
        game1.play(3)
            
        results = game1.show_results()
        
        # Verify structure
        self.assertIsInstance(results, pd.DataFrame)
        self.assertEqual(results.shape, (3, 2))
        
        # Verify all values are valid faces
        vaild_faces = {1, 2, 3, 4, 5, 6}
        for die in results.columns:
            self.assertTrue(all(face in vaild_faces for face in results[die]))

class TestAnalyzer(unittest.TestCase):
    
    def test_01_int_valid(self):
        """Test initalization with valid input."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        
        game1 = Game([die1, die2, die3])
        game1.play(100)
        
        game2 = Game([die1, die2, die3])
        
        analyzer1 = Analyzer(game1)
        analyzer2 = Analyzer(game2)
        
        self.assertIsInstance(analyzer1, Analyzer)
        self.assertIsInstance(analyzer1, Analyzer)
     
    
    def test_02_int_invalid(self):
        """Test initalization with invalid input."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        
        with self.assertRaises(ValueError):
            Analyzer(die1)
    
    
    def test_03_jackpot_valid(self):
        """Test jackpot method with valid input."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        
        game1 = Game([die1, die2, die3])
        game1.play(100)
                
        analyzer1 = Analyzer(game1)
        jackpots = analyzer1.jackpot()
        self.assertIsInstance(jackpots, int)
        
        # Force a jackpot
        analyzer1.game.results.iloc[0] = [1, 1, 1]
        self.assertGreaterEqual(analyzer1.jackpot(), 1)
        
        
    def test_04_jackpot_invalid(self):
        """Test jackpot method with no game played."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        
        game1 = Game([die1, die2, die3])
        
        analyzer1 = Analyzer(game1)
        
        with self.assertRaises(RuntimeError):
            analyzer1.jackpot()
        
        
    def test_05_faces_count_valid(self):
        """Test face counts method."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        
        game1 = Game([die1, die2, die3])
        game1.play(100)
        
        analyzer1 = Analyzer(game1)
        counts = analyzer1.face_counts_per_roll()
        
        self.assertIsInstance(counts, pd.DataFrame)
        self.assertEqual(counts.shape, (100, 6))
        self.assertListEqual(list(counts.columns), [1, 2, 3, 4, 5, 6])
        self.assertTrue((counts.sum(axis=1) == 3).all())
        
    
    def test_06_faces_count_invalid(self):
        """Test face counts method with no game played."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        
        game1 = Game([die1, die2, die3])
        
        analyzer1 = Analyzer(game1)
        
        with self.assertRaises(RuntimeError):
            analyzer1.face_counts_per_roll()
            
            
    def test_07_combo_count_valid(self):
        """Test combo counts method with valid game."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        
        game1 = Game([die1, die2, die3])
        game1.play(100)
        
        analyzer1 = Analyzer(game1)
        combos = analyzer1.combo_count()
        
        self.assertIsInstance(combos, pd.DataFrame)
        
        self.assertIsInstance(combos.index, pd.MultiIndex)
        self.assertEqual(combos.index.names, ['Die_1', 'Die_2', 'Die_3'])
        
        self.assertTrue((combos['Counts'] > 0).all())
        
        
    def test_08_combo_count_invalid(self):
        """Test combo counts method with no game played."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        
        game1 = Game([die1, die2, die3])
        
        analyzer1 = Analyzer(game1)
        
        with self.assertRaises(RuntimeError):
            analyzer1.combo_count()
            
            
    def test_09_permutation_count_invalid(self):
        """Test permutation counts method with no game played."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)
        
        game1 = Game([die1, die2, die3])
        
        analyzer1 = Analyzer(game1)
        
        with self.assertRaises(RuntimeError):
            analyzer1.permutation_count()
            
    def test_10_permutation_count_valid(self):
        """Test permutation with valid game played."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)

        # Test normal case with random rolls
        game1 = Game([die1, die2, die3])
        game1.play(100)
        analyzer1 = Analyzer(game1)
        perms = analyzer1.permutation_count()

        self.assertGreater(len(perms), 0)
        self.assertLessEqual(len(perms), 100) 

        # Verify MultiIndex structure
        self.assertIsInstance(perms.index, pd.MultiIndex)
        self.assertEqual(perms.index.names, ['Die_1', 'Die_2', 'Die_3'])

        # Verify counts sum to number of rolls
        self.assertEqual(perms['Counts'].sum(), 100) 
        
    def test_11_permutation_count_jackpot(self):
        """Test permutation count results."""
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        die3 = Die(faces)

        game = Game([die1, die2, die3])
        game.play(100)
        game.results.iloc[:, :] = 1  # Force all rolls to be (1,1,1)

        analyzer = Analyzer(game)
        perms = analyzer.permutation_count()

        # Should only have one permutation
        self.assertEqual(len(perms), 1)
        self.assertEqual(perms.iloc[0]['Counts'], 100)

        
if __name__ == '__main__':
    unittest.main(verbosity=3)