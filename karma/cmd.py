from argparse import ArgumentParser
import os
from karma.app import app, db
from karma.model.user import User
from karma.model.job import Job         # noqa: F401
from karma.model.award import Award     # noqa: F401


if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='action')
    subparsers.required = True
    subparsers.add_parser('init', help='Creates the database file '
                          'with all its defined tables.')
    subparsers.add_parser('delete-db', help='Removes the database file'
                          'with from disk.')
    user = subparsers.add_parser('add-user', help='Removes the database file'
                                 'with from disk.')
    user.add_argument('username')
    user.add_argument('password')
    user.add_argument('--admin', action='store_true')

    args = parser.parse_args()

    if args.action == 'init':
        with app.app_context():
            db.create_all()
    if args.action == 'delete-db':
        db_file = 'karma/karma.db'
        if os.path.exists(db_file):
            os.remove(db_file)
    if args.action == 'add-user':
        print(f'Adding {args.username} as admin={args.admin}')
        with app.app_context():
            with db:
                user = User(args.username, args.password, args.admin)
                db.add(user)
