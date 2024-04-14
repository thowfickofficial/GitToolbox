import subprocess
import os
import tkinter as tk
from tkinter import filedialog

def is_git_repository(repo_path):
    return os.path.exists(os.path.join(repo_path, '.git'))

def initialize_git_repo(repo_path):
    subprocess.run(['git', 'init'], cwd=repo_path)
    print("Initialized a new Git repository.")

def configure_git_user(repo_path):
    git_username = input("Enter your Git username: ")
    git_email = input("Enter your Git email: ")
    subprocess.run(['git', 'config', 'user.name', git_username], cwd=repo_path)
    subprocess.run(['git', 'config', 'user.email', git_email], cwd=repo_path)
    print("Git username and email configured.")

def git_add_commit_push(repo_path, commit_message, branch='master', create_branch=False, pull_changes=False, add_option='all', amend=False, upstream_branch=None):
    try:
        # Change directory to the repository path
        subprocess.run(['git', 'checkout', branch], cwd=repo_path)

        if pull_changes:
            subprocess.run(['git', 'pull', 'origin', branch], cwd=repo_path)
        
        if add_option == '1':
            subprocess.run(['git', 'add', '.'], cwd=repo_path)
        elif add_option == '2':
            specific_files = input("Enter the specific files or patterns to add (space-separated): ").split()
            subprocess.run(['git', 'add'] + specific_files, cwd=repo_path)
        elif add_option == '3':
            subprocess.run(['git', 'add', '--all'], cwd=repo_path)
        
        if amend:
            subprocess.run(['git', 'commit', '--amend', '-m', commit_message], cwd=repo_path)
        else:
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_path)
        
        if create_branch:
            subprocess.run(['git', 'checkout', '-b', branch, upstream_branch], cwd=repo_path)
        else:
            subprocess.run(['git', 'checkout', branch], cwd=repo_path)
        
        # Push changes to the remote repository
        subprocess.run(['git', 'push', 'origin', branch], cwd=repo_path)
        
        print("Changes added, committed, and pushed successfully.")
    except Exception as e:
        print("An error occurred:", e)
        
def add_git_remote(repo_path):
    remote_name = input("Enter the name of the remote (e.g., 'origin'): ") or 'origin'
    remote_type = input("Enter the type of remote URL ('https' or 'ssh'): ")
    remote_url = input(f"Enter the {remote_type} URL of the remote repository: ")
    
    subprocess.run(['git', 'remote', 'add', remote_name, remote_url], cwd=repo_path)
    print(f"Remote '{remote_name}' added with {remote_type} URL: {remote_url}")


if __name__ == "__main__":
    print("\n\n\t GitCommanderHub\n")
    print("Git Automation Script")
    print("---------------------")
    print("This script helps you automate common Git actions.")
    print("Here are the available options:")
    print("1.  Initialize a new Git repository.")
    print("2.  Configure Git username and email.")
    print("3.  Clone a repository.")
    print("4.  Add, commit, and push changes.")
    print("5.  Revert the last commit.")
    print("6.  Check out a specific commit.")
    print("7.  View commit history.")
    print("8.  Create and apply patches.")
    print("9.  Pull changes from the remote repository.")
    print("10. Add Git remote.")
    print()

    option = input("Select the option number to perform the desired action: ")
    
    if option == '1':
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        
        # Open a file dialog to select the repository path
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        
        initialize_git_repo(repository_path)
        configure_git_user(repository_path)
        print("Git repository initialized and configured.")
        add_git_remote(repository_path)
        print("Continuing to adding, committing, and pushing changes...")
        
        add_option = input("Choose the files to add:\n"
                           "1. Add all modified files.\n"
                           "2. Add specific files or patterns.\n"
                           "3. Add all changes, including untracked files.\n"
                           "Enter the option number (1/2/3): ")
        commit_msg = input("Enter the commit message: ")
        branch_name = input("Enter the branch name (default is master): ") or 'master'
        git_add_commit_push(repository_path, commit_msg, branch_name, add_option=add_option)
    
    
    elif option == '2':
        repository_path = input("Enter the path to your directory: ")
        configure_git_user(repository_path)
    
    elif option == '3':
        repository_url = input("Enter the URL of the repository to clone: ")
        destination_path = input("Enter the destination path for cloning: ")
        subprocess.run(['git', 'clone', repository_url, destination_path])
        print(f"Repository cloned to {destination_path}.")
    
    elif option == '4':
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        
        # Open a file dialog to select the repository path
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        commit_msg = input("Enter the commit message: ")
        branch_name = input("Enter the branch name (default is master): ") or 'master'
        create_new_branch = input("Create a new branch? (y/n): ").lower() == 'y'
        
        if create_new_branch:
            new_branch_name = input("Enter the name of the new branch: ")
            upstream_branch = input("Enter the upstream branch (press Enter to use the same name): ") or new_branch_name
            git_add_commit_push(repository_path, commit_msg, branch_name, create_new_branch, upstream_branch=upstream_branch)
        else:
            pull_before_push = input("Pull changes from the remote before pushing? (y/n): ").lower() == 'y'
            add_option = input("Choose the files to add:\n"
                               "1. Add all modified files.\n"
                               "2. Add specific files or patterns.\n"
                               "3. Add all changes, including untracked files.\n"
                               "Enter the option number (1/2/3): ")
            amend_commit = input("Amend the previous commit? (y/n): ").lower() == 'y'
            
            git_add_commit_push(repository_path, commit_msg, branch_name, False, pull_before_push, add_option, amend_commit)
    
    elif option == '5':
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        
        # Open a file dialog to select the repository path
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        subprocess.run(['git', 'reset', '--soft', 'HEAD~1'], cwd=repository_path)
        print("Last commit reverted.")
    
    elif option == '6':
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        
        # Open a file dialog to select the repository path
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        commit_hash = input("Enter the commit hash to check out: ")
        subprocess.run(['git', 'checkout', commit_hash], cwd=repository_path)
        print(f"Checked out commit {commit_hash}.")
    
    elif option == '7':
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        
        # Open a file dialog to select the repository path
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        subprocess.run(['git', 'log'], cwd=repository_path)
    
    elif option == '8':
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        
        # Open a file dialog to select the repository path
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        patch_name = input("Enter a name for the patch file: ")
        subprocess.run(['git', 'format-patch', '-o', patch_name], cwd=repository_path)
        print(f"Patch file '{patch_name}' created.")
        apply_patch = input("Apply a patch file? (y/n): ").lower() == 'y'
        if apply_patch:
            patch_file = input("Enter the patch file name: ")
            subprocess.run(['git', 'apply', patch_file], cwd=repository_path)
            print(f"Patch '{patch_file}' applied.")
    
    elif option == '9':
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        
        # Open a file dialog to select the repository path
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        branch_name = input("Enter the branch name to pull changes from (default is master): ") or 'master'
        subprocess.run(['git', 'pull', 'origin', branch_name], cwd=repository_path)
        print(f"Changes pulled from the remote repository into branch {branch_name}.")
    
    elif option == '10':
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        
        # Open a file dialog to select the repository path
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        add_git_remote(repository_path)