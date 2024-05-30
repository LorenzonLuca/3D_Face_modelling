import type { Actions } from './$types';
import { PUBLIC_BACKEND_URL } from "$env/static/public";
import axios, { type AxiosRequestConfig } from 'axios';
import { redirect } from '@sveltejs/kit';
import * as https from 'https'

export const actions: Actions = {
    default: async ({ cookies, request }) => {
        const data = await request.formData();
        const username = data.get('username')?.toString();
        const password = data.get('password')?.toString();

        if (username == undefined || password == undefined) {
            return { msg: 'Please fill all the fields' }
        }

        if (username === "" || password === "") {
            return { msg: 'Please fill all the fields' }
        }

        const url = PUBLIC_BACKEND_URL + '/api/login';
        const config: AxiosRequestConfig = {
            method: 'get',
            url: url,
            headers: { "Content-Type": "multipart/form-data" },
            auth: {
                username: username,
                password: password
            },
            httpsAgent: new https.Agent({
                rejectUnauthorized: false
            })
        }

        const res: AuthResponse = await axios(config)
            .then((res) => {
                cookies.set('token', res.data.token, {
                    path: '/',
                    maxAge: 60 * 60 * 24 * 30
                })
                return { 'status': true };
            })
            .catch((err) => {
                return { 'status': false, 'error': err };
            })

        if (res.status) {
            throw redirect(302, '/');
        } else {
            return errorMessage(res.error.response.status)
        }
    }
}

function errorMessage(statusCode: number) {
    switch (statusCode) {
        case 401:
            return { msg: 'Login failed: username or password are wrong' }
        case 500:
            return { msg: 'Something went wrong, try again' }
    }
}