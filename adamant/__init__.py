import datetime
import os
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta


class Adamant:
    def __init__(self,
                 base_url='https://github.com',
                 owner='openstack',
                 repo='nova',
                 branch='master'):

        self.repo_name = repo
        self.repository_url = f'{base_url}/{owner}/{repo}'
        self.local_repos_dir_path = './.repos'
        self.repo_branch = branch
        self.root_dir = Path().resolve()

        if self._is_cloned():
            self._set_repo_root_directory()
            self._pull_update()
        else:
            self._clone_repo()

    def _is_cloned(self):
        return Path(
            f'{self.local_repos_dir_path}/{self.repo_name}'
        ).exists()

    def _set_repo_root_directory(self):
        os.chdir(f'{self.local_repos_dir_path}/{self.repo_name}')

    @staticmethod
    def _pull_update():
        subprocess.check_call(['git', 'fetch', '--all'])
        subprocess.check_call(['git', 'pull'])

    def _clone_repo(self):
        subprocess.check_call(
            ['git', 'clone', self.repository_url,
             f'{self.local_repos_dir_path}/{self.repo_name}']
        )

    @staticmethod
    def get_present_and_past_date(year=0, month=0, day=0):
        date = datetime.datetime.now()
        proc_dt = datetime.date(date.year, date.month, date.day)
        past_date = proc_dt + relativedelta(years=-year,
                                            months=-month,
                                            days=-day)
        return str(proc_dt), str(past_date)

    def most_active_modules_by_commits_in_directory_from_last_six_months(
            self,
            directory_name='.'
    ):

        os.chdir(f'{directory_name}')
        directories_in_curdir = \
            list(filter(os.path.isdir, os.listdir(os.curdir)))

        present_date, past_date = self.get_present_and_past_date(month=6)

        commits = dict()

        for directory in directories_in_curdir:
            commit_count_string = subprocess.check_output(
                f"git log --oneline --follow --after='{past_date} 00:00' "
                f"--before='{present_date} 23:59' -- {directory} | wc -l",
                shell=True
            ).decode().strip()

            commits[directory] = int(commit_count_string)

        sorted_commits = sorted(commits.items(),
                                key=lambda kv: (kv[1], kv[0]), reverse=True)

        twelve_most_active_modules = sorted_commits[:12]

        x_axis = []
        y_axis = []

        for x, y in twelve_most_active_modules:
            x_axis.append(x)
            y_axis.append(y)

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(x_axis, y_axis)
        ax.set_title(
            f'Number of Commits for each {directory_name}/ subdirectory'
        )
        plt.xlabel("Modules")
        plt.ylabel("Number of Commits")
        plt.xticks(rotation=45)

        if not Path(f'{self.root_dir}/.images').exists():
            os.mkdir(f'{self.root_dir}/.images')

        fig.savefig(
            f'{self.root_dir}/.images/num_commits.png', bbox_inches='tight'
        )
