import { readable, writable } from "svelte/store";
import {io} from "./socketConnection";

/**
 * Store event successfull message
 */
export const eventOk = readable('OK');
/**
 * Store event not successfull message
 */
export const eventNotOK = readable('NOK');
/**
 * Store result image of elaboration
 */
export const resultElaborationImg = writable("");
/**
 * Store result mesh of elaboration
 */
export const resultElaborationMesh = writable("");
/**
 * Store mesh name of elaboration
 */
export const meshName = writable("");
/**
 * Store history selected index
 */
export const selectedIndexHistory = writable<undefined | number>(undefined);
/**
 * Store Socket.IO connection
 */
export const ioStore = readable(io);