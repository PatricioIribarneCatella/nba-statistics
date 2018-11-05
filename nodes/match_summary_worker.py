import sys
import json
import argparse
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from workers.matches_summary import MatchSummaryWorker

def main(reducers, config):

    with open(config) as f:
        config_data = json.load(f)

    worker = MatchSummaryWorker(reducers, config_data)

    worker.run()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                    description='Matches summary worker NBA',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
            '--config',
            help='The Net Topology configuration file'
    )
    parser.add_argument(
            '--reducers',
            type=int,
            default=1,
            help='How many reducers are working'
    )
    args = parser.parse_args()

    main(args.reducers, args.config)

