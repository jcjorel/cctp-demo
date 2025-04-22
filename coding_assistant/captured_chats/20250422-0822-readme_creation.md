# Conversation Capture: README Creation

Cette conversation concerne la création du README.md pour le projet de système de réservation de ressources.

## Contexte

La conversation porte sur la création d'un README.md qui décrit:
- L'objectif du projet (implémentation d'un système de réservation de ressources basé sur un CCTP)
- La démarche de programmation basée sur la documentation et l'approche HST
- Les branches Git structurant le projet
- Les étapes d'implémentation prévues

## Conversation

```yaml
USER:
Lit le PDF.

Crée un <project_root>/README.md indiquant:
1/ Indiquant ce projet contient une implémentation pas à pas de l'objet du PDF à des fins de démonstrations de la programmation basée sur la documentation en utilisant l'outil Cline (https://github.com/cline/cline) et le LLM (TODO: Inclure définition de LLM) Anthropic Claude 3.7 Sonnet sur Amazon BedRock (https://aws.amazon.com/fr/bedrock/claude/ )
2/ Donne un définition de la programmation basée sur la documentation et du HST. Indiques que le system prompt de Cline doit être chargé avec le contenu de ce lien (https://github.com/jcjorel/cline-best-practices/blob/master/DOCUMENT_BASED_PROGRAMMING_SYSTEM_PROMPT.md )
3/ Indique que ce fichier README contiendra des liens vers des conversations capturées pour chaque étape
4/ Indique que chaque étape fera l'objet d'une branche Git spécifique pour permettre de naviguer facilement dans la temporalité de l'implémentaton du project
5/ Insère, avant la description de chaque étape un diagramme mermaid de la structure des branches du dépot Git
```

```yaml
ASSISTANT:
Je vais lire le PDF pour comprendre de quoi il s'agit avant de créer le fichier README.md.

[Lecture du fichier PDF]
```

```yaml
USER:
[Contenu du PDF fourni: CCTP pour un système de réservation de ressources]
```

```yaml
ASSISTANT:
J'ai créé le README.md selon les demandes avec:

1. Une introduction expliquant que le projet est une implémentation du système de réservation de ressources décrit dans le CCTP
2. Une définition de la programmation basée sur la documentation et de l'approche HST avec le lien vers le system prompt
3. Une section indiquant que des conversations seront capturées pour chaque étape
4. Une explication sur l'utilisation de branches Git spécifiques
5. Un diagramme mermaid montrant la structure des branches
6. Une structure pour les étapes d'implémentation avec des espaces pour les futurs liens
```

```yaml
USER:
[Confirmation que le fichier README.md a été bien créé]
```

```yaml
USER:
Capture our chat
```

```yaml
ASSISTANT:
[Création d'un fichier de capture de conversation dans coding_assistant/captured_chats/]
```

```yaml
USER:
Indique dans le README.md que Cline est épaulé par les serveurs décrits dans l'image et sont donc un prérequis. Donnes une rapide description des serveurs MCP concernés:

[Image montrant les serveurs MCP: perplexity-mcp, Core Server, awslabs.cdk-mcp-server, awslabs.cost-analysis-mcp-server, awslabs.aws-documentation-mcp-server, FireCrawl]
```

```yaml
ASSISTANT:
[Proposition de modification du README.md avec ajout d'une section sur les serveurs MCP]
```

```yaml
USER:
Indique aussi que tous les serveurs MCP ont été installé depuis la marketplace Cline sauf pour perplexity-mcp qui l'a été depuis https://github.com/jsonallen/perplexity-mcp
```

```yaml
ASSISTANT:
[Mise à jour du README.md avec l'information sur l'installation des serveurs MCP depuis la marketplace Cline et perplexity-mcp depuis GitHub]
```

## Résultat

Un README.md a été créé avec succès, contenant les informations demandées sur le projet de système de réservation de ressources. Le fichier inclut une introduction, des définitions, un diagramme mermaid des branches Git, et une structure pour documenter les étapes d'implémentation.

End of chat capture
