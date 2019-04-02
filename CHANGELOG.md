## Meringue changelog

### task list

* css для PreviewImageField
* thumbnail:

  - watermark
  - определение лица и использование в роли центра изображения
  - указание максимальной ширины или высоты
  - определение фокуса

* PreviewImageFileInput:

  - информация о изображении
  - изображение при инициализации
  - при загрузке изображения сразу же его выводить в превью (js)

* Абстрактная модель для создания галлереи со всеми необходимыми полями, кроме родительской таблицы
* тестирование
* настройки вроде DEBUG из админки
* перезагрузка сервера из админки
* put_js преобразовывать относительные пути
* тег add_attrs добавляющий всё чтопередано атрибутами тега


### release history


#### 0.4.1

* change lib structure
* add python 3 support
* change configurates and functional
* rename PublishModel -> PublishedBase


#### 0.3.5

* Issue #5 :: set verlib as required


#### 0.3.4

* some minor changes


#### 0.3.3

* put_css/put_js:

  - поправлена ссылка на .map
  - добавлен параметр MERINGUE_LOAD_MINI в settings указывающий загружать минифицированный файл или нет (default = DEBUG)


#### 0.3.1.alpha.4

* Шаблонные теги put_css/put_js возвращающие css/js инлайном с заменёнными путями
* weboven_base -> meringue_base
* шаблонный тег field_render выводит поля форм в заранее заданном виде
* шаблонный тег field_render_classes возвращающий список классов для поля
* исправил form_fieldsets теперь можно не указывать title
* исправил совмещение с новым django_hosts, старые не поддерживает
* декоратор anonymous_required пропускающий только неавторизованных пользователей
* переработана функция get_absolute_url подбита под новый формат django_hosts
* добавленна настройка MERINGUE_SITE_PORT указывающая порт для reverse
* пофиксил переименование в upload_handlers
* PublishModel mtime field
* PublishModel ctime field
* put_css/put_js:

  - по возможности выводит минифицированный файл
  - в min переделывает ссылку на .map
  - переработана внутренняя составляющая в отдельный класс


#### 0.3.1.alpha.3

* Поправили зависимости
* Переходим на джанго 1.7
* upload_handlers: md5 -> sha256
* unify_email: если передать пустое значение возвращает None
* unify_email: проверяет на должное содержание символа @
* поправил reset.css
* уменьшил reset.css и сохранил reset.min.css
* coontext_processor.base теперь возвращает и DEBUG
* Шаблонный тег put_reset


#### 0.3.1.alpha.2

* все принты заменены логированием
* добавлены функции унификации почтового адреса и телефонного номера
* изменена стандартная formset_factory для того что бы выставляла префикс на все формы набора включая управляющие
* form_fieldsets - при необходимости разбивает форму по группам (fieldset)


#### 0.3.1.alpha.1

* структура egg
* функция get_version


#### 0.3.0

* доведены до ума существующие возможности
* внесён в список PyPI


#### 0.3.alpha.6

* egg
* пересмотреть upload_handlers генерировать имя загружаемых файлов на основе хеш суммы файла
* PreviewImageFileInput:

  - предустанавливаемый размер


#### 0.3.alpha.5

* немного продокументирован код
* почищен код и приведён в порядок
* продолжаются экперименты с версиями


#### 0.3.alpha.4

* параметры namespace и url_name объеденены в view
* получение view и args для функции реверса вынесено в инициализацию класса
* избавились от регулярных выражений в GetAbsoluteUrlMixin
* продокументировал GetAbsoluteUrlMixin
* исправил GetAbsoluteUrlMixin при работе с django_hosts


#### 0.3.alpha.3

* UrlPatterns - поправлено регулярное выражение, теперь не выдаёт ошибки при имени файла отличающегося от urls.py
* PreviewImageField вынеселена в fields
* get_abolute_url вынесена в mixin
* поправлены регулярные выражения в GetAbsoluteUrlMixin
* get_abolute_url взаимодействует с django_host
* PEP-0008
