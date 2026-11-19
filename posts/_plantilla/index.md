---
title: "Título de tu post (máximo 100 caracteres)"
date: 2026-11-20
author: tu-usuario-de-github
summary: "Una o dos frases que expliquen de qué trata el post. Aparece en el índice del blog (máximo 220 caracteres)."
tags: [terraform]
# cover: img/portada.png   # opcional: imagen de portada dentro de img/
# repo: https://github.com/tu-usuario/tu-repo   # opcional: repo público con el código del post
# slides: https://drive.google.com/...          # opcional: presentación (Drive, Slides, Speaker Deck o SlideShare)
# draft: true              # opcional: true para que el post no se publique todavía
---

Escribe una introducción corta: qué problema resuelves y qué va a aprender quien lee.

## Contexto

Usa títulos de nivel 2 (`##`) y 3 (`###`). No uses `#`: el título del post sale de `title`.

## Paso a paso

Explica con ejemplos de código:

```hcl
resource "aws_s3_bucket" "ejemplo" {
  bucket = "mi-bucket-de-ejemplo"
}
```

Para agregar una imagen, guárdala en la carpeta `img/` de tu post:

![Diagrama de la arquitectura](img/diagrama.png)

## Conclusiones

Cierra con lo más importante y, si quieres, enlaces a la documentación oficial.
