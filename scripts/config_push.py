from nornir import InitNornir
from nornir.core.deserializer.inventory import Inventory
from nornir.core.filter import F
from nornir.plugins.tasks import text
from nornir.plugins.tasks import files
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking
import napalm
import pprint

def deploy_configs(task):
    f = open(f"config/{task.host}.conf", 'rt')
    configuration = f.read()
    f.close()

    multi_result = task.run(
        task=networking.napalm_configure,
        configuration=configuration,
        dry_run=True,
        replace=False
    )

    # print_result(multi_result)


#nr = InitNornir(
#    core={"num_workers": 20},
#    logging={"enabled": True, "level": "DEBUG", "to_console": True}
#)
nr = InitNornir(
    core={"num_workers": 20},
    logging={"enabled": True, "level": "DEBUG", "to_console": True},
    config_file="./config.yaml"
)
#nr = nr.filter(platform="ios")
#nr = nr.filter((F(site="dc-1") | F(site="campus-core")) & ~F(role="oob-management"))
nr = nr.filter((F(site="dc-1")) & ~F(role="oob-management"))
pprint.pprint(Inventory.serialize(nr.inventory).dict())

agg_result=nr.run(
    task=deploy_configs,
    num_workers=1
)

print_result(agg_result)
