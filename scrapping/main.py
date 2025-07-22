import argparse
from typing import Optional
from pydantic import TypeAdapter
from schemas import BannerGroup, banner_groups_adapter

import scrapping

# допущение: фестивальные баннеры всегда одинаковые на японии и глобале
# при этом персонажи на разных баннерах не повторяются

# на глобале могут объединять несколько баннер-групп с японии, чтобы уменьшить отставание


# парсинг аргументов
parser = argparse.ArgumentParser()
parser.add_argument("--refetch", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument("--output", default="banners.json")

args = parser.parse_args()
refetch: bool = args.refetch
output_path: str = args.output

# загрузить информацию о баннерах
if refetch:
    banners_global = scrapping.scrap_global_banners()
    banners_japan = scrapping.scrap_japan_banners()

    with open("banners_global.json", "wb") as f:
        f.write(banner_groups_adapter.dump_json(banners_global, indent=4))

    with open("banners_japan.json", "wb") as f:
        f.write(banner_groups_adapter.dump_json(banners_japan, indent=4))

else:
    with open("banners_global.json", encoding="utf-8") as f:
        banners_global = banner_groups_adapter.validate_json(f.read())

    with open("banners_japan.json", encoding="utf-8") as f:
        banners_japan = banner_groups_adapter.validate_json(f.read())


last_index = banners_global[-1].index

# получить ближайший предыдущий фестивальный баннер и аналогичный на японии
fest_banner_global = [banner for banner in banners_global if banner.index <= last_index and banner.is_fest][-1]
fest_banner_japan = next(banner for banner in banners_japan if banner.check_exact_characters(fest_banner_global))

# найти последние соответствующие баннеры на глобале и японии
after_fest_banners_global = [banner for banner in banners_global if banner.index > fest_banner_global.index and banner.index <= last_index]
after_fest_banners_japan = [banner for banner in banners_japan if banner.index > fest_banner_japan.index]

index_global = fest_banner_global.index
index_japan = fest_banner_japan.index

max_skip_global = 3
max_skip_japan = 3

first = True
while index_global <= last_index:
    matched : Optional[tuple[int, int]] = None # global, japan

    _index_global = index_global
    for i in range(max_skip_global):
        if first : first = False
        else : _index_global += 1
        
        if _index_global >= len(banners_global) or _index_global > last_index: break
        
        _index_japan = index_japan
        for j in range(max_skip_japan):
            if banners_global[_index_global].check_includes_characters(banners_japan[_index_japan]):
                matched = (_index_global, _index_japan)

            _index_japan += 1
            if _index_japan >= len(banners_japan): break

    if matched:
        index_global, index_japan = matched
    else: break

# предсказать последующие баннеры сдвигая их по времени
time_delta = banners_global[index_global].interval.start - banners_japan[index_japan].interval.start  # вычесть из последующий интервалов
upcomming_banners = banners_japan[index_japan + 1 :]

for i, banner in enumerate(upcomming_banners):
    banner.interval.start += time_delta
    banner.interval.end += time_delta
    banner.is_prediction = True
    banner.index = len(banners_global) + i

banner_history = banners_global + upcomming_banners

print("Next banner:", upcomming_banners[0].characters)

with open(output_path, "wb") as f:
    f.write(banner_groups_adapter.dump_json(banner_history, indent=1))
