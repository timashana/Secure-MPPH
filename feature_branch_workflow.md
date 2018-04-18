# Git Feature Branch Workflow 
  - More information here: [Git Feature Branch Workflow | Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)

  - Start with the master branch:

      ```
      git checkout master
      git fetch origin 
      git reset --hard origin/master
      ```

      This switches the repo to the master branch, pulls the latest commits and resets the repo's local copy of master to match the latest version.

  - Create a new branch:
      Use a separate branch for each feature or issue you work on. 

      ```
      git checkout -b new-feature
      ```

      This checks out a branch called new-feature based on master, and the -b flag tells Git to create the branch if it doesn’t already exist.

  - Update, add, commit, and push changes
      Work on the feature and make commits like you would any time you use Git

      ```
      git status
      git add <some-file>
      git commit -m "your message here"
      ```

      ​

  - Push feature branch to remote
      It’s a good idea to push the feature branch up to the central repository. This serves as a convenient backup, when collaborating with other developers, this would give them access to view commits to the new branch.

      ```
      git push -u origin new-feature
      ```

      his command pushes new-feature to the central repository (origin), and the -u flag adds it as a remote tracking branch

  - Resolve feedback
      comment and aprove the pushed commits

  - Merge pull request
      Before you merge, you may have to resolve merge conflicts if others have made changes to the repo. When your pull request is approved and conflict-free, you can add your code to the master branch.