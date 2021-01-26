from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get

#norn = InitNornir()
norn = InitNornir(
    core={"num_workers": 20},
    logging={"enabled": True, "level": "DEBUG", "to_console": True},
    config_file="./config.yaml"
)
#norn = norn.filter(platform="ios")
norn = norn.filter((F(site="campus-building-1") | F(site="dc-1") | F(site="campus-core")) & ~F(role="oob-management"))
#norn = norn.filter((F(site="dc-11")) & ~F(role="oob-management"))

#import ipdb; ipdb.set_trace()

results = norn.run(task=napalm_get, getters=["config"], retrieve="all")

for k, v in results.items():
    if v[0].failed:
        print(f"host {k} napalm_get failed: {v[0].exception}")
    else:
        f = open(f"backup_config/{k}.conf", 'wt')
        f.write(v[0].result['config']['running'])
        f.close()
