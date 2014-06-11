# weboven Nucleum

django base package


## requirements


## task list
* css для PreviewImageField
* пересмотреть upload_handlers генерировать хеш сумму для новых файлов
* совместимость с python 3
* избавиться от регулярных выражений в get_abolute_url
* организовать property для hрost_name, namespace, url_name, reverse_args вместо вычисления каждый раз.


# release history
### 0.3.alfa.3
* UrlPatterns - поправлено регулярное выражение, теперь не выдаёт ошибки при имени файла отличающегося от urls.py
* PreviewImageField вынеселена в fields
* get_abolute_url вынесена в mixin
* поправлены регулярные выражения в get_absolute_url
* get_abolute_url взаимодействует с django_host
* PEP-0008
