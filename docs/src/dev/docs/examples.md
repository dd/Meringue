# Examples of blocks for writing documentation

Коллекция примеров неочевидных блоков которые можно использовать при написании документации.


## Admonitions

[docs 1](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown/#admonition) [docs 2](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)

!!! note

    You should note that the title will be automatically capitalized.

=== ":octicons-arrow-right-16: inline end"

    !!! info inline end "Lorem ipsum"

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et
        euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo
        purus auctor massa, nec semper lorem quam in massa.

    ``` markdown
    !!! info inline end "Lorem ipsum"

        Lorem ipsum dolor sit amet, consectetur
        adipiscing elit. Nulla et euismod nulla.
        Curabitur feugiat, tortor non consequat
        finibus, justo purus auctor massa, nec
        semper lorem quam in massa.
    ```

    Use `inline end` to align to the right (left for rtl languages).

=== ":octicons-arrow-left-16: inline"

    !!! info inline "Lorem ipsum"

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et
        euismod nulla. Curabitur feugiat, tortor non consequat finibus, justo
        purus auctor massa, nec semper lorem quam in massa.

    ``` markdown
    !!! info inline "Lorem ipsum"

        Lorem ipsum dolor sit amet, consectetur
        adipiscing elit. Nulla et euismod nulla.
        Curabitur feugiat, tortor non consequat
        finibus, justo purus auctor massa, nec
        semper lorem quam in massa.
    ```

    Use `inline` to align to the left (right for rtl languages).


## Collapsible blocks

[docs](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#collapsible-blocks)

???+ note "Open styled details"

    ??? danger "Nested details!"
        And more content again.


## Footnotes

[docs](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown/#footnotes)

Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".


## Highlight

[docs](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown-extensions/#highlight)

```bash
git clone git@github.com:dd/Meringue.git
cd Meringue
ls -al
hatch run docs:serve

# This is bash
echo 1
```

### Inline

[docs](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown-extensions/#inlinehilite)

`#!bash python3 manage.py runserver`

`#!python3 import this`


### Annotates

[docs](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#adding-annotations)

```python
import this # (1)
```

1.  :fontawesome-brands-python: Simple is better than complex.


## Diagrams

[docs](https://squidfunk.github.io/mkdocs-material/reference/diagrams/)

``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```


## Content tabs

[docs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/)

=== "Tab 1"
    Markdown **content**.

    Multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b


## Smart Symbols

[docs](https://facelessuser.github.io/pymdown-extensions/extensions/smartsymbols/)

(tm), +/-, 1/4, etc.


## Keys

[docs](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown-extensions/#keys)

++ctrl+alt+delete++


## Icons and Emojis

[docs](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/)

:fontawesome-brands-twitter:{ .twitter } :smile: :heart: :thumbsup:


## Tooltips

[docs](https://squidfunk.github.io/mkdocs-material/reference/tooltips/)

[Hover me](https://example.com "I'm a tooltip!")


## Lists

[docs](https://squidfunk.github.io/mkdocs-material/reference/lists/)

- [X] item 1
    * [X] item A
    * [ ] item B
        more text
        + [x] item a
        + [ ] item b
        + [x] item c
    * [X] item C
- [ ] item 2
- [ ] item 3


## Tables

[docs](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown/#tables)

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
