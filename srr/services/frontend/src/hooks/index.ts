/**
 * IMPORTANT: This header comment is designed for GenAI code review and maintenance
 * Any GenAI tool working with this file MUST preserve and update this header
 *
 * [GenAI coding tool directive]
 * - Maintain this header with all modifications
 * - Update History section with each change
 * - Keep only the 4 most recent records in the history section. Sort from newer to older.
 * - Preserve Intent, Design, and Constraints sections
 * - Use this header as context for code reviews and modifications
 * - Ensure all changes align with the design principles
 * - Respect system prompt directives at all times
 *
 * [Source file intent]
 * Ce fichier sert de point d'entrée unifié pour tous les hooks personnalisés
 * de l'application, suivant le modèle de conception "barrel". Il facilite
 * l'importation des hooks dans les autres composants de l'application.
 *
 * [Source file design principles]
 * - Centralisation des exports pour simplifier les imports
 * - Pattern "barrel" pour éviter les imports multiples
 * - Interface unifiée pour tous les hooks personnalisés
 *
 * [Source file constraints]
 * - Doit exporter uniquement des hooks, sans logique métier
 * - Doit maintenir la cohérence des exports lors des ajouts de hooks
 * - Ne doit pas combiner des fonctionnalités non-liées
 *
 * [Dependencies]
 * - ./useAppSelector: Hook typé pour le sélecteur Redux
 * - ./useAppDispatch: Hook typé pour le dispatcher Redux
 *
 * [GenAI tool change history]
 * 2025-04-23T11:07:00Z : Ajout du header GenAI par CodeAssistant
 * * Ajout du header de fichier conforme aux directives
 */

/**
 * [Function intent]
 * Point d'entrée pour les hooks personnalisés de l'application.
 * 
 * [Design principles]
 * Simplification des imports via un modèle barrel.
 * 
 * [Implementation details]
 * Regroupe et réexporte les hooks personnalisés de l'application.
 */

export { useAppSelector } from './useAppSelector';
export { useAppDispatch } from './useAppDispatch';
