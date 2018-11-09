# Worker Development Guide

This guide may help to create your own **Processor**. 

Let's start with basics.

Terms:

  * Processor - Base Structure which stores information about **Worker** and provides helpers
  * Worker - Instantiated **Processor** which `Processes` Data
  * Data - It can be anything which can be described or implemented by JSON Schema

## Processor

The **Processor** is a Structure which stores data about **Worker**. It's Structure looks like this:

```python
class Processor(models.Model):
    id = models...
    name = models...
    image = models...
    description = models...
    schema = JSONField...
    ui_schema = JSONField..
```

Backend Specific:
  * `id` - Slug Unique Identifier
  * `schema` - Processor's **Input**, **Output**, **Input Config** and **Output Config**

Frontend Specific:
  * `name`
  * `description`
  * `image` passes to frontend. It contains link or base64 encoded image to be shown
  * `ui_schema` used to pass cosmetic changes for a **Frontend** consumers to apply custom rules

### Schema

Let's say a few words about *Schema*. 

Required:
  * **Input** - root property `in`
  * **Output** - root property `out`

Optional:
  * **Input Config** - root property `in_config`
  * **Output Config** - root property `out_config`

Check Workers inside of this Directory to see how it's done :)


## Processing

The only purpose of this Project is **Processing**. 

The Processing Pipeline called ... **Pipeline** :D

When you trigger the Processing each of worker triggers one by one and passes data from one hands to another.

### Example

Pipeline: **random**, **md5**, **web_hook**

This is how it works:
  * You trigger the processing of a pipeline
  * **random** generates a value according it's **Input Config**
    * **random** produces a task for next worker named **md5**
  * **md5** receives input and generates a value
    * **md5** produces a task for next worker named **web_hook**
  * **web_hook** receives input and makes an HTTP Request accoring it's **Input Config**
    * **web_hook** produces a task for next worker 
  * Task Consumer fetches a task **without worker which should receive it** - this is a **Result** of a Pipe

That's all :)