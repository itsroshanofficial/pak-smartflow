import unittest
from pak_smartflow_engine import pak_smartflow_engine

class TestPakSmartFlowEngine(unittest.TestCase):
    
    def test_engine_output_keys(self):
        # Test with standard input values
        result = pak_smartflow_engine(
            confidence=0.95,
            severity=0.80,
            safety_risk=0.50,
            traffic_density=0.50,
            vehicle_history=0.30,
            predicted_risk=0.40,
            compliance=0.70
        )
        
        # Verify that all expected keys are present in the output dictionary
        self.assertIn("Risk Score", result)
        self.assertIn("Fuzzy Decision Score", result)
        self.assertIn("Final Decision Score", result)
        self.assertIn("Recommended Action", result)

    def test_engine_extreme_high_risk(self):
        # Test with extreme high-risk parameters
        result = pak_smartflow_engine(
            confidence=0.99,
            severity=1.00,
            safety_risk=0.90,
            traffic_density=0.90,
            vehicle_history=0.90,
            predicted_risk=0.90,
            compliance=0.10
        )
        
        # Final decision score should reflect high risk
        self.assertGreaterEqual(result["Final Decision Score"], 0.5)

if __name__ == '__main__':
    unittest.main()
