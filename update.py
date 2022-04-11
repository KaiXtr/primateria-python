import git
import os

def print_repository(repo):
    print('Repo description: {}'.format(repo.description))
    print('Repo active branch is {}'.format(repo.active_branch))
    for remote in repo.remotes:
        print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
    print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))

def print_commit(commit):
    print('----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str(commit.authored_datetime))
    print(str("count: {} and size: {}".format(commit.count(),
                                              commit.size)))

repo = git.Repo.clone_from('https://github.com/KaiXtr/mutation-purge','./repository')
tree = repo.tree()
o = repo.remotes.origin
o.pull()

for i in tree:
	commit = repo.iter_commits(paths=i.path,max_count=1).next()
	print(commit.message)
	print(commit.comitter)
	print(i.path)
	print(commit.comitted_date)

'''if not repo.bare:  
    print_repository(repo)
    commits = list(repo.iter_commits('master'))[:3]
    for commit in commits:
        print_commit(commit)
        pass
else:
    print('Could not load repository :(')'''