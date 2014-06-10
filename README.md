# weboven Nucleum

базовый пакет для проектов


## requirements


## task list
* css для PreviewImageField


## release history
### 0.3.alfa.3
* UrlPatterns поправлено регулярное выражение теперь неважно как назван файл содержащий urlpattern
* PreviewImageField вынеселена в fields
* get_abolute_url вынесена в миксин
* поправлены регулярные выражения в get_absolute_url
* get_abolute_url теперь проверяет установлен ли django_host и в случае чего, пытается получить адрес относительно хоста прописанного в модуле
* PEP-0008
