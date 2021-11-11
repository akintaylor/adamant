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
        self.owd = os.getcwd()

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

    def _return_to_repo_root_dir(self):
        os.chdir(self.owd)
        self._set_repo_root_directory()

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

    @staticmethod
    def get_sub_dirs(directory_name):
        os.chdir(f'{directory_name}')
        dirs_in_curdir = list(filter(os.path.isdir, os.listdir(os.curdir)))

        return dirs_in_curdir

    def most_active_modules_by_commits_in_directory_from_last_six_months(
            self,
            directory_name='.'
    ):

        present_date, past_date = self.get_present_and_past_date(month=6)

        commits = dict()

        dirs_in_curdir = self.get_sub_dirs(directory_name)

        for directory in dirs_in_curdir:
            commit_count_string = subprocess.check_output(
                f"git log --oneline --follow --after='{past_date} 00:00' "
                f"--before='{present_date} 23:59' -- {directory} | wc -l",
                shell=True
            ).decode().strip()

            commits[directory] = int(commit_count_string)

        sorted_commits = sorted(commits.items(),
                                key=lambda kv: (kv[1], kv[0]), reverse=True)

        twelve_most_active_modules = sorted_commits[:12]

        x_axis, y_axis = [], []

        for x, y in twelve_most_active_modules:
            x_axis.append(x)
            y_axis.append(y)

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(x_axis, y_axis)
        ax.set_title(
            f'Fig. 1: A barchart showing the twelve most active modules by '
            f'commit in the {directory_name} directory for the last six '
            f'months.', fontdict={'fontsize': 12}, pad=10
        )
        plt.xlabel("Modules")
        plt.ylabel("Number of Commits")
        plt.xticks(rotation=45)

        if not Path(f'{self.root_dir}/.images').exists():
            os.mkdir(f'{self.root_dir}/.images')

        fig.savefig(
            f'{self.root_dir}/.images/{self.repo_name}_num_commits.jpeg',
            bbox_inches='tight'
        )

        self._return_to_repo_root_dir()

    def most_active_modules_by_churn_in_directory_from_last_six_months(
            self,
            directory_name='.'
    ):

        present_date, past_date = self.get_present_and_past_date(month=6)

        churns = dict()

        dirs_in_curdir = self.get_sub_dirs(directory_name)

        for directory in dirs_in_curdir:
            churn_count = subprocess.check_output(
                f"git log --numstat --format= \"$@\" "
                f"--follow --after='{past_date} 00:00' "
                f"--before='{present_date} 23:59' -- {directory} | awk "
                '\'{ins += $1}{del += $2} END{print ""ins","del""}\'',
                shell=True
            ).decode().strip()

            num_insert, num_delete = churn_count.split(',')

            if not num_insert:
                num_insert = 0

            if not num_delete:
                num_delete = 0

            churns[directory] = (int(num_insert), int(num_delete))

        sorted_churns = sorted(
            churns.items(),
            key=lambda kv: (kv[1][0] + kv[1][1], kv[0]),
            reverse=True
        )

        twelve_most_active_modules = sorted_churns[:12]

        labels, inserts, deletions = [], [], []

        for label, (num_inserts, num_deletions) in twelve_most_active_modules:
            labels.append(label)
            inserts.append(num_inserts)
            deletions.append(num_deletions)

        fig, ax = plt.subplots()

        plt.xticks(rotation=45)

        ax.bar(labels, inserts, bottom=deletions,
               label='Number of lines added', color='mediumseagreen')
        ax.bar(labels, deletions,
               label='Number of lines deleted', color='indianred')

        ax.set_ylabel('Churn')
        ax.set_title(f'Fig. 2: A barchart showing the twelve most active '
                     f'modules by *churn in the {directory_name} directory '
                     f'for the last six months.',
                     fontdict={'fontsize': 12}, pad=10)
        ax.legend()

        if not Path(f'{self.root_dir}/.images').exists():
            os.mkdir(f'{self.root_dir}/.images')

        fig.savefig(
            f'{self.root_dir}/.images/{self.repo_name}_churn_num.jpeg',
            bbox_inches='tight'
        )

        self._return_to_repo_root_dir()
