# Blog de Peru HUG

Posts técnicos de la comunidad **HashiCorp User Group Perú**, publicados en
[peru-hug.com/blog](https://peru-hug.com/blog/).

Cualquier persona puede escribir: cada post es una carpeta con un archivo Markdown
y se propone con un Pull Request. Lee la [guía de contribución](CONTRIBUTING.md) para empezar.

## Estructura

```
posts/
  _plantilla/index.md            ← copia esta carpeta para empezar
  2026-11-mi-post/
    index.md                     ← tu post (frontmatter + Markdown)
    img/                         ← imágenes del post (opcional)
authors/
  tu-usuario-de-github.yml       ← tu ficha de autor
tags.yml                         ← etiquetas permitidas
scripts/validate.py              ← el mismo chequeo que corre en cada PR
```

## Cómo se publica

1. Abres un PR con tu post.
2. El workflow **Validar posts** revisa el formato.
3. El equipo de organizadores revisa el contenido y hace merge.
4. El sitio peru-hug.com genera la página del post y la publica en `/blog/`.

Este repo solo guarda contenido: el HTML se genera en el repositorio del sitio, que
escapa cualquier HTML del Markdown.
