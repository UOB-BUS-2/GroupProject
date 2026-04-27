git fetch --all --prune

git log origin/main \
  --date=iso \
  --pretty=format:"============================================================%nCommit: %H%nAuthor: %an <%ae>%nAuthor date: %ad%nCommitter: %cn <%ce>%nCommitter date: %cd%n%nMessage:%n%B%nChanged project files:" \
  --numstat \
  -- . \
  ':(exclude).idea/**' \
  ':(exclude)**/__pycache__/**' \
  ':(exclude)**/*.pyc' \
  ':(exclude)app.db' \
  > git_commit_log.txt