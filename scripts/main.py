import subprocess
import sys
import argparse
from pathlib import Path

# Define all available scripts organized by category
SCRIPTS = {
    'characterization': [
        'participant_characterization/characterization.py'
    ],
    'rq1': [
        'RQ1/coding_bias.py'
    ],
    'rq2': [
        'RQ2/profile.py'
    ],
    'rq3': [
        'RQ3/company.py'
    ],
    'rq4': [
        'RQ4/leaders.py',
        'RQ4/teams.py'
    ],
    'rq5': [
        'RQ5/coding_inclusion_diversity.py',
        'RQ5/diversitycloud.py'
    ],
    'rq6': [
        'RQ6/coding_discrimination_prejudice.py',
        'RQ6/discriminationcloud.py'
    ]
}

def run_script(script_path, verbose=True):
    """
    Execute a Python script and handle its output.
    
    Args:
        script_path: Path to the script relative to the scripts directory
        verbose: Whether to print detailed output
    
    Returns:
        True if successful, False otherwise
    """
    full_path = Path(__file__).parent / script_path
    
    if not full_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"▶️  Running: {script_path}")
        print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(full_path)],
            cwd=full_path.parent,
            capture_output=not verbose,
            text=True,
            check=True
        )
        
        if verbose:
            print(f"✅ Completed: {script_path}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_path}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error running {script_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Run analysis scripts for the Diversity4BRSE study',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --all                    # Run all scripts
  python main.py --rq1 --rq2              # Run RQ1 and RQ2 scripts
  python main.py --characterization       # Run only characterization
  python main.py --rq4 --rq5 --rq6        # Run RQ4, RQ5, and RQ6
  python main.py --all --quiet            # Run all scripts with minimal output
        """
    )
    
    # Add flags for each category
    parser.add_argument('--all', action='store_true',
                        help='Run all scripts')
    parser.add_argument('--characterization', action='store_true',
                        help='Run participant characterization scripts')
    parser.add_argument('--rq1', action='store_true',
                        help='Run RQ1 (bias recognition) scripts')
    parser.add_argument('--rq2', action='store_true',
                        help='Run RQ2 (demographic profile) scripts')
    parser.add_argument('--rq3', action='store_true',
                        help='Run RQ3 (company characteristics) scripts')
    parser.add_argument('--rq4', action='store_true',
                        help='Run RQ4 (team and leadership) scripts')
    parser.add_argument('--rq5', action='store_true',
                        help='Run RQ5 (diversity & inclusion definitions) scripts')
    parser.add_argument('--rq6', action='store_true',
                        help='Run RQ6 (discrimination & prejudice definitions) scripts')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Minimize output (only show summary)')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    # Determine which scripts to run
    scripts_to_run = []
    
    if args.all:
        # Run all scripts in order
        for category in ['characterization', 'rq1', 'rq2', 'rq3', 'rq4', 'rq5', 'rq6']:
            scripts_to_run.extend(SCRIPTS[category])
    else:
        # Run selected scripts
        if args.characterization:
            scripts_to_run.extend(SCRIPTS['characterization'])
        if args.rq1:
            scripts_to_run.extend(SCRIPTS['rq1'])
        if args.rq2:
            scripts_to_run.extend(SCRIPTS['rq2'])
        if args.rq3:
            scripts_to_run.extend(SCRIPTS['rq3'])
        if args.rq4:
            scripts_to_run.extend(SCRIPTS['rq4'])
        if args.rq5:
            scripts_to_run.extend(SCRIPTS['rq5'])
        if args.rq6:
            scripts_to_run.extend(SCRIPTS['rq6'])
    
    if not scripts_to_run:
        print("⚠️  No scripts selected. Use --help to see available options.")
        sys.exit(1)
    
    # Print execution plan
    print("\n" + "="*60)
    print("📊 DIVERSITY4BRSE ANALYSIS PIPELINE")
    print("="*60)
    print(f"Scripts to execute: {len(scripts_to_run)}")
    for i, script in enumerate(scripts_to_run, 1):
        print(f"  {i}. {script}")
    print("="*60 + "\n")
    
    # Execute scripts
    verbose = not args.quiet
    success_count = 0
    failure_count = 0
    failed_scripts = []
    
    for script in scripts_to_run:
        if run_script(script, verbose=verbose):
            success_count += 1
        else:
            failure_count += 1
            failed_scripts.append(script)
    
    # Print summary
    print("\n" + "="*60)
    print("📈 EXECUTION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {success_count}/{len(scripts_to_run)}")
    
    if failure_count > 0:
        print(f"❌ Failed: {failure_count}/{len(scripts_to_run)}")
        print("\nFailed scripts:")
        for script in failed_scripts:
            print(f"  - {script}")
        sys.exit(1)
    else:
        print("🎉 All scripts executed successfully!")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
