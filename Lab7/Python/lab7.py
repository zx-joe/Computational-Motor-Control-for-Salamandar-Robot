""" Lab 7 """
from run_network import main as run_network
from parse_args import save_plots
import farms_pylog as pylog


def main():
    """Main function that runs all the exercises."""
    pylog.info('Running network')
    save = save_plots()
    run_network(plot=not save)


if __name__ == '__main__':
    main()

