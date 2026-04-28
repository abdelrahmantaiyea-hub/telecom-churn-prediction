import subprocess
import sys
import os

def main():
    # Clear the terminal screen for a clean look
    os.system('cls' if os.name == 'nt' else 'clear')

    print("==============================================")
    print("   CELL2CELL CHURN DECISION SYSTEM - v1.0")
    print("==============================================")
    print("1. [TRAIN] Run End-to-End Training Pipeline")
    print("2. [DEPLOY] Launch Streamlit Dashboard")
    print("3. [EXIT] Quit Application")
    print("----------------------------------------------")
    
    choice = input("Enter selection (1-3): ")
    
    if choice == '1':
        print("\n> Starting Training Pipeline...")
        subprocess.run([sys.executable, "src/pipeline/training_pipeline.py"])
        
    elif choice == '2':
        print("\n> Launching Streamlit Dashboard...")
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        
    elif choice == '3':
        print("Exiting application. Goodbye!")
        sys.exit()
    else:
        print("Invalid Selection. Please run again and choose 1, 2, or 3.")

if __name__ == "__main__":
    main()