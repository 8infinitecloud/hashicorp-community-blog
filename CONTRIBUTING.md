# Cómo escribir un post

¡Gracias por compartir lo que sabes con la comunidad! 🎉 Esta guía te lleva de la idea a la publicación.

## 1. Prepara tu post

1. Haz un **fork** de este repositorio y clónalo.
2. Copia `posts/_plantilla` a una carpeta nueva con el formato `AAAA-MM-titulo-en-minusculas`:

   ```bash
   cp -r posts/_plantilla posts/2026-12-mi-primer-modulo-terraform
   ```

3. Escribe tu post en `index.md`. Si usas imágenes, crea `img/` dentro de tu carpeta y guárdalas ahí.
4. Si es tu primer post, crea tu ficha en `authors/<tu-usuario-de-github>.yml`:

   ```yaml
   name: Tu Nombre
   role: DevOps Engineer en Tu Empresa
   github: tu-usuario-de-github
   linkedin: https://www.linkedin.com/in/tu-perfil   # opcional
   bio: Una frase sobre ti.                           # opcional, máximo 200 caracteres
   ```

## 2. Frontmatter

Cada `index.md` empieza con este bloque:

```yaml
---
title: "Título del post"                 # obligatorio, máximo 100 caracteres
date: 2026-12-03                         # obligatorio, AAAA-MM-DD; el mes debe coincidir con la carpeta
author: tu-usuario-de-github             # obligatorio, debe existir en authors/
summary: "De qué trata, en una o dos frases."   # obligatorio, máximo 220 caracteres
tags: [terraform, aws]                   # obligatorio, de 1 a 5, solo las de tags.yml
cover: img/portada.png                   # opcional
draft: true                              # opcional: no se publica mientras sea true
---
```

Un post con `date` en el futuro se publica automáticamente ese día.

## 3. Reglas de contenido

- **Solo Markdown.** No se permite HTML con scripts, iframes, estilos ni eventos. El sitio escapa todo el HTML de todas formas.
- **Títulos desde `##`.** El título principal sale de `title`.
- **Imágenes en `img/`**, en PNG, JPG, WebP o GIF (no SVG), de hasta 1 MB cada una y 5 MB por post. No enlaces imágenes externas.
- **Mínimo 300 caracteres** de contenido.
- **Contenido original** o con la fuente citada, en español, y respetando el
  [Código de Conducta](https://peru-hug.com/code-of-conduct.html).
- Nada de promoción comercial: puedes mencionar dónde trabajas, pero el post debe enseñar algo.
- No incluyas credenciales, tokens ni datos internos de tu empresa en los ejemplos.

## 4. Valida antes de abrir el PR

```bash
pip install pyyaml
python scripts/validate.py
```

Es el mismo chequeo que corre en el PR.

## 5. Abre el Pull Request

- Un post por PR. Solo modifica tu carpeta en `posts/` y tu ficha en `authors/`.
- Completa la plantilla del PR.
- El equipo de organizadores revisará el contenido y te dejará comentarios en el mismo PR.
- Cuando se haga merge, el post aparecerá en [peru-hug.com/blog](https://peru-hug.com/blog/) en unos minutos (como máximo al día siguiente).

¿Tienes una idea pero no sabes si encaja? Abre un issue con la plantilla **Propuesta de post** y lo conversamos.
