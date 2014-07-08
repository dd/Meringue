# weboven Nucleum

django base package


## requirements


## task list
* css для PreviewImageField
* пересмотреть upload_handlers генерировать хеш сумму для новых файлов
* совместимость с python 3
* thumbnail:
  * watermark
  * определение лица и использование в роли центра изображения
  * указание максимальной ширины или высоты
* PreviewImageFileInput:
  * check - предустанавливаемый размер
  * информация о изображении
  * изображение при инициализации
  * при загрузке изображения сразу же его выводить в превью (js)
* PublishModel:
  * поле mtime
* Абстрактная модель для создания галлереи со всеми необходимыми полями, кроме родительской таблицы


## release history
### 0.3.alfa.5
* немного продокументирован код
* почистен код и приведён в порядок
* продолжаются экперименты с версиями

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
