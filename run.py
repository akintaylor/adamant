from adamant import Adamant

if __name__ == '__main__':
    nova = Adamant()

    nova.most_active_modules_by_commits_in_directory_from_last_six_months(
        'nova'
    )
