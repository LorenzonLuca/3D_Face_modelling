import type { LayoutServerLoad } from './$types';
import { PUBLIC_BACKEND_URL } from "$env/static/public";
import axios, { type AxiosRequestConfig } from 'axios';
import * as https from 'https'

export const load: LayoutServerLoad = async ({ cookies }) => {
    const token = cookies.get('token');

    if (token == undefined) {
        return { 'username': false, 'logged': false };
    }

    let url = PUBLIC_BACKEND_URL + '/api/user';
    let config: AxiosRequestConfig = {
        method: 'get',
        url: url,
        auth: {
            username: token,
            password: 'unused'
        },
        httpsAgent: new https.Agent({
            rejectUnauthorized: false
        })
    }

    const username = await axios(config)
        .then((res) => {
            return res.data.username;
        })
        .catch((err) => {
            return false;
        })


    if (!username) {
        return { 'username': false };
    }

    const urlHistory = PUBLIC_BACKEND_URL + '/api/history';
    let configHistory: AxiosRequestConfig = {
        method: 'get',
        url: urlHistory,
        auth: {
            username: token,
            password: 'unused'
        },
        httpsAgent: new https.Agent({
            rejectUnauthorized: false
        })
    }

    const history = await axios(configHistory)
        .then((res) => {
            return res.data.history;
        })
        .catch((err) => {
            return false;
        })

    if (!history) {
        return { 'username': username, 'history': [], 'logged': true, 'token': token };
    }
    return { 'username': username, 'history': history, 'logged': true, 'token': token };
}