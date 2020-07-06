from locust.env import Environment
from performance.scenarios.scenario_organization_load import CustomerReadUser
from locust.stats import stats_printer, print_stats
import gevent
import logging
import sys
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
root = logging.getLogger()
root.setLevel(logging.WARNING)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


if __name__ == "__main__":
    env = Environment(user_classes=[CustomerReadUser],
                      host="http://api.owlvey.com:48100",
                      parsed_options="--skip-log-setup")
    env.create_local_runner()
    env.create_web_ui("127.0.0.1", 9090)
    gevent.spawn(stats_printer(env.stats))
    env.runner.start(10, hatch_rate=2)
    gevent.spawn_later(30, lambda: env.runner.quit())
    print_stats(env.stats)
    env.runner.greenlet.join()
    env.web_ui.stop()


