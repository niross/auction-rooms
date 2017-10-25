from fabric.api import runs_once, lcd, local, task


@task
@runs_once
def register_deployment(git_path):
    with(lcd(git_path)):
        revision = local('git log -n 1 --pretty="format:%H"', capture=True)
        branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
        local(
            'curl https://intake.opbeat.com/api/v1/organizations'
            '/a8c27beba6ef4c09aa8340432aa690ff/apps/9a18256ec2/releases/'
            ' -H "Authorization: Bearer '
            '1df6a84d68212cc7500ac7fbc4ceac641295e2e7"'
            ' -d rev="{}"'
            ' -d branch="{}"'
            ' -d status=completed'.format(revision, branch))
