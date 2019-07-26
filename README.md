# Validators analysis

## Crawler

Make sure you run local redis instance before start. To receive blocks from cyberd node, use the following commands:

```bash
# This one will add recurrent tast to a task queue
$ python ./parallel_scraper.py

# This will execute tasks in queue
$ celery -A parallel_scraper worker
```

If you've done everything correctly, you'll get a non-empty file ./euler_validators_original.csv

## Counters and visualizations

```
TODO
```