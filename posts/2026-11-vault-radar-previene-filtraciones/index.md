---
title: "Cómo Vault Radar previene filtraciones antes de que ocurran"
date: 2026-11-19
author: 8infinitecloud
summary: "Toyota, Codecov y CircleCI tienen algo en común: un secreto expuesto. Repasamos esos casos y cómo HCP Vault Radar detecta credenciales filtradas antes de que lleguen a producción."
tags: [vault, hcp, seguridad, devops]
---

Una contraseña en un archivo de configuración, un token pegado en un script de CI o una llave SSH olvidada en un commit: así empiezan muchas de las filtraciones más costosas. Este post resume mi charla en Peru HUG sobre **HCP Vault Radar** y cómo ayuda a pasar de reaccionar a prevenir.

📑 **Presentación completa:** [Cómo Vault Radar previene filtraciones antes de que ocurran](https://drive.google.com/file/d/1BUxVsU_YVkpAy6mRgW4Q658F09rOykVT/view)

## Tres filtraciones que empezaron con un secreto expuesto

### Toyota (2022): una credencial olvidada durante cinco años

El código fuente de un servicio para clientes quedó publicado en un repositorio público de GitHub con una clave de acceso a un servidor de datos dentro. Estuvo ahí casi cinco años, de 2017 a 2022, y expuso datos de cerca de 300 mil clientes. Nadie lo notó porque nadie estaba buscando.

### Codecov (2021): un script alterado en CI/CD

Los atacantes modificaron el script que miles de pipelines descargaban para subir reportes de cobertura. La versión alterada enviaba a un servidor externo todas las variables de entorno del pipeline, incluidos tokens y credenciales de cientos de empresas. El problema de fondo: los secretos vivían como variables de entorno al alcance de cualquier script.

### CircleCI (2023): un token robado

Un malware en la laptop de un empleado robó un token de sesión válido. Con él, los atacantes entraron a sistemas internos y extrajeron secretos de clientes: variables de entorno, tokens y llaves. Miles de organizaciones tuvieron que rotar sus credenciales.

**La lección común:** los secretos terminan donde no deberían (código, configuración, pipelines) y casi nunca alguien lo detecta a tiempo.

## Qué es HCP Vault Radar

HCP Vault Radar es la solución de HashiCorp para **descubrir y reducir el riesgo de secretos expuestos** en una organización. Busca credenciales, claves de API y contraseñas en código fuente, repositorios, configuraciones y pipelines de CI/CD.

- **Descubre secretos no gestionados**, con más de 300 algoritmos de detección en plataformas de control de versiones compatibles con Git.
- **Escanea múltiples fuentes**: GitHub, GitLab, Bitbucket, Jira y Confluence.
- **Guía la remediación**, con pasos específicos según el tipo de secreto encontrado.
- **Asegura lo que encuentra**: los secretos detectados se pueden mover a Vault para gestionarlos de forma centralizada.

## Dónde actúa: antes de que el secreto llegue a producción

La clave es **dónde** se hace el escaneo. Vault Radar puede revisar cada **commit**, cada **branch** y cada **pull request**, para que un secreto se detecte en la revisión de código y no meses después en un incidente.

Además del escaneo, Vault Radar:

- **Correlaciona** los hallazgos con Vault, para saber si un secreto filtrado ya está gestionado ahí.
- **Notifica** al equipo y se integra con herramientas de gestión de incidentes de seguridad.
- Usa un **agente** para escanear fuentes dentro de tu propia red.

## La demo: reproducir los casos en un repositorio

Para la charla armé un repositorio con vulnerabilidades **intencionales y ficticias** que imitan cada caso:

- `toyota-case/`: contraseñas de bases de datos en Python, Spring y archivos `.properties`, y una llave SSH privada.
- `codecov-case/`: el script de subida alterado y tokens de API escritos directamente en scripts y `package.json`.
- `circleci-case/`: secretos en `.circleci/config.yml` y un `.env` subido al repositorio.
- Más carpetas con secretos en Docker, Kubernetes y Terraform, datos personales (PII) y lenguaje no inclusivo, que Vault Radar también detecta.

Este es el tipo de configuración que Vault Radar marca como hallazgo:

```yaml
# .circleci/config.yml: credenciales escritas directamente en el pipeline
environment:
  AWS_ACCESS_KEY_ID: AKIAIOSFODNN7EXAMPLE
  DATABASE_URL: postgresql://admin:password123@db.example.com:5432/app
```

Para escanear una carpeta con el CLI de Vault Radar, después de configurar las credenciales de tu proyecto de HCP:

```bash
vault-radar scan folder -p ./circleci-case -o circleci.csv
```

El reporte lista cada secreto encontrado, el archivo donde está y su severidad. Revisa la [documentación del CLI](https://developer.hashicorp.com/hcp/docs/vault-radar/cli) para ver todas las fuentes que puede escanear.

## Cómo resolverlo

1. **Nunca escribas credenciales en el código** ni en archivos de configuración versionados.
2. **Centraliza los secretos en Vault** y entrégalos a las aplicaciones en tiempo de ejecución.
3. **Escanea en cada commit y pull request** con Vault Radar, no solo en auditorías puntuales.
4. **Rota las credenciales** expuestas apenas se detectan y, mejor aún, usa credenciales dinámicas de corta duración.
5. **Revisa la integridad de los scripts de terceros** que corren en tus pipelines.

Un secreto detectado en un pull request es un comentario de revisión. El mismo secreto detectado en producción es un incidente. ¿Tienes preguntas sobre Vault Radar? Escríbenos en el grupo de WhatsApp de la comunidad.
