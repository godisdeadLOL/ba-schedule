# ba-schedule

**BA Schedule** — инструмент для отображения списка баннеров _Blue Archive Global_ с прогнозами будущих баннеров на основе истории японской версии.

---

## 📊 Статус

[![Deploy](https://github.com/godisdeadLOL/ba-schedule/actions/workflows/main.yaml/badge.svg?branch=upload&event=push)](https://github.com/godisdeadLOL/ba-schedule/actions/workflows/main.yaml)
[![pages-build-deployment](https://github.com/godisdeadLOL/ba-schedule/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/godisdeadLOL/ba-schedule/actions/workflows/pages/pages-build-deployment)

## 🌐 Онлайн-версия

🔗 [Открыть страницу](https://godisdeadlol.github.io/ba-schedule/)

## 🔍 Как работает

- Данные обновляются автоматически по расписанию с помощью задачи **cron**.
- Алгоритм:
  - Находит последний совпадающий баннер между **JP** и **Global**.
  - Строит прогноз, добавляя последующие JP-баннеры с учётом разницы во времени.
- Результат — **ориентировочный график будущих баннеров Global**.

## ⚠️ Дисклеймер

Предсказания основаны на истории JP и не гарантируют точного совпадения. Разработчики могут менять порядок баннеров.
