# weboven Nucleum

django base package


## requirements


## task list
* css для PreviewImageField
* пересмотреть upload_handlers генерировать хеш сумму для новых файлов
* совместимость с python 3


## release history
### 0.3.alfa.4
* параметры namespace и url_name объеденены в view
* получение view и args для функции реверса вынесено в инициализацию класса
* избавились от регулярных выражений в GetAbsoluteUrlMixin
* продокументировал GetAbsoluteUrlMixin
* исправил GetAbsoluteUrlMixin при работе с django_hosts

### 0.3.alfa.3
* UrlPatterns - поправлено регулярное выражение, теперь не выдаёт ошибки при имени файла отличающегося от urls.py
* PreviewImageField вынеселена в fields
* get_abolute_url вынесена в mixin
* поправлены регулярные выражения в GetAbsoluteUrlMixin
* get_abolute_url взаимодействует с django_host
* PEP-0008
