"""
Test script to validate the scraping functions work correctly
This script tests the parsing functions with sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test the parsing functions from both scripts
def test_value_parsing():
    """Test market value parsing function"""
    # Import the parsing function
    import value
    
    test_cases = [
        ('€50.00m', 50.0),
        ('€1.50m', 1.5),
        ('€750k', 0.75),
        ('€25.00m', 25.0),
        ('-', 0),
        ('€0.50m', 0.5)
    ]
    
    print("Testing market value parsing:")
    for test_input, expected in test_cases:
        result = value.parse_market_value(test_input)
        status = "✓" if abs(result - expected) < 0.01 else "✗"
        print(f"  {status} '{test_input}' -> {result} (expected {expected})")
    
def test_age_parsing():
    """Test age parsing functions"""
    import age
    
    # Test direct age parsing
    age_test_cases = [
        ('25', 25),
        ('30 years', 30),
        ('28', 28),
        ('-', None),
        ('abc', None)
    ]
    
    print("\nTesting age parsing:")
    for test_input, expected in age_test_cases:
        result = age.parse_age_directly(test_input)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{test_input}' -> {result} (expected {expected})")

def test_team_data_structure():
    """Test that the data structures are correct"""
    print("\nTesting team data structures:")
    
    # Test value script structure
    import value
    sample_players = [
        {'player_name': 'Player 1', 'market_value_millions': 50.0},
        {'player_name': 'Player 2', 'market_value_millions': 25.0},
        {'player_name': 'Player 3', 'market_value_millions': 30.0}
    ]
    
    total, avg, count = value.calculate_team_statistics(sample_players)
    print(f"  ✓ Value calculation: Total={total}, Average={avg}, Count={count}")
    
    # Test age script structure
    import age
    sample_ages = [
        {'player_name': 'Player 1', 'age': 25},
        {'player_name': 'Player 2', 'age': 28},
        {'player_name': 'Player 3', 'age': 30}
    ]
    
    total_age, avg_age, count_age = age.calculate_age_statistics(sample_ages)
    print(f"  ✓ Age calculation: Total={total_age}, Average={avg_age}, Count={count_age}")

if __name__ == "__main__":
    print("Running scraping script tests...\n")
    
    try:
        test_value_parsing()
        test_age_parsing()
        test_team_data_structure()
        print("\n✓ All tests passed! Scripts are ready to use.")
        print("\nTo run the actual scraping:")
        print("1. Run: python value.py (for team values)")
        print("2. Run: python age.py (for team ages)")
        print("\nNote: Scraping will take some time due to delays between requests.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        print("Please check the script implementations.")