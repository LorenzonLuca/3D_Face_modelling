import { PUBLIC_BACKEND_URL } from "$env/static/public";
import ioClient from "socket.io-client";

/**
 * Socket.IO connection
 */
export const io = ioClient(PUBLIC_BACKEND_URL, { secure: false });