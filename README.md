# AI Planner
## Created by: Riley Alden, Archer James, Megdalia Bromhal, Long Nguyen
- Lead Developer: Archer James

## Build from scratch instructions

### Setting up repo & Reflex
1. Clone repository in desired directory
   ```
   git clone https://github.com/UNCW-CSC-450/csc450-fa24-team3.git
   ```
   
2. Create virtual environment

   **Windows users**

     ```
     # Redirecting to the repository folder (where you'll initialize your virtual environment)
     cd csc450-fa24-team3 
     py -3 -m venv .venv # Setting up virtual environment
     ```
     ```
     .venv\\Scripts\\activate # Activating virtual environment
     ```
     ```
     deactivate # deactivate virtual environment (after you're done with the application)
     ```
   **Mac/Linux users**
     ```
     # Redirecting to the repository folder (where you'll initialize your virtual environment)
     cd csc450-fa24-team3 
     python3 -m venv .venv # Setting up virtual environment
     ```
     ```
     source .venv/bin/activate # Activating virtual environment
     ```
     ```
     deactivate # How you can deactivate virtual environment (after you're done with the application)
     ```
     
3. Install Reflex & Other Packages
   ```
   pip install reflex # May have to use pip3
   pip install openai # OpenAI API package
   pip install requests # For Canvas API requests, OR python3 -m pip install types-requests
   ```
   
4. Run Reflex
   ```
   cd csc450-fa24-team3/AIPlanner # Redirecting to the AIPlanner folder
   reflex run # Running Reflex
   ```

### Setting up Reflex database (automated by running dbresetscript.bat OR dbresetscriptMAC.sh)

1. Initialize Reflex database

   ```
   # While in csc450-fa24-team3/AIPlanner
   reflex db init
   ```

2. Update database format

   ```
   # While in csc450-fa24-team3/AIPlanner
   reflex db makemigrations
   ```

3. Updata database data

   ```
   # While in csc450-fa24-team3/AIPlanner
   reflex db migrate
   ```

### Accessing AIPlanner Web Application (running Reflex)

   ```
   # While in csc450-fa24-team3/AIPlanner
   reflex run
   ```
  Go to http://localhost://3000 in browser, or whatever port Reflex directs you to in terminal after running Reflex.


## References
https://reflex.dev/docs/getting-started/installation/
