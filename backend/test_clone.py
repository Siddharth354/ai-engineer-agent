from app.services.git_service import GitService

service = GitService()

path = service.clone_repository(
    "https://github.com/octocat/Hello-World.git"
)

print(path)