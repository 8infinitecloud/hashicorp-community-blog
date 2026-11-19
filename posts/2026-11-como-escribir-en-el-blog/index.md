---
title: "Cómo escribir en el blog de Peru HUG"
date: 2026-11-19
author: 8infinitecloud
summary: "El blog de la comunidad está abierto: cualquier persona puede proponer un post con un Pull Request. Te contamos cómo funciona, de la idea a la publicación."
tags: [comunidad]
---

El blog de HashiCorp User Group Perú es de la comunidad: lo escriben las personas que usan Terraform, Vault, Consul y el resto del ecosistema en su día a día. Si resolviste un problema, armaste un laboratorio o aprendiste algo que a otros les ahorraría horas, este es el lugar para contarlo.

## Cómo funciona

Todo el contenido vive en un repositorio público de GitHub, [hashicorp-community-blog](https://github.com/8infinitecloud/hashicorp-community-blog). Cada post es una carpeta con un archivo Markdown, y se propone con un Pull Request:

1. Haz un fork del repositorio.
2. Copia la carpeta `posts/_plantilla` con el nombre `AAAA-MM-titulo-de-tu-post`.
3. Escribe tu post en `index.md` y guarda tus imágenes en `img/`.
4. Si es tu primer post, agrega tu ficha de autor en `authors/tu-usuario.yml`.
5. Abre el Pull Request.

Un chequeo automático revisa el formato en cada PR: que el frontmatter esté completo, que tu ficha de autor exista, que las imágenes estén en el lugar correcto y no pesen demasiado. Si algo falla, el mensaje te dice qué corregir.

## Revisión y publicación

Alguien del equipo de organizadores lee tu post y te deja comentarios en el mismo PR. Revisamos que el contenido sea técnicamente correcto, que respete el [Código de Conducta](https://peru-hug.com/code-of-conduct.html) y que se entienda bien.

Cuando el PR se aprueba y se integra, nosotros nos encargamos del resto:

- Publicamos tu post en [peru-hug.com/blog](https://peru-hug.com/blog/), con el estilo del sitio, tu nombre, tu rol y enlaces a tus perfiles.
- Lo compartimos en la [página de LinkedIn de Peru HUG](https://www.linkedin.com/company/peru-hashicorp-user-group/), mencionándote, para que llegue a toda la comunidad.

## Ideas para tu primer post

- Un módulo de Terraform que reutilizas en todos tus proyectos y por qué.
- Cómo migraste secretos de variables de entorno a Vault.
- Lo que aprendiste preparando la certificación Terraform Associate.
- El resumen de una charla de nuestros meetups, con tus propias notas.

No hace falta que sea largo ni perfecto: un buen ejemplo práctico vale más que un texto extenso. ¡Te esperamos!
