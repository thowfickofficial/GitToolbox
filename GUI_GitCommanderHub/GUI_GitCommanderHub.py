import subprocess
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

def is_git_repository(repo_path):
    return os.path.exists(os.path.join(repo_path, '.git'))

def initialize_git_repo(repo_path):
    subprocess.run(['git', 'init'], cwd=repo_path)
    print("Initialized a new Git repository.")

def configure_git_user(repo_path):
    git_username = simpledialog.askstring("Git Configuration", "Enter your Git username:")
    git_email = simpledialog.askstring("Git Configuration", "Enter your Git email:")
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
            specific_files = simpledialog.askstring("Specific Files", "Enter the specific files or patterns to add (space-separated): ")
            specific_files = specific_files.split()
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
    remote_name = simpledialog.askstring("Git Remote", "Enter the name of the remote (e.g., 'origin'):") or 'origin'
    remote_type = simpledialog.askstring("Git Remote", "Enter the type of remote URL ('https' or 'ssh'):")
    remote_url = simpledialog.askstring("Git Remote", f"Enter the {remote_type} URL of the remote repository:")
    
    subprocess.run(['git', 'remote', 'add', remote_name, remote_url], cwd=repo_path)
    print(f"Remote '{remote_name}' added with {remote_type} URL: {remote_url}")

def display_intro():
    introduction = (
        "GitCommanderHub\n"
        "---------------------\n"
        "This GitCommanderHub helps you automate common Git actions.\n"
        "Here are the available options:\n"
        "1.  Initialize a new Git repository.\n"
        "2.  Configure Git username and email.\n"
        "3.  Clone a repository.\n"
        "4.  Add, commit, and push changes.\n"
        "5.  Pull changes from the remote repository.\n"
        "6.  Add Git remote.\n"
    )
    intro_label.config(text=introduction)
    option = simpledialog.askstring("Options", "Select the option number to perform the desired action:")

    if option == '1':
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        if not is_git_repository(repository_path):
            initialize_git_repo(repository_path)
            configure_git_user(repository_path)
            add_git_remote(repository_path)
            
            add_option = simpledialog.askstring("Add Files", "Choose the files to add:\n"
                                                "1. Add all modified files.\n"
                                                "2. Add specific files or patterns.\n"
                                                "3. Add all changes, including untracked files.\n"
                                                "Enter the option number (1/2/3): ")
            commit_msg = simpledialog.askstring("Commit Message", "Enter the commit message:")
            branch_name = simpledialog.askstring("Branch Name", "Enter the branch name (default is master):") or 'master'
            git_add_commit_push(repository_path, commit_msg, branch_name, add_option=add_option)
        
        else:
            print("The selected directory is already a Git repository.")

    elif option == '2':
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        configure_git_user(repository_path)
    
    elif option == '3':
        repository_url = simpledialog.askstring("Repository URL", "Enter the URL of the repository to clone:")
        destination_path = filedialog.askdirectory(title="Select Destination Directory")
        subprocess.run(['git', 'clone', repository_url, destination_path])
        print(f"Repository cloned to {destination_path}.")
    
    elif option == '4':
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        commit_msg = simpledialog.askstring("Commit Message", "Enter the commit message:")
        branch_name = simpledialog.askstring("Branch Name", "Enter the branch name (default is master):") or 'master'
        create_new_branch = simpledialog.askstring("Create New Branch", "Create a new branch? (yes/no):")
        
        if create_new_branch.lower() == 'yes':
            new_branch_name = simpledialog.askstring("New Branch Name", "Enter the name of the new branch:")
            upstream_branch = simpledialog.askstring("Upstream Branch", "Enter the upstream branch:")
            git_add_commit_push(repository_path, commit_msg, branch_name, create_branch=True, upstream_branch=upstream_branch)
        else:
            pull_before_push = simpledialog.askstring("Pull Before Push", "Pull changes from the remote before pushing? (yes/no):")
            add_option = simpledialog.askstring("Add Files", "Choose the files to add:\n"
                                                "1. Add all modified files.\n"
                                                "2. Add specific files or patterns.\n"
                                                "3. Add all changes, including untracked files.\n"
                                                "Enter the option number (1/2/3): ")
            amend_commit = simpledialog.askstring("Amend Commit", "Amend the previous commit? (yes/no):")
            
            git_add_commit_push(repository_path, commit_msg, branch_name, add_option=add_option, amend=(amend_commit.lower() == 'yes'))
    
    elif option == '5':
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        branch_name = simpledialog.askstring("Branch Name", "Enter the branch name to pull changes from (default is master):") or 'master'
        subprocess.run(['git', 'pull', 'origin', branch_name], cwd=repository_path)
        print(f"Changes pulled from the remote repository into branch {branch_name}.")
    
    elif option == '6':
        repository_path = filedialog.askdirectory(title="Select Repository Directory")
        add_git_remote(repository_path)

root = tk.Tk()
root.title("GitCommanderHub")
intro_label = tk.Label(root, font=("Arial", 12))
intro_label.pack(padx=20, pady=20)
intro_button = tk.Button(root, text="Start", command=display_intro)
intro_button.pack(pady=10)

root.mainloop()
