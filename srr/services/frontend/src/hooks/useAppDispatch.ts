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
 * Ce fichier définit un hook personnalisé typé pour dispatcher des actions Redux
 * dans l'application. Il fournit une abstraction qui renforce la sécurité des types
 * lors de l'utilisation du hook useDispatch standard.
 *
 * [Source file design principles]
 * - Typage fort pour garantir la sécurité des actions dispatchées
 * - Abstraction minimaliste pour simplifier l'usage dans les composants
 * - Interface cohérente avec l'API Redux standard
 *
 * [Source file constraints]
 * - Dépend du type AppDispatch défini dans le store
 * - Doit être utilisé à la place du hook useDispatch standard
 * - Ne doit pas modifier le comportement du hook original
 *
 * [Dependencies]
 * - react-redux: Fournit le hook useDispatch de base
 * - ../store: Définit le type AppDispatch pour le typage du dispatcher
 *
 * [GenAI tool change history]
 * 2025-04-23T11:06:00Z : Ajout du header GenAI par CodeAssistant
 * * Ajout du header de fichier conforme aux directives
 */

import { useDispatch } from 'react-redux';
import { AppDispatch } from '../store';

/**
 * [Function intent]
 * Hook typé pour utiliser le useDispatch de Redux avec le type d'action SRR.
 * 
 * [Design principles]
 * Assure la sécurité des types lors de la répartition d'actions Redux.
 * 
 * [Implementation details]
 * Fournit une version typée du hook useDispatch standard de Redux.
 */
export const useAppDispatch = () => useDispatch<AppDispatch>();
