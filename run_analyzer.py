import sys
import os
sys.path.append('scripts')

from analyzer import SimpleNepalAnalyzer

print("Starting Nepalese Data Analyzer...")
print("This will analyze earthquake, temperature, and exam data.")

analyzer = SimpleNepalAnalyzer()
analyzer.run_all()

print("\nPress Enter to exit...")
input()